# DigitalOcean Patterns

Use this reference when infrastructure changes target DigitalOcean.

## Scope

- droplets
- VPC and private networking
- firewalls
- managed databases
- spaces and object storage
- DNS and reserved IPs

## Planning Notes

- Keep provider resources grouped by concern so network and app-server changes stay reviewable.
- Prefer private networking and explicit firewall rules over broad public exposure.
- Keep cloud-init small and predictable; move long-lived host config to Ansible or similar.
- Verify region, size, cost, and dependency changes before apply.

## Review Checks

- Avoid opening SSH or database access broadly when a narrow CIDR or private path exists.
- Do not hide reserved IP, DNS, and application rollout assumptions inside one opaque step.
- Use managed databases when self-hosting does not buy enough control to justify the burden.
- Call out cost, quota, or availability changes explicitly.
