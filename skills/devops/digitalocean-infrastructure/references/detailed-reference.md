# DigitalOcean Infrastructure Detailed Reference

## Managed Database

### PostgreSQL Cluster

```hcl
resource "digitalocean_database_cluster" "postgres" {
  name       = "${var.project}-${var.environment}-pg"
  engine     = "pg"
  version    = "16"
  size       = var.db_size  # db-s-1vcpu-1gb, db-s-2vcpu-4gb
  region     = var.region
  node_count = 1  # Increase for HA

  private_network_uuid = digitalocean_vpc.main.id

  tags = [var.project, var.environment]
}

resource "digitalocean_database_firewall" "postgres" {
  cluster_id = digitalocean_database_cluster.postgres.id

  rule {
    type  = "droplet"
    value = digitalocean_droplet.app.id
  }
}

output "database_uri" {
  value     = digitalocean_database_cluster.postgres.uri
  sensitive = true
}

output "database_private_uri" {
  value     = digitalocean_database_cluster.postgres.private_uri
  sensitive = true
}
```

### Valkey Cluster

```hcl
resource "digitalocean_database_cluster" "valkey" {
  name       = "${var.project}-${var.environment}-valkey"
  engine     = "valkey"
  version    = "7"
  size       = "db-s-1vcpu-1gb"
  region     = var.region
  node_count = 1

  private_network_uuid = digitalocean_vpc.main.id
  tags                 = [var.project]
}
```

## Spaces (Object Storage)

```hcl
resource "digitalocean_spaces_bucket" "assets" {
  name   = "${var.project}-assets"
  region = var.spaces_region  # nyc3, sfo3, ams3, sgp1, fra1

  acl = "private"
}

resource "digitalocean_spaces_bucket_cors_configuration" "assets" {
  bucket = digitalocean_spaces_bucket.assets.id
  region = var.spaces_region

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "PUT", "POST"]
    allowed_origins = ["https://${var.domain}"]
    max_age_seconds = 3600
  }
}

output "spaces_endpoint" {
  value = digitalocean_spaces_bucket.assets.bucket_domain_name
}
```

## DNS Records

```hcl
resource "digitalocean_domain" "main" {
  name = var.domain
}

resource "digitalocean_record" "app" {
  domain = digitalocean_domain.main.id
  type   = "A"
  name   = "@"
  value  = digitalocean_reserved_ip.app.ip_address
  ttl    = 300
}

resource "digitalocean_record" "www" {
  domain = digitalocean_domain.main.id
  type   = "CNAME"
  name   = "www"
  value  = "@"
  ttl    = 300
}
```

## SSH Keys

```hcl
data "digitalocean_ssh_key" "deploy" {
  name = "deploy-key"
}

resource "digitalocean_ssh_key" "deploy" {
  name       = "${var.project}-deploy"
  public_key = file(pathexpand("~/.ssh/deploy.pub"))
}
```

See [references/digitalocean-production-stack.md](digitalocean-production-stack.md) for a complete production setup with VPC, droplet, firewall, database, and outputs.

## References

- [references/digitalocean-sizes.md](digitalocean-sizes.md) - Droplet and database sizes
- [references/digitalocean-production-stack.md](digitalocean-production-stack.md) - Complete production setup
