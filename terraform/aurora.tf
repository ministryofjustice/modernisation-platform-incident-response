resource "aws_rds_cluster" "db" {
  cluster_identifier           = "response-${terraform.workspace}"
  apply_immediately            = true
  availability_zones           = ["eu-west-1a", "eu-west-1b", "eu-west-1c"]
  backup_retention_period      = 14
  database_name                = "response"
  db_subnet_group_name         = data.aws_db_subnet_group.data_persitance_subnet_group.name
  deletion_protection          = true
  engine                       = "aurora-postgresql"
  engine_mode                  = "serverless"
  final_snapshot_identifier    = "response-${terraform.workspace}-final-snapshot"
  kms_key_id                   = data.aws_kms_key.rds.arn
  master_username              = "response"
  master_password              = data.aws_secretsmanager_secret_version.database_password.secret_string
  preferred_backup_window      = "05:15-05:45"
  preferred_maintenance_window = "mon:05:50-mon:06:20"
  storage_encrypted            = true
  skip_final_snapshot          = false
  vpc_security_group_ids       = [aws_security_group.response_rds.id]
  scaling_configuration {
    auto_pause               = true
    max_capacity             = 16
    min_capacity             = 4
    seconds_until_auto_pause = 86400
    timeout_action           = "ForceApplyCapacityChange"
  }
}

resource "aws_security_group" "response_rds" {
  name        = "response-rds-${terraform.workspace}"
  description = "response rds access"
  vpc_id      = data.aws_vpc.default.id
  tags        = { "Name" = "response-api-${terraform.workspace}" }
}

resource "aws_security_group_rule" "response_rds_ecs_task" {
  type                     = "ingress"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  security_group_id        = aws_security_group.response_rds.id
  source_security_group_id = aws_security_group.ecs_service.id
  description              = "Response RDS inbound from Response ECS tasks"
}

resource "aws_db_subnet_group" "data_persitance_subnet_group" {
  name       = "data-persitance-subnet-${terraform.workspace}"
  subnet_ids = data.aws_subnet_ids.data_persitance.ids
}
