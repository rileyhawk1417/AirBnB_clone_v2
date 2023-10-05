#!/usr/bin/env bash
# This bash file helps setup nginx with the folders

# setup nginx
sudo apt-get update -y;
sudo apt-get install nginx -y;

# Setup the directories
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir /data/web_static/shared/

# Create symbolic link each time script is run
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current/ 

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
sudo chown -R ubuntu:ubuntu /data/

echo "
server {
	listen 80 default_server;
	listen [::]:80 default_server;
	root    /var/www/html;
	index   index.html index.htm;
	add_header X-Served-By $HOSTNAME;
	server_name seanriley.tech www.seanriley.tech;
	rewrite ^/redirect_me https://www.duckduckgo permanent;
	location /hbnb_static {
		alias /data/web_static/current;
		try_files \$uri \$uri/ /index.html;
		index index.html;
	}

	error_page 404 /404.html;
	location /404 {
		root /var/www/html;
		internal;
	}
}
" | sudo tee /etc/nginx/sites-enabled/default;
sudo service nginx restart;
