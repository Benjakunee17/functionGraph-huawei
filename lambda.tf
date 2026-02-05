#function start ecs
resource "huaweicloud_fgs_function" "start_ecs" {
  name        = "auto-start-ecs-functiongraph-test"
  app         = "default"
  description = "auto start ECS by tag (Terraform)"

  runtime = "Python3.9"
  handler = "main.handler"

  memory_size = 256
  timeout     = 30

  # ⭐ ใช้ zip แทน inline
  code_type = "zip"
  # ส่ง zip แบบ base64 (ตามที่ error แนะนำ)
  func_code = filebase64("${path.module}/lambda-code/start-ecs/main.zip")

  functiongraph_version = "v2"
  agency                = "fg-ecs-automation"

  # environment variables (ไปโผล่ใน context.user_data ตามโค้ดคุณ)
  user_data = jsonencode({
    HUAWEI_ACCESS_KEY = var.access_key
    HUAWEI_SECRET_KEY = var.secret_key
    HUAWEI_PROJECT_ID = var.project_id
    HUAWEI_REGION     = var.region

    schedule_key      = "AutomaticStartStopSchedule"
    schedule_value    = "Enabled"
    environment_key   = "Environment"
    environment_value = "non-prod"
  })
}


#function stop ecs



resource "huaweicloud_fgs_function" "stop_ecs" {
  name        = "auto-stop-ecs-functiongraph-test"
  app         = "default"
  description = "auto start ECS by tag (Terraform)"

  runtime = "Python3.9"
  handler = "main.handler"

  memory_size = 256
  timeout     = 30

  # ⭐ ใช้ zip แทน inline
  code_type = "zip"
  # ส่ง zip แบบ base64 (ตามที่ error แนะนำ)
  func_code = filebase64("${path.module}/lambda-code/stop-ecs/main.zip")

  functiongraph_version = "v2"
  agency                = "fg-ecs-automation"

  # environment variables (ไปโผล่ใน context.user_data ตามโค้ดคุณ)
  user_data = jsonencode({
    HUAWEI_ACCESS_KEY = var.access_key
    HUAWEI_SECRET_KEY = var.secret_key
    HUAWEI_PROJECT_ID = var.project_id
    HUAWEI_REGION     = var.region

    schedule_key      = "AutomaticStartStopSchedule"
    schedule_value    = "Enabled"
    environment_key   = "Environment"
    environment_value = "non-prod"
  })
}



/************************************************************************************/

#function start rds

resource "huaweicloud_fgs_function" "start_rds" {
  name        = "auto-start-rds-functiongraph-test"
  app         = "default"
  description = "auto start RDS by tag (Terraform)"

  runtime = "Python3.9"
  handler = "main.handler"

  memory_size = 256
  timeout     = 30

  # ⭐ ใช้ zip แทน inline
  code_type = "zip"
  # ส่ง zip แบบ base64 (ตามที่ error แนะนำ)
  func_code = filebase64("${path.module}/lambda-code/start-rds/main.zip")

  functiongraph_version = "v2"
  agency                = "fg-ecs-automation"

  # environment variables (ไปโผล่ใน context.user_data ตามโค้ดคุณ)
  user_data = jsonencode({
    HUAWEI_ACCESS_KEY = var.access_key
    HUAWEI_SECRET_KEY = var.secret_key
    HUAWEI_PROJECT_ID = var.project_id
    HUAWEI_REGION     = var.region

    schedule_key      = "AutomaticStartStopSchedule"
    schedule_value    = "Enabled"
    environment_key   = "Environment"
    environment_value = "non-prod"
  })
}

#function stop rds

resource "huaweicloud_fgs_function" "stop_rds" {
  name        = "auto-stop-rds-functiongraph-test"
  app         = "default"
  description = "auto stop RDS by tag (Terraform)"

  runtime = "Python3.9"
  handler = "main.handler"

  memory_size = 256
  timeout     = 30

  # ⭐ ใช้ zip แทน inline
  code_type = "zip"
  # ส่ง zip แบบ base64 (ตามที่ error แนะนำ)
  func_code = filebase64("${path.module}/lambda-code/stop-rds/main.zip")

  functiongraph_version = "v2"
  agency                = "fg-ecs-automation"

  # environment variables (ไปโผล่ใน context.user_data ตามโค้ดคุณ)
  user_data = jsonencode({
    HUAWEI_ACCESS_KEY = var.access_key
    HUAWEI_SECRET_KEY = var.secret_key
    HUAWEI_PROJECT_ID = var.project_id
    HUAWEI_REGION     = var.region

    schedule_key      = "AutomaticStartStopSchedule"
    schedule_value    = "Enabled"
    environment_key   = "Environment"
    environment_value = "non-prod"
  })
}




