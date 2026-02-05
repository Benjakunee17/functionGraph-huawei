#function start ecs
resource "huaweicloud_fgs_function_trigger" "start_ecs_timer" {
  function_urn = huaweicloud_fgs_function.start_ecs.urn
  type         = "TIMER"
  status       = "ACTIVE"

  # event_data เป็น JSON string
  event_data = jsonencode({
    name           = "FunctionGraph-start"
    schedule_type  = "Cron"           # หรือ "Rate" ถ้าใช้ @every
    sync_execution = false            # async
    user_event     = "Start ECS by tag on schedule"
    schedule       = "0 05 11 ? * MON-FRI"
  })
}


# #function stop ecs

resource "huaweicloud_fgs_function_trigger" "stop_ecs_timer" {
  function_urn = huaweicloud_fgs_function.stop_ecs.urn
  type         = "TIMER"
  status       = "ACTIVE"

  # event_data เป็น JSON string
  event_data = jsonencode({
    name           = "FunctionGraph-stop-ecs"
    schedule_type  = "Cron"           # หรือ "Rate" ถ้าใช้ @every
    sync_execution = false            # async
    user_event     = "Stop ECS by tag on schedule"
    schedule       = "0 30 11 ? * MON-FRI"
  })
}

/***********************************************************************************************************************/

#function start rds
resource "huaweicloud_fgs_function_trigger" "start_rds_timer" {
  function_urn = huaweicloud_fgs_function.start_rds.urn
  type         = "TIMER"
  status       = "ACTIVE"

  # event_data เป็น JSON string
  event_data = jsonencode({
    name           = "FunctionGraph-start-rds"
    schedule_type  = "Cron"           # หรือ "Rate" ถ้าใช้ @every
    sync_execution = false            # async
    user_event     = "Start RDS by tag on schedule"
    schedule       = "0 05 11 ? * MON-FRI"
  })
}



#function stop rds
resource "huaweicloud_fgs_function_trigger" "stop_rds_timer" {
  function_urn = huaweicloud_fgs_function.stop_rds.urn
  type         = "TIMER"
  status       = "ACTIVE"

  # event_data เป็น JSON string
  event_data = jsonencode({
    name           = "FunctionGraph-stop-rds"
    schedule_type  = "Cron"           # หรือ "Rate" ถ้าใช้ @every
    sync_execution = false            # async
    user_event     = "Stop RDS by tag on schedule"
    schedule       = "0 05 11 ? * MON-FRI"
  })
}
