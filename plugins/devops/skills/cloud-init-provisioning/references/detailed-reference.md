# Cloud-Init Provisioning Detailed Reference

## Service Configuration

### Enable and Start Services

```yaml
#cloud-config
runcmd:
  - systemctl enable --now docker
  - systemctl enable --now nginx
  - systemctl enable --now fail2ban
```

### Systemd Service Creation

```yaml
#cloud-config
write_files:
  - path: /etc/systemd/system/myapp.service
    owner: root:root
    permissions: "0644"
    content: |
      [Unit]
      Description=My Application
      After=network.target docker.service
      Requires=docker.service

      [Service]
      Type=simple
      User=deploy
      WorkingDirectory=/opt/app
      ExecStart=/usr/bin/docker compose up
      ExecStop=/usr/bin/docker compose down
      Restart=always
      RestartSec=10

      [Install]
      WantedBy=multi-user.target

runcmd:
  - systemctl daemon-reload
  - systemctl enable --now myapp
```

## Firewall Configuration

### UFW Setup

```yaml
#cloud-config
packages:
  - ufw

runcmd:
  - ufw default deny incoming
  - ufw default allow outgoing
  - ufw allow ssh
  - ufw allow http
  - ufw allow https
  - ufw --force enable
```

### SSH Fail2Ban Jail

Use Fail2Ban as a second layer after SSH key authentication, root-login restrictions, and a firewall. It reacts to repeated authentication failures by blocking the source IP through the host firewall.

Prefer a minimal override file instead of copying the full stock `jail.conf`. Stock `.conf` files should stay upgradeable, and local overrides should contain only the settings you mean to change.

```yaml
#cloud-config
packages:
  - fail2ban

write_files:
  - path: /etc/fail2ban/jail.d/sshd.local
    owner: root:root
    permissions: "0644"
    content: |
      [sshd]
      enabled = true
      port = ssh
      filter = sshd
      maxretry = 5
      findtime = 10m
      bantime = 10m
      # Optional for noisier hosts. Test before enabling broadly.
      # mode = aggressive

runcmd:
  - systemctl enable --now fail2ban
  - fail2ban-client status
  - fail2ban-client status sshd
```

## Terraform/OpenTofu Integration

### Inline User Data

```hcl
resource "digitalocean_droplet" "app" {
  name   = "app-server"
  image  = "ubuntu-22-04-x64"
  size   = "s-1vcpu-1gb"
  region = "nyc1"

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
  EOT
}
```

### Template File

```yaml
# templates/cloud-init.yaml
#cloud-config
package_update: true
packages:
  - docker.io
users:
  - name: ${username}
    groups: docker
    ssh_authorized_keys:
      - ${ssh_key}
```

```hcl
resource "digitalocean_droplet" "app" {
  user_data = templatefile("${path.module}/templates/cloud-init.yaml", {
    username = var.deploy_user
    ssh_key  = var.deploy_ssh_key
  })
}
```

## Complete Production Example

```yaml
#cloud-config
package_update: true
package_upgrade: true

packages:
  - docker.io
  - docker-compose-plugin
  - fail2ban
  - ufw
  - unattended-upgrades

groups:
  - docker

users:
  - name: deploy
    groups: docker, sudo
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
    ssh_authorized_keys:
      - ssh-ed25519 AAAA... deploy-key

write_files:
  - path: /etc/docker/daemon.json
    owner: root:root
    permissions: "0644"
    content: |
      {
        "log-driver": "json-file",
        "log-opts": {
          "max-size": "10m",
          "max-file": "3"
        }
      }

  - path: /etc/fail2ban/jail.d/sshd.local
    owner: root:root
    permissions: "0644"
    content: |
      [sshd]
      enabled = true
      port = ssh
      filter = sshd
      maxretry = 5
      findtime = 10m
      bantime = 10m

runcmd:
  - systemctl enable --now docker
  - sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
  - sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
  - sed -i 's/^#\?ClientAliveInterval.*/ClientAliveInterval 60/' /etc/ssh/sshd_config
  - sed -i 's/^#\?ClientAliveCountMax.*/ClientAliveCountMax 10/' /etc/ssh/sshd_config
  - systemctl restart sshd
  - ufw default deny incoming
  - ufw default allow outgoing
  - ufw allow ssh
  - ufw allow http
  - ufw allow https
  - ufw --force enable
  - systemctl enable --now fail2ban
  - fail2ban-client status sshd
  - systemctl enable --now unattended-upgrades

final_message: "Cloud-init completed after $UPTIME seconds"
```

## Server Tuning

### Performance and Cleanup

```yaml
#cloud-config
runcmd:
  - |
    if ! grep -q "vm.swappiness=10" /etc/sysctl.conf; then
      echo "vm.swappiness=10" >> /etc/sysctl.conf
      sysctl -p
    fi
  - timedatectl set-timezone UTC
  - apt-get autoremove -y
  - apt-get clean
```

### Swappiness Values

| Value | Behavior |
|-------|----------|
| `0` | Only swap to avoid out-of-memory failures |
| `10` | Minimal swapping, recommended for many app hosts |
| `60` | Default Ubuntu behavior |
| `100` | Aggressive swapping |

## Debugging

### Check Cloud-Init Status

```bash
cloud-init status
cat /var/log/cloud-init.log
cat /var/log/cloud-init-output.log
```

### Re-Run Cloud-Init for Testing

```bash
sudo cloud-init clean
sudo cloud-init init
```

### Verify Host Hardening

```bash
sudo systemctl status fail2ban
sudo fail2ban-client status
sudo fail2ban-client status sshd
sudo ufw status verbose
sudo sshd -T | grep -E '^(passwordauthentication|permitrootlogin|clientalive)'
```

### Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| YAML parse error | Indentation wrong | Use 2-space indentation and validate YAML before provisioning |
| User not created | Missing root-level `users:` key | Ensure `users:` is at the root of the cloud-config document |
| Packages not installed | Package index not refreshed | Set `package_update: true` |
| SSH key rejected | Wrong key format | Use the full public key string |
| Service not starting | Missing systemd dependency or reload | Use `After=`, run `systemctl daemon-reload`, then enable the service |
| Fail2Ban jail inactive | Override file not loaded or service not restarted | Check `fail2ban-client status` and restart Fail2Ban after config changes |
