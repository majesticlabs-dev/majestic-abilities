# Integration with Terraform

## Provision Script Pattern

```bash
#!/usr/bin/env bash
# infra/bin/provision
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$repo_root/infra"

# 1. OpenTofu creates the server from a reviewed plan
tofu plan -out=tfplan
tofu show tfplan
read -r -p "Apply this reviewed plan? [y/N] " reply
case "$reply" in y|Y|yes|YES) ;; *) echo "Apply cancelled"; exit 1 ;; esac
tofu apply tfplan
SERVER_IP="$(tofu output -raw server_ip)"

case "$SERVER_IP" in
  ""|*[!0-9A-Fa-f:.]*)
    echo "Invalid server IP from Terraform output: $SERVER_IP" >&2
    exit 1
    ;;
esac

# 2. Wait for SSH for at most five minutes
deadline=$((SECONDS + 300))
until ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=accept-new "root@${SERVER_IP}" true 2>/dev/null; do
  if (( SECONDS >= deadline )); then
    echo "Timed out waiting for SSH on ${SERVER_IP}" >&2
    exit 1
  fi
  sleep 5
done

# 3. Generate inventory
printf "[web]\n%s ansible_user=root\n" "$SERVER_IP" > ansible/hosts.ini

# 4. Run Ansible
cd ansible
ansible-galaxy install -r requirements.yml
ANSIBLE_SSH_ARGS="-o StrictHostKeyChecking=accept-new -o UserKnownHostsFile=./known_hosts" \
  ansible-playbook -i hosts.ini playbook.yml

# 5. Kamal bootstrap
cd "$repo_root"
bundle exec kamal server bootstrap
```
