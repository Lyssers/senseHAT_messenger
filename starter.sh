#!/bin/bash
sudo cp ./index.html /var/www/servers/www.yourdomain/index.html
sudo cp ./lighttpd.conf /etc/lighttpd/lighttpd.conf
sudo systemctl restart lighttpd
