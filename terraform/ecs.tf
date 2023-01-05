resource "aws_ecs_cluster" "cluster" {
  name = "incident-response"
}

resource "aws_ecs_service" "service" {
  name             = "response"
  cluster          = aws_ecs_cluster.cluster.id
  task_definition  = aws_ecs_task_definition.response.arn
  desired_count    = 1
  launch_type      = "FARGATE"
  platform_version = "1.4.0"
  depends_on       = [aws_lb.loadbalancer]

  deployment_controller {
    type = "ECS"
  }

  network_configuration {
    security_groups  = [aws_security_group.ecs_service.id]
    subnets          = data.aws_subnet.private.*.id
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.tg.arn
    container_name   = "nginx"
    container_port   = 80
  }
}

resource "aws_security_group" "ecs_service" {
  name_prefix = "ecs_service-"
  vpc_id      = data.aws_vpc.default.id

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_security_group_rule" "ecs_ingress" {
  description              = "Allow load balancer in on 80"
  type                     = "ingress"
  from_port                = 80
  to_port                  = 80
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.incident_response_loadbalancer.id
  security_group_id        = aws_security_group.ecs_service.id
}

resource "aws_security_group_rule" "ecs_outbound" {
  description       = "Allow all outbound traffic from the ECS service"
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.ecs_service.id
}

resource "aws_cloudwatch_log_group" "response" {
  name = "response"
}
