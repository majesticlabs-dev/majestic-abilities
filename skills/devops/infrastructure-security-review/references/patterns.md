# Infrastructure Security Patterns

## State

- backend is encrypted
- locking exists where the tool supports it
- public access to state storage is blocked

## Secrets

- no hardcoded keys or passwords
- variables do not ship dangerous defaults
- secret loading path is explicit and auditable

## Network

- admin ports are not open to the world
- databases stay on private networks where possible
- firewall and ingress rules are narrow and named clearly

## Hosts And Services

- no root login by default
- password auth disabled unless explicitly required
- monitoring, backups, and patch posture are defined for production systems
