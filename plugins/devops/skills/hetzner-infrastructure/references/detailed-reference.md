# Or with 1Password Detailed Reference

## Floating IPs (High Availability)

```hcl
resource "hcloud_floating_ip" "app" {
  type          = "ipv4"
  name          = "${var.project}-vip"
  home_location = "fsn1"
}

resource "hcloud_floating_ip_assignment" "app" {
  floating_ip_id = hcloud_floating_ip.app.id
  server_id      = hcloud_server.app.id
}

output "floating_ip" {
  value = hcloud_floating_ip.app.ip_address
}
```

## Load Balancers

### HTTP Load Balancer

```hcl
resource "hcloud_load_balancer" "web" {
  name               = "${var.project}-lb"
  load_balancer_type = "lb11"
  location           = "fsn1"

  labels = {
    project = var.project
  }
}

resource "hcloud_load_balancer_network" "web" {
  load_balancer_id = hcloud_load_balancer.web.id
  network_id       = hcloud_network.private.id
  ip               = "10.0.1.100"
}

resource "hcloud_load_balancer_service" "http" {
  load_balancer_id = hcloud_load_balancer.web.id
  protocol         = "http"
  listen_port      = 80
  destination_port = 8080

  health_check {
    protocol = "http"
    port     = 8080
    interval = 10
    timeout  = 5
    retries  = 3

    http {
      path         = "/health"
      status_codes = ["200"]
    }
  }
}

resource "hcloud_load_balancer_target" "web" {
  load_balancer_id = hcloud_load_balancer.web.id
  type             = "server"
  server_id        = hcloud_server.app.id
  use_private_ip   = true

  depends_on = [hcloud_load_balancer_network.web]
}
```

### HTTPS Load Balancer with Certificate

```hcl
resource "hcloud_managed_certificate" "web" {
  name         = "${var.project}-cert"
  domain_names = [var.domain, "www.${var.domain}"]

  labels = {
    project = var.project
  }
}

resource "hcloud_load_balancer_service" "https" {
  load_balancer_id = hcloud_load_balancer.web.id
  protocol         = "https"
  listen_port      = 443
  destination_port = 8080

  http {
    certificates = [hcloud_managed_certificate.web.id]
    redirect_http = true
  }

  health_check {
    protocol = "http"
    port     = 8080
    interval = 10
    timeout  = 5
  }
}
```

## Volumes (Persistent Storage)

```hcl
resource "hcloud_volume" "data" {
  name      = "${var.project}-data"
  size      = 100  # GB
  location  = "fsn1"
  format    = "ext4"

  labels = {
    project = var.project
    purpose = "database"
  }
}

resource "hcloud_volume_attachment" "data" {
  volume_id = hcloud_volume.data.id
  server_id = hcloud_server.db.id
  automount = true
}
```

## SSH Keys

```hcl
resource "hcloud_ssh_key" "deploy" {
  name       = "${var.project}-deploy"
  public_key = file(var.ssh_public_key_path)
}
```

## References

- [references/hetzner-server-types.md](hetzner-server-types.md) - All server types with specs
- [references/ansible-integration.md](ansible-integration.md) - Hetzner+Ansible patterns, Kamal-ready playbooks
- [references/best-practices.md](best-practices.md) - Labels, cost optimization, placement groups, snapshots
- [references/object-storage.md](object-storage.md) - S3-compatible Object Storage with AWS provider
- [references/production-stack.md](production-stack.md) - Complete production setup
- [references/storage-box.md](storage-box.md) - CIFS-mounted backup storage for Litestream and docker-volume-backup
