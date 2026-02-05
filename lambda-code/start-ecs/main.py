import os
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcore.http.http_config import HttpConfig
from huaweicloudsdkecs.v2 import *
from huaweicloudsdkecs.v2.region.ecs_region import EcsRegion

# ---------- Config จาก Environment Variables ----------
# HUAWEI_ACCESS_KEY, HUAWEI_SECRET_KEY, HUAWEI_PROJECT_ID, HUAWEI_REGION
# schedule_key, schedule_value, environment_key, environment_value

def get_ecs_client():
    ak = os.environ.get("HUAWEI_ACCESS_KEY")
    sk = os.environ.get("HUAWEI_SECRET_KEY")
    project_id = os.environ.get("HUAWEI_PROJECT_ID")
    region = os.environ.get("HUAWEI_REGION", "ap-southeast-2")

    if not ak or not sk or not project_id:
        raise ValueError("ต้องตั้งค่า HUAWEI_ACCESS_KEY, HUAWEI_SECRET_KEY, HUAWEI_PROJECT_ID ใน Environment variable")

    config = HttpConfig.get_default_config()
    config.ignore_ssl_verification = True  # ถ้าอยากเปิด verify SSL ให้เปลี่ยนเป็น False

    credentials = BasicCredentials(ak, sk, project_id)

    client = EcsClient.new_builder() \
        .with_http_config(config) \
        .with_credentials(credentials) \
        .with_region(EcsRegion.value_of(region)) \
        .build()

    return client


# ---------- ฟังก์ชันเรียก start ECS ----------
def start_ecs_instance(client, instance_id):
    req_body = BatchStartServersRequestBody(
        os_start=BatchStartServersOption(
            servers=[ServerId(id=instance_id)]
        )
    )
    request = BatchStartServersRequest(body=req_body)
    response = client.batch_start_servers(request)
    print(f"เรียก BatchStartServers สำหรับ {instance_id} แล้ว")
    return response


# ---------- ฟังก์ชันหาจาก Tag ----------
def list_ecs_by_tag_value(client, tags):
    """
    tags = [
        [schedule_key, schedule_value],
        [environment_key, environment_value]
    ]
    """
    schedule_key, schedule_value = tags[0]
    env_key, env_value = tags[1]

    request = ListServersDetailsRequest()
    servers = []
    instance_ids = []

    try:
        response = client.list_servers_details(request)
        servers.extend(response.servers)
    except exceptions.ClientRequestException as e:
        print(f"Error listing ECS servers: {e.status_code} {e.error_msg}")
        return []

    print(f"พบ ECS ทั้งหมด {len(servers)} ตัวใน project นี้")

    for s in servers:
        metadata = getattr(s, "metadata", {}) or {}
        tags_list = getattr(s, "tags", []) or []

        schedule_match = False
        env_match = False

        # 1) เช็คใน metadata
        if metadata.get(schedule_key) == schedule_value:
            schedule_match = True
        if metadata.get(env_key) == env_value:
            env_match = True

        # 2) เช็คใน tags_list (object / dict / 'KEY=VALUE')
        if not (schedule_match and env_match) and tags_list:
            kv = {}

            for t in tags_list:
                # รูปแบบ object ของ SDK (เช่น ServerTag)
                if hasattr(t, "key") and hasattr(t, "value"):
                    kv[t.key] = t.value
                # รูปแบบ dict
                elif isinstance(t, dict):
                    k = t.get("key")
                    v = t.get("value")
                    if k is not None:
                        kv[k] = v
                # รูปแบบ string: "KEY=VALUE"
                elif isinstance(t, str) and "=" in t:
                    k, v = t.split("=", 1)
                    kv[k] = v

            if kv.get(schedule_key) == schedule_value:
                schedule_match = True
            if kv.get(env_key) == env_value:
                env_match = True

        if schedule_match and env_match:
            print(f"Matched ECS: id={s.id}, name={getattr(s, 'name', '')}, "
                  f"metadata={metadata}, tags={tags_list}")
            instance_ids.append(s.id)
        else:
            print(f"Skip ECS: id={s.id}, name={getattr(s, 'name', '')}, "
                  f"metadata={metadata}, tags={tags_list}")

    print(f"ECS ที่ตรง Tag เงื่อนไขทั้งหมด: {len(instance_ids)} ตัว")
    return instance_ids


# ---------- ฟังก์ชันหลัก ----------
def start_ecs_all():
    schedule_key = os.environ["schedule_key"]
    schedule_value = os.environ["schedule_value"]

    environment_key = os.environ["environment_key"]
    environment_value = os.environ["environment_value"]

    tags = [[schedule_key, schedule_value],
            [environment_key, environment_value]]

    client = get_ecs_client()

    ids = list_ecs_by_tag_value(client, tags)
    if len(ids) > 0:
        for instance_id in ids:
            print(f"Starting ECS: {instance_id}")
            start_ecs_instance(client, instance_id)
    else:
        print("ไม่พบ ECS ที่มี Tag ตามเงื่อนไข")


# ---------- Entry สำหรับ FunctionGraph ----------
def handler(event, context):
    start_ecs_all()
