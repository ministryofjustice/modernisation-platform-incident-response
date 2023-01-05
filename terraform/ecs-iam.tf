
resource "aws_iam_role" "response_primary" {
  name_prefix        = "response-primary-"
  assume_role_policy = data.aws_iam_policy_document.ecs_tasks_assume_policy.json
}

resource "aws_iam_role_policy" "response_primary" {
  role   = aws_iam_role.response_primary.name
  policy = data.aws_iam_policy_document.response_primary.json
}

data "aws_iam_policy_document" "response_primary" {
  statement {
    sid       = "SecretManagerListAllSecrets"
    effect    = "Allow"
    resources = ["*"]

    actions = ["secretsmanager:ListSecrets"]
  }

  statement {
    sid       = "SecretManagerRetrieveAccountSecrets"
    effect    = "Allow"
    resources = ["arn:aws:secretsmanager:eu-west-1:${data.aws_caller_identity.current.account_id}:secret:*"]

    actions = ["secretsmanager:GetSecretValue"]
  }
}

resource "aws_iam_role" "execution_role" {
  name_prefix        = "execution_role-"
  assume_role_policy = data.aws_iam_policy_document.ecs_tasks_assume_policy.json
}

resource "aws_iam_role_policy" "execution_role" {
  role   = aws_iam_role.execution_role.id
  policy = data.aws_iam_policy_document.execution_role.json
}

data "aws_iam_policy_document" "execution_role" {
  statement {
    effect    = "Allow"
    resources = ["*"]

    actions = [
      "ecr:GetAuthorizationToken",
      "ecr:BatchCheckLayerAvailability",
      "ecr:GetDownloadUrlForLayer",
      "ecr:BatchGetImage",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "ssm:GetParameters",
      "secretsmanager:GetSecretValue",
    ]
  }
}

data "aws_iam_policy_document" "ecs_tasks_assume_policy" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      identifiers = ["ecs-tasks.amazonaws.com"]
      type        = "Service"
    }
  }
}
