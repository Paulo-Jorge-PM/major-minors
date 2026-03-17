# Deploy Guide (Docker Compose + Nginx + Let's Encrypt)

This guide deploys the website to `minors.paulojorgepm.net` with:
- Flask behind Nginx
- HTTPS via Let's Encrypt
- GraphDB not exposed publicly
- SPARQL query endpoint/page disabled

## 1. Required environment variables

Run from project root:

```bash
export SECRET_KEY='replace-with-a-long-random-secret'
export GRAPHDB_AUTH_TOKEN_SECRET='replace-with-a-long-random-secret'
export FLASK_DEBUG='false'
# Optional: comma-separated list of allowed origins for /api/*
# export CORS_ORIGINS='https://minors.paulojorgepm.net'
```

## 2. Start containers

```bash
docker compose up -d --build
```

Current compose mapping:
- Flask binds to `127.0.0.1:8001` (local-only)
- GraphDB is internal-only (no host published ports)

## 3. Quick security checks

```bash
docker compose ps
ss -ltnp | rg ':8001|:7200|:7300'
```

Expected:
- `127.0.0.1:8001` is listening
- No public `7200`/`7300` listeners

## 4. Nginx site config

Create `/etc/nginx/sites-available/minors.paulojorgepm.net`:

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name minors.paulojorgepm.net;

    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name minors.paulojorgepm.net;

    client_max_body_size 16m;

    access_log /var/log/nginx/minors.paulojorgepm.net.access.log;
    error_log  /var/log/nginx/minors.paulojorgepm.net.error.log warn;

    ssl_certificate /etc/letsencrypt/live/minors.paulojorgepm.net/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/minors.paulojorgepm.net/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # SPARQL endpoint intentionally disabled
    location = /api/sparql {
        default_type application/json;
        return 503 '{"message":"SPARQL query service temporarily disabled due to low resources."}';
    }

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Port $server_port;
        proxy_connect_timeout 5s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/minors.paulojorgepm.net /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 5. Issue certificate (Let's Encrypt)

```bash
sudo certbot --nginx -d minors.paulojorgepm.net
sudo systemctl reload nginx
```

Check renewal timer:

```bash
systemctl status certbot.timer
```

## 6. SPARQL status

SPARQL is currently disabled by configuration/code:
- `flask/app/controllers/api.py` (`SPARQL_API_ENABLED = False`)
- `flask/app/views/sparql.html` (query form/scripts commented out)

