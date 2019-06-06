#!/usr/bin/env sh
# Deployment script for MMDA
# Force a renewal of the Let's Encrypt TLS Certificate
# Usually a systemd Timer takes care of this, just in case.

set -ex

/usr/bin/docker run --rm -v /etc/letsencrypt:/etc/letsencrypt certbot/certbot renew  --force-renewal --webroot -w /etc/letsencrypt
