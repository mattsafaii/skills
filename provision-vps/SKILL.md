---
name: provision-vps
description: Provision and secure a DigitalOcean droplet for a Safaii Studio project — create the droplet with the hardened cloud-config, verify the secure bootstrap, and hand off to Kamal. Use when Matt says "provision a droplet", "create a VPS", "spin up a server for [project]", "set up a droplet for [project]", "deploy [project] to a server", or "/provision". This is the DevOps entry point for the Safaii Studio self-hosted stack (DigitalOcean + Kamal + Tailscale + Basecamp alerts). Do not use for generic server questions with no provisioning intent — point those at the reference docs instead.
---

# Provision a Safaii Studio VPS

Provision a hardened DigitalOcean droplet for a Safaii Studio project and hand it
off to Kamal. Everything is opinionated and decided — this skill encodes those
decisions so provisioning is repeatable without re-litigating them.

## The stack (decided, don't re-derive)

- **Provider:** DigitalOcean, Safaii Studio account (`safaii-studio` doctl context)
- **Deploy tool:** Kamal (zero-downtime deploys, kamal-proxy handles TLS/Let's Encrypt)
- **Internal access:** Tailscale mesh VPN (not SSH tunnels as the default)
- **Alerts:** Basecamp chatbot → "Server Alerts" room in the Office project
- **OS:** Ubuntu 24.04

## Decisions already made (honor these)

- Plain droplet names, NO `-prod` suffix — Matt will never run staging. Name is
  the project name (`hookah-hunt`, `garp`).
- SSH stays on port 22; keep `PermitRootLogin prohibit-password` (Kamal connects
  as root by default — the article's `PermitRootLogin no` would break Kamal).
- No healthchecks.io, no spiped, no Cloudflare Tunnel, no Docker-in-Docker
  monitoring, no Docker contexts — all evaluated and skipped. See the reference
  docs for the reasoning if it comes up.
- Internal services bind loopback-only (`port: "127.0.0.1:X:X"`), NOT bare
  `port: "X:X"` — Docker bypasses UFW, so loopback binding is the real protection.

## Key paths

- Cloud-config: `~/Code/safaii-tools/scripts/Server Config Script/digitalocean-cloud-config.yaml`
- Kamal accessory security: `~/Code/safaii-tools/scripts/Server Config Script/kamal-accessory-security.md`
- Cloudflare Tunnel eval: `~/Code/safaii-tools/scripts/Server Config Script/cloudflare-tunnel-vs-ufw-proxy.md`

## Workflow

### 1. Gather

- Confirm the project name and that it has a repo with `config/deploy.yml`
  (Kamal initialized) or a Basecamp project it belongs to.
- Confirm the cloud-config is up to date: it ships SSH hardening, UFW, fail2ban,
  unattended-upgrades, disk/inode/CPU/mem monitors, Docker log + crash-loop
  monitor, Basecamp alerts, Tailscale install + auth, and Docker log caps.

### 2. Prepare secrets in the cloud-config

- **Tailscale auth key:** `/etc/tailscale-authkey` currently has a placeholder.
  Before creating a droplet, check whether Matt has generated a single-use,
  short-expiry key and pasted it in. If not, flag it — the droplet will boot
  without joining the tailnet (recoverable: `tailscale up` manually later).
- **Basecamp lines_url:** already set to the Office "Server Alerts" room. For a
  second project, Matt may want a per-project room + bot instead — ask before
  assuming. Keep the alert sender script as-is either way.

### 3. Register SSH key (once)

If the Mac Mini key isn't registered with the Safaii DO account:

```bash
doctl compute ssh-key create matt-macmini --public-key "$(cat ~/.ssh/id_ed25519.pub)"
```

Fingerprint is used in `--ssh-keys` below. `doctl compute ssh-key list` to check.

### 4. Create the droplet

From the `safaii-studio` context:

```bash
doctl compute droplet create <project> \
  --size s-1vcpu-2gb \
  --image ubuntu-24-04 \
  --region sfo3 \
  --ssh-keys <fingerprint> \
  --user-data-file "$HOME/Code/scripts/Server Config Script/digitalocean-cloud-config.yaml" \
  --wait
```

- `--ssh-keys` (root access safety net during first boot) is separate from the
  key embedded in the cloud-config (matt user). Both are needed.
- No `-prod` suffix on the name.

### 5. Verify the bootstrap

- `doctl compute droplet get <project>` for the IP.
- SSH in as root with the Mac Mini key. Confirm:
  - `matt` user exists with key auth: `sudo su - matt` then `ssh-keygen -l` check
  - UFW active: `ufw status verbose` (22/80/443, deny incoming)
  - fail2ban active, monitors running: `systemctl status monitor-docker-logs`
  - Monitors present: `ls /usr/local/bin/` shows `send_basecamp_message`,
    `monitor-disk.sh`, `monitor-resources.sh`, `monitor-docker-logs.sh`
  - Tailscale: `tailscale status` (or flag if auth key wasn't set)
  - Basecamp alert works: `send_basecamp_message "Test — <project> droplet up"`

### 6. Post-Tailscale lockdown (do at first login)

Once tailnet SSH is verified, close public port 22:

```bash
sudo ufw allow in on tailscale0 to any port 22 proto tcp
sudo ufw delete allow 22/tcp
sudo ufw status verbose   # 22 should be tailscale0-only
```

Full checklist in `kamal-accessory-security.md`. If Tailscale join failed, DO
NOT delete public 22 — keep it as the recovery path.

### 7. SSH alias on the Mac

Add to `~/.ssh/config` (use tailnet IP once Tailscale is up):

```
Host <project>
  HostName <tailscale-ip>
  User root
  IdentityFile ~/.ssh/id_ed25519
  ServerAliveInterval 30
```

### 8. Hand off to Kamal

From the project repo: `kamal setup`. This installs Docker, provisions
kamal-proxy, and deploys. TLS is automatic via kamal-proxy (Let's Encrypt).
Confirm the DNS A record points at the droplet before `kamal setup`.

## Reminders

- Everything above is Safaii Studio (account 6191443, `safaii-studio` doctl
  context). Zonebrite has its OWN DigitalOcean account, Basecamp account
  (6060605), and separate alerting — never cross them.
- Nothing in this skill is Basecamp-tracked (skill/config work).
- If a tweet/article suggests a tool for this stack, check the reference docs
  before adopting — most were already evaluated and skipped with reasons.
