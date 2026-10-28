# Student Record & Academic Management Platform — AWS DevOps Automation

A GitHub-ready starter project based on the supplied Unit 4 brief. It demonstrates Terraform provisioning on AWS and Ansible configuration management for a small Flask API served behind Nginx.

## Architecture

- Terraform: VPC (`10.1.0.0/16`), public subnet (`10.1.1.0/24`), Internet Gateway, route table, security group, EC2 instance, and private/versioned S3 bucket.
- Ansible: common packages, Docker Engine, Nginx reverse proxy, and application deployment.
- Flask API: `/api/health`, `/api/students`, and `/api/marks`.
- Nginx accepts HTTP on port 80 and proxies requests to the application on port 8080.

## Important safety notes

- This starter can create billable AWS resources. Review `terraform plan` before applying.
- Set `ssh_allowed_cidr` to your own public IP in CIDR form (for example, `203.0.113.10/32`). Do not use `0.0.0.0/0` for SSH.
- Port 8080 is not exposed publicly by default; traffic should pass through Nginx on port 80.
- Do not commit AWS credentials, private keys, Terraform state, `.env` files, or real student data.
- The included Flask app uses in-memory sample data for demonstration only. It is not production-ready and does not provide authentication or persistent database storage.
- The S3 bucket name is globally unique; set `project_name` and `environment` appropriately.

## Prerequisites

- AWS account and permissions to create VPC, EC2, security groups, IAM-independent S3 resources, and related networking.
- AWS CLI configured locally (`aws configure` or an approved SSO/profile workflow).
- Terraform 1.7+.
- Ansible 2.16+ and Python 3.
- An existing EC2 key pair in the target AWS region.

## Configure

1. Copy the sample variables file:

   ```bash
   cp terraform/terraform.tfvars.example terraform/terraform.tfvars
   ```

2. Edit `terraform/terraform.tfvars`. Set `key_name`, `ssh_allowed_cidr`, and a unique `project_name`.
3. Set your AWS region through `AWS_REGION` or the `aws_region` variable.
4. Review the configuration and security settings before creating resources.

## Deploy

From the repository root:

```bash
cd terraform
terraform init
terraform fmt -check
terraform validate
terraform plan
terraform apply
terraform output
```

After apply, return to the repository root and configure Ansible:

```bash
cd ..
cp ansible/group_vars/all.yml.example ansible/group_vars/all.yml
```

Use the public IP from `terraform output -raw app_server_public_ip` to update `ansible/inventory.ini`. Ensure your private key path matches the EC2 key pair. Then run:

```bash
ansible-playbook -i ansible/inventory.ini ansible/site.yml
```

Test the deployment:

```bash
curl http://<EC2_PUBLIC_IP>/api/health
curl http://<EC2_PUBLIC_IP>/api/students
```

The health endpoint should return JSON containing `"status": "UP"`.

## Clean up

Destroy resources when finished to avoid ongoing charges:

```bash
cd terraform
terraform destroy
```

The S3 bucket is configured with `force_destroy = false`; remove any objects in it before destroying the infrastructure. Do not store important data in this demo bucket.

## Repository layout

```text
.
├── README.md
├── .gitignore
├── app/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── terraform/
│   ├── versions.tf
│   ├── variables.tf
│   ├── main.tf
│   ├── outputs.tf
│   └── terraform.tfvars.example
└── ansible/
    ├── inventory.ini.example
    ├── ansible.cfg
    ├── site.yml
    ├── group_vars/
    │   └── all.yml.example
    └── roles/
        ├── common/tasks/main.yml
        ├── docker/tasks/main.yml
        ├── nginx/tasks/main.yml
        ├── nginx/templates/library.conf.j2
        └── student_app/tasks/main.yml
```

## GitHub upload

Create a new empty GitHub repository, extract this ZIP, and run:

```bash
git init
git add .
git commit -m "Add AWS Terraform and Ansible student platform"
git branch -M main
git remote add origin https://github.com/<YOUR_USERNAME>/<YOUR_REPOSITORY>.git
git push -u origin main
```

Replace the placeholder URL with your repository URL. Never upload `terraform.tfvars`, state files, SSH keys, or credentials.
