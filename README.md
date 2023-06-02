# README #

### Python 3 - Requirements: ###

pip install flask
pip install flask-cors
pip install cachetools
pip install requests

### Server Configs - NGINX Example ###

Expose GraphDB with a reverse-proxy:

```
server {
listen 80;

  server_name sparql.xxx.uminho.pt;

  location / {
    proxy_pass http://localhost:7200;
    proxy_set_header Host $host;
  }
}
```

Install UWSGI (and configure it) and expose the Flask web app in NGINX:

```
server {
    listen 80;
    server_name xxx.uminho.pt;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/var/www/major-minors/uwsgi.sock;
    }

    location /static {
        alias  /var/www/major-minors/static;
    }

    location /favicon.ico {
        alias /var/www/major-minors/static/favicon.ico;
    }
}
```
