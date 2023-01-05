locals {
  dns_prefixes = {
    "development" = "dev.incident"
    "production"  = "incident"
  }

  is_production = {
    "development" = "false"
    "production"  = "true"
  }

  dns_prefix = "incident"

  mandatory_moj_tags = {
    business-unit    = "OPG"
    application      = "opg-incident-response"
    environment-name = terraform.workspace
    owner            = "OPG Webops: opgteam@digital.justice.gov.uk"
  }

  optional_tags = {
    infrastructure-support = "OPG Webops: opgteam@digital.justice.gov.uk"
    terraform-managed      = "Managed by Terraform"
  }

  tags = merge(local.mandatory_moj_tags, local.optional_tags)
}

variable "default_role" {
  default = "incident-response-ci"
}

variable "management_role" {
  default = "incident-response-ci"
}

variable "accounts" {
  default = {
    "development" = "679638075911"
    "production"  = "997462338508"
  }
}
