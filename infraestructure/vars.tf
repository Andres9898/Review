variable "region" {
  default = "us-east-1"
}

variable "vpc_cidr" {
  default = "10.0.0.0/24"
}

variable "public_subnets" {
  default = ["10.0.0.0/27", "10.0.0.32/27"]
}

variable "private_subnets" {
  default = ["10.0.0.64/27", "10.0.0.96/27"]
}

variable "instance_type" {
  default = "r5.large"
}

variable "db_username" {
  default = "admin"
}

variable "db_password" {
  description = "Database password"
  sensitive   = true
}
