---
name: digitalocean-infrastructure
description: "Provision and review DigitalOcean infrastructure with OpenTofu. Use when managing Droplets, VPCs, managed databases, firewalls, reserved IPs, or cloud-init on DigitalOcean."
---

# DigitalOcean Infrastructure

Verify current regions, images, sizes, prices, quotas, and provider schemas before planning or applying changes.

## Provider Setup

```hcl
terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

provider "digitalocean" {
  # Uses DIGITALOCEAN_TOKEN env var
}
```

## VPC (Virtual Private Cloud)

```hcl
resource "digitalocean_vpc" "main" {
  name     = "${var.project}-${var.environment}-vpc"
  region   = var.region
  ip_range = "10.10.0.0/16"

  description = "VPC for ${var.project} ${var.environment}"
}
```

## Droplets (Compute)

### Basic Droplet

```hcl
resource "digitalocean_droplet" "app" {
  name     = "${var.project}-${var.environment}-app"
  region   = var.region
  size     = var.droplet_size  # s-1vcpu-1gb, s-2vcpu-4gb, etc.
  image    = "ubuntu-22-04-x64"
  vpc_uuid = digitalocean_vpc.main.id

  ssh_keys   = var.ssh_key_ids
  monitoring = true
  ipv6       = false

  tags = [var.project, var.environment]
}
```

### Droplet with Cloud-Init

```hcl
resource "digitalocean_droplet" "app" {
  name     = "${var.project}-app"
  region   = var.region
  size     = "s-1vcpu-2gb"
  image    = "ubuntu-22-04-x64"
  vpc_uuid = digitalocean_vpc.main.id

  ssh_keys   = var.ssh_key_ids
  monitoring = true

  user_data = <<-EOT
    #cloud-config
    package_update: true
    packages:
      - docker.io
      - docker-compose-plugin
    users:
      - name: deploy
        groups: docker
        sudo: ALL=(ALL) NOPASSWD:ALL
        shell: /bin/bash
        ssh_authorized_keys:
          - ${var.deploy_ssh_key}
    runcmd:
      - systemctl enable --now docker
      - sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
      - systemctl restart sshd
  EOT

  tags = [var.project]
}
```

See [references/digitalocean-sizes.md](references/digitalocean-sizes.md) for droplet and database sizes.

## Reserved IP (Static IP)

```hcl
resource "digitalocean_reserved_ip" "app" {
  region = var.region
}

resource "digitalocean_reserved_ip_assignment" "app" {
  ip_address = digitalocean_reserved_ip.app.ip_address
  droplet_id = digitalocean_droplet.app.id
}

output "app_ip" {
  value = digitalocean_reserved_ip.app.ip_address
}
```

## Firewall

### Basic Web Server Firewall

```hcl
resource "digitalocean_firewall" "web" {
  name = "${var.project}-web-firewall"

  droplet_ids = [digitalocean_droplet.app.id]

  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = var.ssh_allowed_ips
  }

  inbound_rule {
    protocol         = "tcp"
    port_range       = "80"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule {
    protocol         = "tcp"
    port_range       = "443"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "tcp"
    port_range            = "all"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "udp"
    port_range            = "all"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "icmp"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
}
```

### Dynamic IP Whitelist

```hcl
variable "db_allowed_ips" {
  type        = list(string)
  default     = []
  description = "IPs allowed to access database directly"
}

resource "digitalocean_database_firewall" "postgres" {
  cluster_id = digitalocean_database_cluster.postgres.id

  rule {
    type  = "droplet"
    value = digitalocean_droplet.app.id
  }

  dynamic "rule" {
    for_each = var.db_allowed_ips
    content {
      type  = "ip_addr"
      value = rule.value
    }
  }
}
```

## Detailed Reference

Load [detailed-reference.md](references/detailed-reference.md) for extended resource examples. Load [patterns.md](references/patterns.md) when planning or reviewing DigitalOcean changes.
