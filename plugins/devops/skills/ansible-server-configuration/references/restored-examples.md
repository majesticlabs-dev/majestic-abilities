# Ansible Server Configuration Detailed Reference

## Common Tasks

### Package Management

```yaml
- name: Install required packages
  ansible.builtin.apt:
    name:
      - curl
      - ca-certificates
      - gnupg
      - fail2ban
      - ufw
      - ntp
    state: present
    update_cache: true
```

### Docker Installation

```yaml
- name: Check if Docker is installed
  ansible.builtin.command: docker --version
  register: docker_installed
  ignore_errors: true
  changed_when: false

- name: Install Docker from the distribution package repository
  ansible.builtin.apt:
    name: docker.io
    state: present
    update_cache: true
  when: docker_installed.rc != 0

- name: Ensure Docker is running
  ansible.builtin.systemd:
    name: docker
    state: started
    enabled: true
```

### SSH Hardening

```yaml
- name: Disable SSH password authentication
  ansible.builtin.lineinfile:
    path: /etc/ssh/sshd_config
    regexp: "^#?PasswordAuthentication"
    line: "PasswordAuthentication no"
  notify: Restart ssh

- name: Disable SSH root login with password
  ansible.builtin.lineinfile:
    path: /etc/ssh/sshd_config
    regexp: "^#?PermitRootLogin"
    line: "PermitRootLogin prohibit-password"
  notify: Restart ssh

handlers:
  - name: Restart ssh
    ansible.builtin.systemd:
      name: ssh  # Ubuntu uses 'ssh', not 'sshd'
      state: restarted
```

### Fail2ban

```yaml
- name: Configure fail2ban for SSH
  ansible.builtin.copy:
    dest: /etc/fail2ban/jail.local
    content: |
      [sshd]
      enabled = true
      port = ssh
      filter = sshd
      logpath = /var/log/auth.log
      maxretry = 5
      bantime = 3600
      findtime = 600
    mode: "0644"
  notify: Restart fail2ban

- name: Ensure fail2ban is running
  ansible.builtin.systemd:
    name: fail2ban
    state: started
    enabled: true

handlers:
  - name: Restart fail2ban
    ansible.builtin.systemd:
      name: fail2ban
      state: restarted
```

### UFW Firewall

```yaml
- name: Set UFW default policies
  community.general.ufw:
    direction: "{{ item.direction }}"
    policy: "{{ item.policy }}"
  loop:
    - { direction: incoming, policy: deny }
    - { direction: outgoing, policy: allow }

- name: Allow specified ports through UFW
  community.general.ufw:
    rule: allow
    port: "{{ item }}"
    proto: tcp
  loop:
    - 22   # SSH
    - 80   # HTTP
    - 443  # HTTPS

- name: Enable UFW
  community.general.ufw:
    state: enabled
```

### Kernel Tuning

```yaml
- name: Configure sysctl for performance
  ansible.posix.sysctl:
    name: "{{ item.name }}"
    value: "{{ item.value }}"
    state: present
    reload: true
  loop:
    - { name: vm.swappiness, value: "10" }
    - { name: net.core.somaxconn, value: "65535" }
```

### Timezone

```yaml
- name: Set timezone
  community.general.timezone:
    name: "{{ timezone }}"
```

### Remove Snap (Ubuntu bloat)

```yaml
- name: Remove snapd
  ansible.builtin.apt:
    name: snapd
    state: absent
    purge: true
  ignore_errors: true

- name: Remove snap directories
  ansible.builtin.file:
    path: "{{ item }}"
    state: absent
  loop:
    - /snap
    - /var/snap
    - /var/lib/snapd
```

## Galaxy Dependencies

### requirements.yml

```yaml
---
roles:
  - name: geerlingguy.swap
    version: 2.0.0
  - name: geerlingguy.docker
    version: 7.4.1

collections:
  - name: community.general
  - name: ansible.posix
```

### Installation

```bash
ansible-galaxy install -r requirements.yml --force
```

## Running Playbooks

### Basic Execution

```bash
ansible-playbook -i hosts.ini playbook.yml
```

### With Variables

```bash
ansible-playbook -i hosts.ini playbook.yml \
  -e "timezone=Europe/Berlin" \
  -e "swap_size_mb=4096"
```

### Dry Run

```bash
ansible-playbook -i hosts.ini playbook.yml --check --diff
```

### Limit to Specific Hosts

```bash
ansible-playbook -i hosts.ini playbook.yml --limit web
```

See [Kamal Server Preparation](kamal-playbook.md) for a complete Kamal deployment server playbook.

See [Integration with Terraform](provision-script.md) for the Terraform-Ansible-Kamal provisioning pipeline.

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `ssh: connect refused` | Server not ready | Wait or check firewall |
| `Permission denied` | Wrong SSH key | Specify with `-i` |
| `sudo: password required` | User needs NOPASSWD | Use `become_method: sudo` |
| Handler not running | Task didn't change | Use `changed_when: true` |
| Module not found | Missing collection | Install from requirements.yml |
