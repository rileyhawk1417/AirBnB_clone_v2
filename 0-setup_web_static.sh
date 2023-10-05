#!/usr/bin/env bash
# This bash file helps setup nginx with the folders

# setup nginx
sudo apt-get update -y;
sudo apt-get install nginx -y;

# Setup the directories
mkdir -p /data/web_static/releases/test/
mkdir /data/web_static/shared/
mkdir /data/web_static/current/

# Create symbolic link each time script is run
ln -sf /data/web_static/current/ /data/web_static/releases/test/

# Insert content into files
echo "
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
" | sudo tee /data/web_static/releases/test/index.html

# Give ownership to ubuntu
chown -R ubuntu:ubuntu /data/

echo "
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root    /var/www/html;
    index   index.html index.htm;
    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }
    location /redirect_me {
        return 301 www.duckduckgo.com permanent;
    }
    error_page 404 /404.html;
    location /404 {
        root /var/www/html;
        internal;
    }
}
" | sudo tee /etc/nginx/sites-available/default;
service nginx restart;
