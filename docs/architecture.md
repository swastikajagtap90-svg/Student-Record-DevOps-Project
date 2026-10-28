# Architecture Notes

1. Public HTTP requests reach the EC2 security group on port 80.
2. Nginx reverse-proxies to the Docker-published loopback port `127.0.0.1:8080`.
3. The Flask API is containerized and does not expose port 8080 to the internet.
4. SSH ingress is restricted to the `ssh_allowed_cidr` Terraform variable.
5. S3 is private, blocks public access, uses server-side encryption, and enables versioning.

This is a learning/demo architecture, not a production reference design. For production, add TLS, IAM instance roles, centralized secrets, durable database storage, logging/monitoring, patch management, private subnets/NAT or Systems Manager access, and a multi-AZ design.
