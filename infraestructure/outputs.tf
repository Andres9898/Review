output "vpc_id" {
  description = "ID de la VPC principal"
  value       = module.vpc.vpc_id
}

output "public_subnets" {
  description = "Subredes públicas"
  value       = module.vpc.public_subnets
}

output "private_subnets" {
  description = "Subredes privadas"
  value       = module.vpc.private_subnets
}

output "alb_dns_name" {
  description = "DNS del Load Balancer"
  value       = aws_lb.app_lb.dns_name
}

output "cloudfront_domain" {
  description = "Dominio de distribución CloudFront"
  value       = aws_cloudfront_distribution.app_cdn.domain_name
}

output "aurora_cluster_endpoint" {
  description = "Endpoint principal del clúster Aurora"
  value       = module.aurora.cluster_endpoint
}

output "aurora_reader_endpoint" {
  description = "Endpoint de lectura del clúster Aurora"
  value       = module.aurora.cluster_reader_endpoint
}

output "autoscaling_group_name" {
  description = "Nombre del grupo de AutoScaling"
  value       = aws_autoscaling_group.app_asg.name
}
