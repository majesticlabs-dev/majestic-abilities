# Infrastructure Discovery

## Files To Look For

- Terraform/OpenTofu: `*.tf`, `*.tfvars`, `.terraform.lock.hcl`
- Terragrunt: `terragrunt.hcl`
- Ansible: `ansible.cfg`, `playbook.yml`, `playbooks/`, `roles/`
- cloud-init: `cloud-init*.yml`, `user-data*.yml`, `cloud-config*.yml`
- deployment helpers: `Makefile`, `Taskfile.yml`, `wrangler.jsonc`, `wrangler.toml`, `docker-compose*.yml`

## Signals To Extract

- providers and regions
- environments or workspaces
- state backend location
- secret sources
- rollout commands
- existing modules or shared stacks
