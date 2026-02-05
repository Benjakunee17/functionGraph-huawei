import os
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcore.http.http_config import HttpConfig

from huaweicloudsdkrds.v3 import *
from huaweicloudsdkrds.v3.region.rds_region import RdsRegion


# ---------- Config จาก Environment Variables ----------
# HUAWEI_ACCESS_KEY, HUAWEI_SECRET_KEY, HUAWEI_PROJECT_ID, HUAWEI_REGION
# schedule_key, schedule_value, environment_key, environment_value

def get_rds_client():
    ak = os.environ.get("HUAWEI_ACCESS_KEY")
    sk = os.environ.get("HUAWEI_SECRET_KEY")
    project_id = os.environ.get("HUAWEI_PROJECT_ID")
    region = os.environ.get("HUAWEI_REGION", "ap-southeast-2")

    if not ak or not sk or not project_id:
        raise ValueError(
            "ต้องตั้งค่า HUAWEI_ACCESS_KEY, HUAWEI_SECRET_KEY, "
            "HUAWEI_PROJECT_ID ใน Environment variable"
        )

    config = HttpConfig.get_default_config()
    # ถ้าอยากเปิด verify SSL ให้เปลี่ยนเป็น False
    config.ignore_ssl_verification = True

    credentials = BasicCredentials(ak, sk, project_id)

    client = RdsClient.new_builder() \
        .with_http_config(config) \
        .with_credentials(credentials) \
        .with_region(RdsRegion.value_of(region)) \
        .build()

    return client


# ---------- ฟังก์ชันเรียก stop RDS ----------
def stop_rds_instance(client, instance_id: str):
    """
    เรียก Stop RDS Instance ตาม instance_id

    ⚠ ถ้าชื่อ class/method ไม่ตรง (เช่น StopInstanceRequest / stop_instance)
    ให้ดูจาก API Explorer → RDS → Stop Instance → Python SDK แล้วปรับตามนั้น
    """
    req = StopInstanceRequest(instance_id=instance_id)
    resp = client.stop_instance(req)

    print(f"เรียก StopInstance สำหรับ RDS {instance_id} แล้ว")
    return resp


# ---------- ฟังก์ชันหาจาก Tag ----------
def list_rds_by_tag_value(client, tags):
    """
    tags = [
        [schedule_key, schedule_value],
        [environment_key, environment_value]
    ]
    """
    schedule_key, schedule_value = tags[0]
    env_key, env_value = tags[1]

    # ⚠ ถ้าชื่อ request/list method ต่าง ให้เช็คใน API Explorer -> Query Instances
    request = ListInstancesRequest()
    instances = []
    matched_ids = []

    try:
        response = client.list_instances(request)
        # ชื่อ field อาจเป็น instances / items / db_instances แล้วแต่เวอร์ชัน
        instances = getattr(response, "instances", []) or \
                    getattr(response, "items", []) or \
                    getattr(response, "db_instances", [])
    except exceptions.ClientRequestException as e:
        print(f"Error listing RDS instances: {e.status_code} {e.error_msg}")
        return []

    print(f"พบ RDS Instance ทั้งหมด {len(instances)} ตัวใน project นี้")

    for ins in instances:
        tags_list = getattr(ins, "tags", []) or []

        schedule_match = False
        env_match = False

        kv = {}

        # รูปแบบ object (เช่น TagResp, TagItem)
        for t in tags_list:
            if hasattr(t, "key") and hasattr(t, "value"):
                kv[t.key] = t.value
            elif isinstance(t, dict):
                k = t.get("key")
                v = t.get("value")
                if k is not None:
                    kv[k] = v
            elif isinstance(t, str) and "=" in t:
                k, v = t.split("=", 1)
                kv[k] = v

        if kv.get(schedule_key) == schedule_value:
            schedule_match = True
        if kv.get(env_key) == env_value:
            env_match = True

        ins_id = getattr(ins, "id", None) or getattr(ins, "instance_id", None)
        ins_name = getattr(ins, "name", "") or getattr(ins, "instance_name", "")

        if schedule_match and env_match:
            print(f"Matched RDS: id={ins_id}, name={ins_name}, tags={kv}")
            if ins_id:
                matched_ids.append(ins_id)
        else:
            print(f"Skip RDS: id={ins_id}, name={ins_name}, tags={kv}")

    print(f"RDS ที่ตรง Tag เงื่อนไขทั้งหมด: {len(matched_ids)} ตัว")
    return matched_ids


# ---------- ฟังก์ชันหลัก ----------
def stop_rds_all():
    schedule_key = os.environ["schedule_key"]
    schedule_value = os.environ["schedule_value"]

    environment_key = os.environ["environment_key"]
    environment_value = os.environ["environment_value"]

    tags = [
        [schedule_key, schedule_value],
        [environment_key, environment_value],
    ]

    client = get_rds_client()

    ids = list_rds_by_tag_value(client, tags)
    if len(ids) > 0:
        for instance_id in ids:
            print(f"Stopping RDS: {instance_id}")
            stop_rds_instance(client, instance_id)
    else:
        print("ไม่พบ RDS ที่มี Tag ตามเงื่อนไข")


# ---------- Entry สำหรับ FunctionGraph ----------
def handler(event, context):
    stop_rds_all()
