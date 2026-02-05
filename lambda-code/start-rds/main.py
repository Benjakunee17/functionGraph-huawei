import os
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcore.http.http_config import HttpConfig

# 👇 เปลี่ยนมาใช้ RDS SDK
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


# ---------- ฟังก์ชันเรียก start RDS ----------
def start_rds_instance(client, instance_id: str):
    """
    เรียก Start RDS Instance ตาม instance_id
    ⚠ ถ้าชื่อ class/method ไม่ตรง ให้ดูจาก API Explorer → RDS → Start Instance → Python SDK
    ตัวอย่างทั่วไปจะเป็นประมาณนี้:
    """
    # ตัวอย่างชื่อ Request/Method ที่ใช้บ่อยใน SDK V3
    req = StartInstanceRequest(instance_id=instance_id)
    resp = client.start_instance(req)

    print(f"เรียก StartInstance สำหรับ RDS {instance_id} แล้ว")
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

    # RDS ส่วนใหญ่ใช้ ListInstancesRequest / ListInstancesDetailsRequest
    # ⚠ ชื่อ request อาจต่าง ให้เช็คใน API Explorer -> Query Instances
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
        # พยายามอ่าน tags ในหลายรูปแบบ (แล้วแต่ SDK)
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

        if schedule_match and env_match:
            ins_id = getattr(ins, "id", None) or getattr(ins, "instance_id", None)
            ins_name = getattr(ins, "name", "") or getattr(ins, "instance_name", "")
            print(f"Matched RDS: id={ins_id}, name={ins_name}, tags={kv}")
            if ins_id:
                matched_ids.append(ins_id)
        else:
            ins_id = getattr(ins, "id", None) or getattr(ins, "instance_id", None)
            ins_name = getattr(ins, "name", "") or getattr(ins, "instance_name", "")
            print(f"Skip RDS: id={ins_id}, name={ins_name}, tags={kv}")

    print(f"RDS ที่ตรง Tag เงื่อนไขทั้งหมด: {len(matched_ids)} ตัว")
    return matched_ids


# ---------- ฟังก์ชันหลัก ----------
def start_rds_all():
    # ใช้ env key/value แบบเดียวกับตอน ECS ได้เลย
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
            print(f"Starting RDS: {instance_id}")
            start_rds_instance(client, instance_id)
    else:
        print("ไม่พบ RDS ที่มี Tag ตามเงื่อนไข")


# ---------- Entry สำหรับ FunctionGraph ----------
def handler(event, context):
    start_rds_all()
