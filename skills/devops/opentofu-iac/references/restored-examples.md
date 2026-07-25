# OpenTofu Infrastructure as Code Detailed Reference

## Module Design

### Module Structure

```
modules/
└── vpc/
    ├── main.tf          # Primary resources
    ├── variables.tf     # Input variables
    ├── outputs.tf       # Output values
    ├── versions.tf      # Required providers
    └── README.md        # Documentation
```

### Calling Modules

```hcl
module "vpc" {
  source = "./modules/vpc"

  cidr_block  = "10.0.0.0/16"
  environment = var.environment

  azs             = ["us-east-1a", "us-east-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]
}

# Remote module with version
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = local.cluster_name
  cluster_version = "1.29"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnet_ids
}
```

### Module Best Practices

- Expose minimal, clear interface of variables
- Use sensible defaults where possible
- Document all variables and outputs
- Avoid over-generic "god" modules
- Prefer composition over configuration flags
- Version pin remote modules

## State Management

### Remote Backend (S3)

```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/network/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

### OpenTofu State Encryption (Unique Feature)

```hcl
terraform {
  encryption {
    key_provider "pbkdf2" "main" {
      passphrase = var.state_encryption_passphrase
    }

    method "aes_gcm" "encrypt" {
      keys = key_provider.pbkdf2.main
    }

    state {
      method   = method.aes_gcm.encrypt
      enforced = true
    }

    plan {
      method   = method.aes_gcm.encrypt
      enforced = true
    }
  }
}
```

### State Commands

```bash
# List resources in state
tofu state list

# Show specific resource
tofu state show aws_instance.web

# Move resource (refactoring)
tofu state mv aws_instance.old aws_instance.new

# Remove from state (without destroying)
tofu state rm aws_instance.imported

# Import existing resource
tofu import aws_instance.web i-1234567890abcdef0
```

See [Provider Configuration](provider-config.md) for AWS provider setup, authentication methods, and multi-provider patterns.

See [Environment Strategies](environment-strategies.md) for workspaces and directory-based environment management.

## CLI Workflow

```bash
# Initialize working directory
tofu init

# Validate configuration
tofu validate

# Format code
tofu fmt -recursive

# Preview and review changes
tofu plan -out=plan.tfplan
tofu show plan.tfplan
read -r -p "Apply this reviewed plan? [y/N] " reply
case "$reply" in y|Y|yes|YES) ;; *) echo "Apply cancelled"; exit 1 ;; esac

# Apply the reviewed plan
tofu apply plan.tfplan

# Destroy infrastructure
tofu destroy

# Show current state
tofu show

# Review and apply state refresh separately
tofu plan -refresh-only -out=refresh.tfplan
tofu show refresh.tfplan
read -r -p "Apply this reviewed refresh plan? [y/N] " reply
case "$reply" in y|Y|yes|YES) ;; *) echo "Refresh cancelled"; exit 1 ;; esac
tofu apply refresh.tfplan
```

## Best Practices Checklist

When writing OpenTofu/Terraform code:

- [ ] Use remote backend with locking for team use
- [ ] Enable state encryption (OpenTofu feature)
- [ ] Never commit `.tfstate` or `.tfvars` with secrets to VCS
- [ ] Pin provider and module versions
- [ ] Use `tofu plan` before every `apply`
- [ ] Use `lifecycle.prevent_destroy` for critical resources
- [ ] Document all variables and outputs
- [ ] Use `locals` for computed values and tags
- [ ] Prefer `for_each` over `count` for named resources
- [ ] Use validation blocks for variable constraints
- [ ] Store secrets in secret managers, not in code

## Common Patterns

### Conditional Resources

```hcl
resource "aws_eip" "static" {
  count = var.create_elastic_ip ? 1 : 0

  instance = aws_instance.web.id
}
```

### Dynamic Blocks

```hcl
resource "aws_security_group" "main" {
  name = "${local.name_prefix}-sg"

  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.port
      to_port     = ingress.value.port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
    }
  }
}
```

## References

For detailed patterns and examples:
- [references/hcl-patterns.md](hcl-patterns.md) - Advanced HCL patterns
- [references/project-scaffolding.md](project-scaffolding.md) - Directory structure, .gitignore, next_steps output, security-first variables
- [references/post-provisioning.md](post-provisioning.md) - bin/setup-server scripts for post-infra, pre-deployment setup
- [references/state-management.md](state-management.md) - State operations and encryption
- [references/provider-examples.md](provider-examples.md) - Multi-cloud provider configs
- [references/makefile-automation.md](makefile-automation.md) - Makefile workflows for plan/apply/destroy
