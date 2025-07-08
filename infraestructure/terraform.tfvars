region        = "us-east-1"
vpc_cidr      = "10.0.0.0/24"
public_subnets  = ["10.0.0.0/27", "10.0.0.32/27"]
private_subnets = ["10.0.0.64/27", "10.0.0.96/27"]
instance_type = "r5.large"

db_username = "admin"
db_password = "SuperSecurePassword123!"
