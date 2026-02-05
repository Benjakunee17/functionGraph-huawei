# non-prod common

terraform {
  required_version = ">= 1.4.0"
  required_providers {
    huaweicloud = {
      source  = "huaweicloud/huaweicloud"
      version = ">= 1.61.0"
    }
  }
}

provider "huaweicloud" {

  project_id = var.project_id
  region     = var.region
  access_key = var.access_key
  secret_key = var.secret_key
  auth_url   = "https://iam.myhuaweicloud.com/v3"
  
}
