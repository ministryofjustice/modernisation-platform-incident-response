resource "aws_secretsmanager_secret" "slack_token" {
  name = "response/${terraform.workspace}/slack-token"
}

resource "aws_secretsmanager_secret" "slack_signing_key" {
  name = "response/${terraform.workspace}/slack-signing-key"
}

resource "aws_secretsmanager_secret" "slack_team_id" {
  name = "response/${terraform.workspace}/slack-team-id"
}

resource "aws_secretsmanager_secret" "database_password" {
  name = "response/${terraform.workspace}/rds-password"
}

data "aws_secretsmanager_secret_version" "database_password" {
  secret_id = aws_secretsmanager_secret.database_password.id
}

resource "aws_secretsmanager_secret" "django_secret_key" {
  name = "response/${terraform.workspace}/django-secret-key"
}

resource "aws_secretsmanager_secret" "github_client_id" {
  name = "response/${terraform.workspace}/github-client-id"
}

resource "aws_secretsmanager_secret" "github_client_secret" {
  name = "response/${terraform.workspace}/github-client-secret"
}

resource "aws_secretsmanager_secret" "statuspage_io_page_id" {
  name = "response/${terraform.workspace}/statuspageio-page-id"
}

resource "aws_secretsmanager_secret" "statuspage_io_api_key" {
  name = "response/${terraform.workspace}/statuspageio-api-key"
}

resource "aws_secretsmanager_secret" "pagerduty_api_key" {
  name = "response/${terraform.workspace}/pagerduty-api-key"
}
