output "app_server_public_ip" {
  description = "Public IPv4 address for Ansible inventory and HTTP smoke tests."
  value       = aws_instance.app.public_ip
}

output "app_server_public_dns" {
  description = "Public DNS name of the EC2 instance."
  value       = aws_instance.app.public_dns
}

output "backup_bucket_name" {
  description = "Private, versioned S3 bucket for demo backup storage."
  value       = aws_s3_bucket.backup.bucket
}
