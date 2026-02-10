#!/usr/bin/env bash
set -euo pipefail

ENV=${1:-dev}
echo "Starting deploy for $ENV"

docker compose -f docker-compose.yml up -d --build

cat > nginx.conf <<'NG'
events {}
http {
  server {
    listen 443 ssl;
    ssl_certificate /etc/nginx/certs/fullchain.pem;
    ssl_certificate_key /etc/nginx/certs/privkey.pem;
    location /api/ {
      proxy_pass http://server:8080/;
    }
    location / {
      proxy_pass http://web:5173/;
    }
  }
}
NG

echo "Deploy complete"
