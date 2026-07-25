# Hetzner Patterns

Use this reference when infrastructure changes target Hetzner Cloud.

## Scope

- compute
- private networking
- firewalls
- floating IPs
- load balancers
- volumes

## Planning Notes

- Keep labels and network topology explicit so fleet operations stay readable.
- Prefer private networks for east-west traffic and restrictive firewall rules for ingress.
- Keep bootstrap steps small; push long-lived host config to Ansible or similar.
- Verify replacement risk, region availability, and public exposure before apply.

## Review Checks

- Never default SSH access to the world.
- Keep public and private interface assumptions visible in code.
- Use floating IPs and load balancers intentionally, not as accidental overlap.
- If the design depends on post-provisioning steps, document that dependency explicitly.
