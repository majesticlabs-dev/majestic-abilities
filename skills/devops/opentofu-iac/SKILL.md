---
name: opentofu-iac
description: "Build and maintain infrastructure as code with OpenTofu and HCL. Use when creating `.tf` files, configuring providers and remote state, reviewing plans, managing environments, or extracting justified reusable modules."
---

# OpenTofu Infrastructure as Code

## ⚠️ SIMPLICITY FIRST - Default to Flat Files

**ALWAYS start with the simplest approach. Only add complexity when explicitly requested.**

### Simple (DEFAULT) vs Overengineered

| Aspect | ✅ Simple (Default) | ❌ Overengineered |
|--------|---------------------|-------------------|
| Structure | Flat .tf files in one directory | Nested modules/ + environments/ directories |
| Modules | None or only remote registry modules | Custom local modules for simple resources |
| Environments | Workspaces OR single tfvars | Duplicate directory per environment |
| Variables | Inline defaults, minimal tfvars | Complex variable hierarchies |
| File count | 3-5 .tf files total | 15+ files across nested directories |

### When to Use Simple Approach (90% of cases)

- Managing 1-5 resources of each type
- Single provider, single region
- Small team or solo developer
- Standard infrastructure patterns

### When Complexity is Justified (10% of cases)

- Enterprise multi-region, multi-account
- Reusable modules shared across teams
- Complex dependency chains
- User explicitly requests modular structure

**Rule: If you can define everything in 5 flat .tf files, DO IT.**

### Simple Project Structure (DEFAULT)

```
infra/
├── main.tf           # All resources
├── variables.tf      # Input variables
├── outputs.tf        # Outputs
├── versions.tf       # Provider versions
└── terraform.tfvars  # Variable values (gitignored)
```

## Overview

OpenTofu is a community-driven, open-source fork of Terraform under MPL-2.0 license, maintained by the Linux Foundation. It uses HashiCorp Configuration Language (HCL) for declarative infrastructure management across cloud providers.

## Core Philosophy

Prioritize:
- **Declarative over imperative**: Describe desired state, not steps
- **Idempotency**: Apply safely multiple times with same result
- **Modularity**: Compose infrastructure from reusable modules
- **State as truth**: State file is the source of truth for managed resources
- **Immutable infrastructure**: Replace resources rather than mutate in place

## HCL Syntax Essentials

### Resource Blocks

```hcl
resource "aws_instance" "web" {
  ami           = var.ami_id
  instance_type = var.instance_type

  tags = {
    Name        = "${var.project}-web"
    Environment = var.environment
  }
}
```

### Data Sources

```hcl
data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  owners = ["099720109477"]  # Canonical
}
```

### Variables

```hcl
variable "environment" {
  description = "Deployment environment (dev, staging, prod)"
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "instance_types" {
  description = "Map of environment to instance type"
  type        = map(string)
  default = {
    dev     = "t3.micro"
    staging = "t3.small"
    prod    = "t3.medium"
  }
}
```

### Outputs

```hcl
output "instance_ip" {
  description = "Public IP of the web instance"
  value       = aws_instance.web.public_ip
  sensitive   = false
}

output "database_password" {
  description = "Generated database password"
  value       = random_password.db.result
  sensitive   = true
}
```

### Locals

```hcl
locals {
  common_tags = {
    Project     = var.project
    Environment = var.environment
    ManagedBy   = "OpenTofu"
  }

  name_prefix = "${var.project}-${var.environment}"
}
```

## Meta-Arguments

### count - Create Multiple Instances

```hcl
resource "aws_instance" "server" {
  count = var.server_count

  ami           = var.ami_id
  instance_type = var.instance_type

  tags = {
    Name = "${local.name_prefix}-server-${count.index}"
  }
}
```

### for_each - Create from Map/Set

```hcl
resource "aws_iam_user" "users" {
  for_each = toset(var.user_names)

  name = each.value
  path = "/users/"
}

resource "aws_security_group_rule" "ingress" {
  for_each = var.ingress_rules

  type              = "ingress"
  from_port         = each.value.port
  to_port           = each.value.port
  protocol          = each.value.protocol
  cidr_blocks       = each.value.cidr_blocks
  security_group_id = aws_security_group.main.id
}
```

### depends_on - Explicit Dependencies

```hcl
resource "aws_instance" "app" {
  ami           = var.ami_id
  instance_type = var.instance_type

  depends_on = [
    aws_db_instance.database,
    aws_elasticache_cluster.cache
  ]
}
```

### lifecycle - Control Resource Behavior

```hcl
resource "aws_instance" "critical" {
  ami           = var.ami_id
  instance_type = var.instance_type

  lifecycle {
    prevent_destroy = true
    create_before_destroy = true
    ignore_changes = [
      tags["LastUpdated"],
      user_data
    ]
  }
}

# Replace when AMI changes
resource "aws_instance" "immutable" {
  ami           = var.ami_id
  instance_type = var.instance_type

  lifecycle {
    replace_triggered_by = [
      null_resource.ami_trigger
    ]
  }
}
```

## Detailed Reference

Load [restored-examples.md](references/restored-examples.md) for additional HCL examples, templates, and advanced patterns.
