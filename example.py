import requests
import json
import os
 
# ใส่ ECS IDs ที่ต้องการเปิด
ECS_IDS = [
    "5b5ce0b4-211f-4db6-8643-80a889cc87d0",
    "e210dfb5-2d95-466f-a704-2fc1f13718b3",
    "013e6035-a01d-4dff-a98d-04e83936b38c",
    "79075271-6198-456d-822a-8fa111668b81",
    "b354fe42-1f30-420c-8f72-80ae42ecf45e",
    "8fdf347a-25b7-4370-8f7f-3eb29dc29779",
    "41eb383c-210e-4e83-9784-4d1758ce861b",
    "6c8c03d6-d7b0-4fec-b705-20dd94eae282",
    "a28342e3-3525-4131-b34c-7f26821373e2"
]
# region เดียวกับ ECS
REGION = "ap-southeast-2"
 
def handler(event, context):
    token = context.getToken()
    url = f"https://ecs.{REGION}.myhuaweicloud.com/v1/{context.getProjectID()}/cloudservers/action"
   
    payload = {
        "os-start": {
            "servers": [{"id": ecs_id} for ecs_id in ECS_IDS]
        }
    }
   
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": token
    }
   
    response = requests.post(url, headers=headers, data=json.dumps(payload))
   
    return {
        "status": response.status_code,
        "response": response.text
    }
