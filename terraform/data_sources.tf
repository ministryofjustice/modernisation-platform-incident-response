data "aws_vpc" "default" {
  default = true
}

data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_subnet_ids" "public" {
  vpc_id = data.aws_vpc.default.id
  tags   = { Name = "*public*" }
}

data "aws_subnet" "public" {
  count             = length(tolist(data.aws_subnet_ids.public.ids))
  availability_zone = data.aws_availability_zones.available.names[count.index]
  tags              = { Name = "*public*" }
}

data "aws_subnet_ids" "private" {
  vpc_id = data.aws_vpc.default.id
  tags   = { Name = "private" }
}

data "aws_subnet" "private" {
  count             = length(tolist(data.aws_subnet_ids.private.ids))
  availability_zone = data.aws_availability_zones.available.names[count.index]
  tags              = { Name = "private" }
}

data "aws_subnet_ids" "data_persitance" {
  vpc_id = data.aws_vpc.default.id

  filter {
    name   = "tag:Name"
    values = ["persistence"]
  }
}

data "aws_caller_identity" "current" {}

data "aws_kms_key" "rds" {
  key_id = "alias/aws/rds"
}

data "aws_db_subnet_group" "data_persitance_subnet_group" {
  name = "data-persitance-subnet-${terraform.workspace}"
}
