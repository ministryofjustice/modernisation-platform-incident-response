data "aws_route53_zone" "opg_service_justice_gov_uk" {
  provider = aws.management
  name     = "opg.service.justice.gov.uk"
}

resource "aws_route53_record" "response" {
  provider = aws.management
  zone_id  = data.aws_route53_zone.opg_service_justice_gov_uk.zone_id
  name     = local.dns_prefix
  type     = "A"

  alias {
    evaluate_target_health = false
    name                   = aws_lb.loadbalancer.dns_name
    zone_id                = aws_lb.loadbalancer.zone_id
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_acm_certificate" "response" {
  domain_name       = aws_route53_record.response.fqdn
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route53_record" "validation" {
  for_each = {
    for dvo in aws_acm_certificate.response.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }
  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  provider        = aws.management
  zone_id         = data.aws_route53_zone.opg_service_justice_gov_uk.id
  depends_on      = [aws_acm_certificate.response]
}

resource "aws_acm_certificate_validation" "response" {
  certificate_arn         = aws_acm_certificate.response.arn
  validation_record_fqdns = [for record in aws_route53_record.validation : record.fqdn]
  depends_on              = [aws_route53_record.validation]
}

output "response_domain" {
  value = aws_route53_record.response.fqdn
}
