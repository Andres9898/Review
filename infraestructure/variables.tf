variable "region" {}
variable "vpc_cidr" {}
variable "public_subnets" {}
variable "private_subnets" {}
variable "instance_type" {}
variable "db_username" {}
variable "db_password" {
  sensitive = true
}