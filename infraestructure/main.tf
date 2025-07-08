provider "aws" {
  region = var.region
}

# VPC and Subnets
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.2"

  name                 = "farmamigo-vpc"
  cidr                 = var.vpc_cidr
  azs                  = ["${var.region}a", "${var.region}b"]
  public_subnets       = var.public_subnets
  private_subnets      = var.private_subnets
  enable_nat_gateway   = true
  single_nat_gateway   = true
  enable_dns_hostnames = true
  enable_dns_support   = true
}

# Security Groups
resource "aws_security_group" "alb_sg" {
  name   = "alb-sg"
  vpc_id = module.vpc.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "internal_sg" {
  name   = "internal-traffic"
  vpc_id = module.vpc.vpc_id

  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Launch Template
resource "aws_launch_template" "app" {
  name_prefix   = "farmamigo-app-"
  image_id      = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  vpc_security_group_ids = [aws_security_group.internal_sg.id]

  user_data = base64encode(<<-EOF
              #!/bin/bash
              curl -sL https://deb.nodesource.com/setup_18.x | bash -
              apt-get install -y nodejs
              cd /home/ubuntu/app && npm install && npm start
            EOF
  )
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
}

# AutoScaling Group
resource "aws_autoscaling_group" "app_asg" {
  desired_capacity     = 1
  max_size             = 2
  min_size             = 1
  vpc_zone_identifier  = module.vpc.public_subnets
  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }
  tag {
    key                 = "Name"
    value               = "farmamigo-app"
    propagate_at_launch = true
  }
}

# Load Balancer
resource "aws_lb" "app_lb" {
  name               = "farmamigo-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = module.vpc.public_subnets
}

resource "aws_lb_target_group" "app_tg" {
  name     = "farmamigo-tg"
  port     = 3000
  protocol = "HTTP"
  vpc_id   = module.vpc.vpc_id
  target_type = "instance"
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.app_lb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app_tg.arn
  }
}

resource "aws_autoscaling_attachment" "asg_attachment" {
  autoscaling_group_name = aws_autoscaling_group.app_asg.name
  lb_target_group_arn    = aws_lb_target_group.app_tg.arn
}

# Aurora PostgreSQL Cluster
module "aurora" {
  source  = "terraform-aws-modules/rds-aurora/aws"
  version = "8.5.0"

  name                 = "farmamigo-db"
  engine               = "aurora-postgresql"
  engine_version       = "15.3"
  instance_class       = "db.r5.large"
  instances            = 2
  master_username      = var.db_username
  master_password      = var.db_password
  vpc_id               = module.vpc.vpc_id
  subnets              = module.vpc.private_subnets
  security_group_ids   = [aws_security_group.internal_sg.id]
  storage_encrypted    = true
  skip_final_snapshot  = true
}

# CloudFront
resource "aws_cloudfront_distribution" "app_cdn" {
  origin {
    domain_name = aws_lb.app_lb.dns_name
    origin_id   = "alb-origin"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  enabled             = true
  default_root_object = ""
  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "alb-origin"

    viewer_protocol_policy = "redirect-to-https"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }
}
