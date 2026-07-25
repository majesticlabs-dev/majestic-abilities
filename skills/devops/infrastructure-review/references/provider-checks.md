# Provider Review Checks

Use only the sections matching the detected providers. Verify exact resource semantics against current provider documentation.

## DigitalOcean

- Droplets and managed databases use intentional regions, sizes, and VPC placement.
- Firewalls attach to every intended resource and keep administrative ingress narrow.
- Reserved IP and DNS rollout assumptions are explicit.
- Spaces, backups, monitoring, and replacement behavior match production requirements.

## Hetzner Cloud

- Public and private network interfaces are intentional.
- Firewalls attach through explicit server IDs or reviewed label selectors.
- Location, network-zone, architecture, and server-type choices are compatible.
- Volumes, load balancers, floating IPs, and placement groups have clear lifecycle ownership.

## Cloudflare

- API tokens are scoped to the required account, zones, and permissions.
- Existing DNS and ruleset resources are imported rather than recreated accidentally.
- `Full (strict)` is used when the origin certificate is valid; weaker modes are justified and temporary.
- WAF, redirect, and cache rules preserve intended ordering and plan availability.

## AWS and Other Clouds

- Production workloads do not rely on permissive default networks.
- Identity uses roles or workload identities instead of static access keys where supported.
- Data services have encryption, recovery, and private-access controls appropriate to their classification.
- Audit logging and destructive lifecycle behavior are explicit.

## Cross-Provider

- Remote state is protected and concurrent writes are controlled where supported.
- Internal services are private by default.
- Administrative access is narrow and attributable.
- Resource replacement, quota, cost, and regional availability risks are documented.
