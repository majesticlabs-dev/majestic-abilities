# Ansible Integration for Hetzner

## Post-Provisioning with Ansible

Cloud-init runs at first boot. For ongoing configuration or re-running setup, use Ansible.

```hcl
# outputs.tf
output "server_ip" {
  value       = hcloud_server.app.ipv4_address
  description = "Server IP for Ansible inventory"
}

output "ansible_inventory" {
  value = <<-EOT
    [web]
    ${hcloud_server.app.ipv4_address} ansible_user=root
  EOT
  description = "Ansible inventory content"
}
```

## Provision Script (Terraform > Ansible > Kamal)

```bash
#!/usr/bin/env bash
# infra/bin/provision
set -euo pipefail

INFRA_DIR="$(dirname "$0")/.."

# 1. OpenTofu
cd "$INFRA_DIR"
tofu plan -out=tfplan
tofu show tfplan
read -r -p "Apply this reviewed plan? [y/N] " reply
case "$reply" in y|Y|yes|YES) ;; *) echo "Apply cancelled"; exit 1 ;; esac
tofu apply tfplan

# 2. Wait for SSH
SERVER_IP="$(tofu output -raw server_ip)"
case "$SERVER_IP" in
  ""|*[!0-9A-Fa-f:.]*)
    echo "Invalid server IP from Terraform output: $SERVER_IP" >&2
    exit 1
    ;;
esac

deadline=$((SECONDS + 300))
until ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=accept-new "root@${SERVER_IP}" true 2>/dev/null; do
  if (( SECONDS >= deadline )); then
    echo "Timed out waiting for SSH on ${SERVER_IP}" >&2
    exit 1
  fi
  echo "Waiting for server..."
  sleep 5
done

# 3. Ansible
tofu output -raw ansible_inventory > ansible/hosts.ini
cd ansible
ansible-galaxy install -r requirements.yml --force
ANSIBLE_SSH_ARGS="-o StrictHostKeyChecking=accept-new -o UserKnownHostsFile=./known_hosts" \
  ansible-playbook -i hosts.ini playbook.yml

# 4. Kamal bootstrap
cd ../..
bundle exec kamal server bootstrap
```

## Kamal-Ready Server Playbook

Based on [kamal-ansible-manager](https://github.com/guillaumebriday/kamal-ansible-manager):

```yaml
# infra/ansible/playbook.yml
---
- name: Configure Hetzner server for Kamal
  hosts: web
  become: true

  vars:
    swap_file_size_mb: "2048"
    timezone: "UTC"

  roles:
    - role: geerlingguy.swap
      when: ansible_swaptotal_mb < 1

  tasks:
    - name: Install Docker
      ansible.builtin.apt:
        name: docker.io
        state: present
        update_cache: true

    - name: Enable Docker
      ansible.builtin.systemd:
        name: docker
        state: started
        enabled: true

    - name: Install security packages
      ansible.builtin.apt:
        name: [fail2ban, ufw]
        state: present
        update_cache: true

    - name: Configure fail2ban
      ansible.builtin.copy:
        dest: /etc/fail2ban/jail.local
        content: |
          [sshd]
          enabled = true
          maxretry = 5
          bantime = 3600
        mode: "0644"

    - name: Configure UFW
      community.general.ufw:
        rule: allow
        port: "{{ item }}"
        proto: tcp
      loop: [22, 80, 443]

    - name: Enable UFW
      community.general.ufw:
        state: enabled
        policy: deny
        direction: incoming

    - name: Harden SSH
      ansible.builtin.lineinfile:
        path: /etc/ssh/sshd_config
        regexp: "^#?PasswordAuthentication"
        line: "PasswordAuthentication no"
      notify: Restart ssh

  handlers:
    - name: Restart ssh
      ansible.builtin.systemd:
        name: ssh
        state: restarted
```

## Requirements

```yaml
# infra/ansible/requirements.yml
---
roles:
  - name: geerlingguy.swap
    version: 2.0.0
collections:
  - name: community.general
```

## When to Use Each Approach

| Approach | Use Case |
|----------|----------|
| Cloud-init only | Immutable infra, destroy/recreate pattern |
| Ansible only | Existing servers, complex multi-step config |
| Cloud-init + Ansible | First boot basics, then Ansible for hardening |
