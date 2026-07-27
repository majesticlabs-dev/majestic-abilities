---
name: hetzner-infrastructure
description: "Provision and review Hetzner Cloud infrastructure with OpenTofu. Use when managing servers, private networks, firewalls, load balancers, volumes, object storage, or Storage Boxes."
---

# Hetzner Infrastructure

Verify current locations, server types, prices, quotas, and provider schemas before planning or applying changes.

## Provider Setup

```hcl
terraform {
  required_providers {
    hcloud = {
      source  = "hetznercloud/hcloud"
      version = "~> 1.50"
    }
  }
}

provider "hcloud" {
  # Uses HCLOUD_TOKEN env var
}
```

### Authentication

```bash
export HCLOUD_TOKEN="your-api-token"
# Or load the token from 1Password
export HCLOUD_TOKEN="$(op read 'op://Infrastructure/Hetzner/api_token')"
```

## Locations

| Code | Region | Network Zone |
|------|--------|--------------|
| `fsn1` | Germany | `eu-central` |
| `nbg1` | Germany | `eu-central` |
| `hel1` | Finland | `eu-central` |
| `ash` | US East | `us-east` |
| `hil` | US West | `us-west` |

See [references/hetzner-server-types.md](references/hetzner-server-types.md) for all server types (CX, CPX, CAX, CCX).

## Servers (Compute)

### Basic Server

```hcl
resource "hcloud_server" "app" {
  name        = "${var.project}-${var.environment}-app"
  server_type = "cx22"
  image       = "ubuntu-24.04"
  location    = "fsn1"

  ssh_keys = [hcloud_ssh_key.deploy.id]

  labels = {
    environment = var.environment
    project     = var.project
    role        = "web"
  }

  public_net {
    ipv4_enabled = true
    ipv6_enabled = true
  }
}
```

### Server with Cloud-Init

```hcl
resource "hcloud_server" "app" {
  name        = "${var.project}-app"
  server_type = "cx22"
  image       = "ubuntu-24.04"
  location    = "fsn1"

  ssh_keys = [hcloud_ssh_key.deploy.id]

  user_data = <<-EOT
    #cloud-config
    package_update: true
    packages:
      - docker.io
      - docker-compose-plugin

    users:
      - name: deploy
        groups: docker, sudo
        sudo: ALL=(ALL) NOPASSWD:ALL
        shell: /bin/bash
        ssh_authorized_keys:
          - ${var.deploy_ssh_key}

    runcmd:
      - systemctl enable --now docker
      - sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
      - sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
      - systemctl restart sshd
  EOT

  labels = {
    environment = var.environment
    role        = "web"
  }
}
```

## Private Networks

### Network with Subnet

```hcl
resource "hcloud_network" "private" {
  name     = "${var.project}-network"
  ip_range = "10.0.0.0/16"

  labels = {
    project = var.project
  }
}

resource "hcloud_network_subnet" "private" {
  network_id   = hcloud_network.private.id
  type         = "cloud"
  network_zone = "eu-central"
  ip_range     = "10.0.1.0/24"
}
```

### Server in Private Network

```hcl
resource "hcloud_server" "db" {
  name        = "${var.project}-db"
  server_type = "cpx31"
  image       = "ubuntu-24.04"
  location    = "fsn1"

  ssh_keys = [hcloud_ssh_key.deploy.id]

  network {
    network_id = hcloud_network.private.id
    ip         = "10.0.1.10"
  }

  public_net {
    ipv4_enabled = false
    ipv6_enabled = false
  }

  labels = {
    role = "database"
  }

  depends_on = [hcloud_network_subnet.private]
}
```

## Firewalls

Never default SSH to `0.0.0.0/0`. Resolve and validate the admin IP, using `/32` for IPv4 and `/128` for IPv6, before passing it to OpenTofu:

```bash
ADMIN_CIDR="$(python3 - <<'PY'
import ipaddress
import urllib.request

raw = urllib.request.urlopen("https://api64.ipify.org", timeout=10).read().decode().strip()
ip = ipaddress.ip_address(raw)
print(f"{ip}/{32 if ip.version == 4 else 128}")
PY
)"
tofu plan -var="admin_ip=${ADMIN_CIDR}" -out=tfplan
tofu show tfplan
read -r -p "Apply this reviewed plan? [y/N] " reply
case "$reply" in y|Y|yes|YES) ;; *) echo "Apply cancelled"; exit 1 ;; esac
tofu apply tfplan
```

### Web Server Firewall

```hcl
resource "hcloud_firewall" "web" {
  name = "${var.project}-web-firewall"

  rule {
    description = "SSH"
    direction   = "in"
    protocol    = "tcp"
    port        = "22"
    source_ips  = [var.admin_ip]
  }

  rule {
    description = "HTTP"
    direction   = "in"
    protocol    = "tcp"
    port        = "80"
    source_ips  = ["0.0.0.0/0", "::/0"]
  }

  rule {
    description = "HTTPS"
    direction   = "in"
    protocol    = "tcp"
    port        = "443"
    source_ips  = ["0.0.0.0/0", "::/0"]
  }

  apply_to {
    label_selector = "role=web"
  }
}

variable "admin_ip" {
  description = "Admin IP for SSH access (CIDR)"
  type        = string
}
```

### Protect Private-Network Databases

Hetzner Cloud Firewalls do not filter traffic over private Cloud Networks. Do not rely on an `hcloud_firewall` resource to restrict database traffic between private-network peers.

Instead:

- disable the database server's public interfaces
- bind the database to its private address
- enforce host-level firewall rules with Ansible or cloud-init
- restrict database authentication rules to the required application addresses
- separate trust zones into distinct private networks when stronger isolation is required

## Detailed Reference

Load [detailed-reference.md](references/detailed-reference.md) for extended resource examples. Load [patterns.md](references/patterns.md) when planning or reviewing Hetzner changes.
