---
name: kamal-deploy
description: "Deploy and operate Rails applications with Kamal 2. Use when configuring deploy.yml, kamal-proxy, registries, secrets, accessories, server preparation, or container deployment troubleshooting."
---

# Kamal Deploy

Servers need Docker, SSH access, and ports 22/80/443 open. Provision with Ansible or cloud-init.

## Configuration: config/deploy.yml

### Minimal Setup

```yaml
service: myapp
image: myapp

servers:
  web:
    - 203.0.113.10

proxy:
  ssl: true
  host: myapp.com

registry:
  username: username
  password:
    - KAMAL_REGISTRY_PASSWORD

env:
  clear:
    RAILS_ENV: production
    RAILS_LOG_TO_STDOUT: "true"
  secret:
    - RAILS_MASTER_KEY
```

### Multi-Role Setup (Web + Job Worker)

```yaml
service: myapp
image: myapp

servers:
  web:
    - 203.0.113.10
  job:
    hosts:
      - 203.0.113.10
    cmd: bin/jobs start

proxy:
  ssl: true
  host: myapp.com

registry:
  username: username
  password:
    - KAMAL_REGISTRY_PASSWORD

env:
  clear:
    RAILS_ENV: production
    SOLID_QUEUE_IN_PUMA: false
  secret:
    - RAILS_MASTER_KEY
```

**Job worker notes:**
- `cmd: bin/jobs start` runs Solid Queue in a separate container
- Set `SOLID_QUEUE_IN_PUMA: false` to disable in-process queue
- Job role has no proxy — only web role serves HTTP traffic

### With Local Registry

Eliminates Docker Hub dependency, rate limits, and external costs:

```yaml
registry:
  server: localhost:5555
  username: ignored
  password:
    - KAMAL_REGISTRY_PASSWORD
```

Deploy the registry as an accessory:

```yaml
accessories:
  registry:
    image: registry:2
    host: 203.0.113.10
    port: "5555:5000"
    volumes:
      - registry_data:/var/lib/registry
```

### With Accessories

```yaml
accessories:
  db:
    image: postgres:16
    host: 203.0.113.10
    port: 5432
    env:
      clear:
        POSTGRES_DB: myapp_production
      secret:
        - POSTGRES_PASSWORD
    directories:
      - data:/var/lib/postgresql/data
    options:
      shm-size: 256m

  redis:
    image: redis:7-alpine
    host: 203.0.113.10
    port: 6379
    directories:
      - data:/data
    cmd: redis-server --appendonly yes
```

### Docker Volumes for Persistence

For SQLite + ActiveStorage apps, mount a named volume:

```yaml
servers:
  web:
    hosts:
      - 203.0.113.10
    volumes:
      - myapp_storage:/rails/storage
    labels:
      docker-volume-backup.stop-during-backup: "true"
  job:
    hosts:
      - 203.0.113.10
    cmd: bin/jobs start
    volumes:
      - myapp_storage:/rails/storage
```

Both web and job containers share the same volume for database access.

## Proxy Configuration (kamal-proxy)

Kamal 2 uses kamal-proxy (not Traefik). It handles SSL termination, routing, and zero-downtime deploys.

### Basic SSL

```yaml
proxy:
  ssl: true
  host: myapp.com
```

Automatic Let's Encrypt certificate provisioning — no manual cert management.

### Custom Port

```yaml
proxy:
  ssl: true
  host: myapp.com
  app_port: 3000
```

### Multiple Hosts

```yaml
proxy:
  ssl: true
  hosts:
    - myapp.com
    - www.myapp.com
```

### Health Check

```yaml
proxy:
  ssl: true
  host: myapp.com
  healthcheck:
    path: /up
    interval: 3
    timeout: 3
```

### Response Timeout

```yaml
proxy:
  ssl: true
  host: myapp.com
  response_timeout: 30
```

## Detailed Reference

Load [detailed-reference.md](references/detailed-reference.md) for extended examples, templates, and advanced patterns.
