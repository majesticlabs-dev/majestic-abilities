---
name: cloud-init-provisioning
description: "Provision virtual machines with small, testable cloud-init configurations. Use when creating user data, bootstrapping users and packages, hardening SSH, or handing first-boot configuration to later automation."
---

# Cloud-Init Provisioning

Examples assume an Ubuntu or Debian host unless stated otherwise. Adapt package managers, service names, and SSH paths for the selected image.

## Overview

Cloud-init is the industry standard for cross-platform cloud instance initialization. It runs on first boot to configure users, packages, files, and services before the instance becomes available.

## Core Format

Cloud-init configs start with `#cloud-config`:

```yaml
#cloud-config
package_update: true
packages:
  - nginx
  - docker.io
```

## User Management

### Create Deploy User

```yaml
#cloud-config
users:
  - name: deploy
    groups: docker, sudo
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
    ssh_authorized_keys:
      - ssh-ed25519 AAAA... deploy@example.com
```

### Multiple Users

```yaml
#cloud-config
users:
  - default  # Keep cloud provider's default user
  - name: deploy
    groups: docker
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
    ssh_authorized_keys:
      - ssh-ed25519 AAAA... key1
  - name: monitoring
    groups: adm
    shell: /bin/bash
    ssh_authorized_keys:
      - ssh-ed25519 AAAA... monitoring-key
```

## Package Installation

### Basic Packages

```yaml
#cloud-config
package_update: true
package_upgrade: true
packages:
  - docker.io
  - docker-compose-plugin
  - nginx
  - certbot
  - python3-certbot-nginx
  - fail2ban
  - ufw
```

### From Custom Repositories

```yaml
#cloud-config
apt:
  sources:
    docker:
      source: "deb [arch=amd64] https://download.docker.com/linux/ubuntu $RELEASE stable"
      keyid: 9DC858229FC7DD38854AE2D88D81803C0EBFCD88

packages:
  - docker-ce
  - docker-ce-cli
  - containerd.io
```

## SSH Hardening

### Declarative SSH Lockdown

Prefer declarative `ssh_pwauth: false` over runcmd sed commands:

```yaml
#cloud-config
ssh_pwauth: false  # Disable password auth at cloud-init level

runcmd:
  # Additional hardening via sshd_config
  - sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin prohibit-password/' /etc/ssh/sshd_config
  - systemctl restart sshd
```

### Full SSH Hardening

```yaml
#cloud-config
ssh_pwauth: false  # Declarative - cleaner than sed

runcmd:
  # Disable root login (or use prohibit-password for key-only root)
  - sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
  - sed -i 's/^PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config

  # Disable password authentication (backup for ssh_pwauth)
  - sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config

  # Increase keepalive for stable connections
  - sed -i 's/^#\?ClientAliveInterval.*/ClientAliveInterval 60/' /etc/ssh/sshd_config
  - sed -i 's/^#\?ClientAliveCountMax.*/ClientAliveCountMax 10/' /etc/ssh/sshd_config

  # Restart SSH
  - systemctl restart sshd
```

## Docker Setup

### Docker with Compose

```yaml
#cloud-config
package_update: true
packages:
  - docker.io
  - docker-compose-plugin

groups:
  - docker

users:
  - name: deploy
    groups: docker
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
    ssh_authorized_keys:
      - ssh-ed25519 AAAA...

runcmd:
  - systemctl enable --now docker
  - usermod -aG docker deploy
```

### Docker with Custom Daemon Config

```yaml
#cloud-config
write_files:
  - path: /etc/docker/daemon.json
    content: |
      {
        "log-driver": "json-file",
        "log-opts": {
          "max-size": "10m",
          "max-file": "3"
        },
        "storage-driver": "overlay2"
      }

runcmd:
  - systemctl enable --now docker
```

## File Creation

### Write Configuration Files

```yaml
#cloud-config
write_files:
  - path: /etc/nginx/sites-available/app
    content: |
      server {
          listen 80;
          server_name example.com;
          location / {
              proxy_pass http://127.0.0.1:3000;
              proxy_set_header Host $host;
              proxy_set_header X-Real-IP $remote_addr;
          }
      }
    owner: root:root
    permissions: '0644'

  - path: /opt/app/.env
    content: |
      RAILS_ENV=production
      PORT=3000
    owner: deploy:deploy
    permissions: '0600'
```

### Verify Downloaded Scripts

Pin remote scripts to an immutable release or commit and verify a project-owned checksum before executing them as root. Replace the example URL and checksum with reviewed real values:

```yaml
#cloud-config
runcmd:
  - |
    set -eu
    curl -fsSL https://example.com/releases/v1.2.3/setup.sh -o /opt/setup.sh
    echo '<EXPECTED_SHA256>  /opt/setup.sh' | sha256sum -c -
    chmod 0755 /opt/setup.sh
    /opt/setup.sh
```

## Detailed Reference

Load [detailed-reference.md](references/detailed-reference.md) for extended examples, templates, and advanced patterns.
