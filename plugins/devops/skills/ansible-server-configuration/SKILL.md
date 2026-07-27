---
name: ansible-server-configuration
description: "Configure and maintain servers with focused Ansible playbooks. Use when hardening hosts, installing packages, managing services, or automating repeatable post-provisioning work."
---

# Ansible Server Configuration

## ⚠️ SIMPLICITY FIRST - Default to Flat Structure

**ALWAYS start with the simplest approach. Only add complexity when explicitly requested.**

### Simple (DEFAULT) vs Overengineered

| Aspect | ✅ Simple (Default) | ❌ Overengineered |
|--------|---------------------|-------------------|
| Playbooks | 1 playbook with inline tasks | Multiple playbooks + custom roles |
| Roles | Use Galaxy roles (geerlingguy.*) | Write custom roles for simple tasks |
| Inventory | Single `hosts.ini` | Multiple inventories + group_vars hierarchy |
| Variables | Inline in playbook or single vars file | Scattered across group_vars/host_vars |
| File count | ~3-5 files total | 20+ files in nested directories |

### When to Use Simple Approach (90% of cases)

- Setting up 1-5 servers
- Standard stack (Docker, nginx, fail2ban, ufw)
- Single environment or identical servers
- No complex conditional logic per host

### When Complexity is Justified (10% of cases)

- Large fleet with divergent configurations
- Multi-team requiring role isolation
- Complex orchestration with dependencies
- User explicitly requests modular structure

**Rule: If you can fit everything in one 200-line playbook, DO IT.**

## When to Use Ansible vs Cloud-Init

| Use Cloud-Init When | Use Ansible When |
|---------------------|------------------|
| First boot only | Re-running config on existing servers |
| Simple package install | Complex multi-step configuration |
| Basic user creation | Role-based configuration |
| Immutable infrastructure | Mutable servers needing updates |

**Rule of thumb:** Cloud-init for initial provisioning, Ansible for ongoing management.

## Directory Structure

### Simple Structure (DEFAULT)

```
infra/ansible/
├── playbook.yml          # Single playbook with all tasks inline
├── requirements.yml      # Galaxy dependencies (geerlingguy.*, etc.)
├── hosts.ini             # Inventory (git-ignored)
└── hosts.ini.example     # Inventory template
```

### Complex Structure (only when justified)

```
infra/ansible/
├── playbook.yml          # Main playbook
├── requirements.yml      # Galaxy dependencies
├── hosts.ini             # Inventory (git-ignored)
├── hosts.ini.example     # Inventory template
├── group_vars/
│   └── all.yml           # Shared variables
└── roles/
    └── custom_role/
        ├── tasks/main.yml
        ├── handlers/main.yml
        └── templates/
```

## Inventory

### Static Inventory

```ini
# hosts.ini
[web]
192.168.1.1 ansible_user=root

[db]
192.168.1.2 ansible_user=root

[all:vars]
ansible_python_interpreter=/usr/bin/python3
```

### Dynamic from Terraform

```bash
# Generate inventory from Terraform output
SERVER_IP=$(cd infra && tofu output -raw server_ip)
cat > infra/ansible/hosts.ini << EOF
[web]
$SERVER_IP ansible_user=root
EOF
```

## Playbook Structure

### Basic Playbook

```yaml
---
- name: Configure web servers
  hosts: web
  become: true

  vars:
    timezone: "UTC"
    swap_size_mb: "2048"

  tasks:
    - name: Update apt cache
      ansible.builtin.apt:
        update_cache: true
        cache_valid_time: 3600

    - name: Install packages
      ansible.builtin.apt:
        name:
          - docker.io
          - fail2ban
          - ufw
        state: present
```

### With Roles

```yaml
---
- name: Configure web servers
  hosts: web
  become: true

  vars:
    security_autoupdate_reboot: true
    security_autoupdate_reboot_time: "03:00"

  roles:
    - role: geerlingguy.swap
      when: ansible_swaptotal_mb < 1
    - role: geerlingguy.docker
    - role: security
```

## Detailed Reference

Load [restored-examples.md](references/restored-examples.md) for additional playbook templates and advanced patterns.
