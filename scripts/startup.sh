#!/bin/sh

set -e

echo "Generating static HTML ..."
jekyll build -s /workdir -d /usr/share/nginx/html

echo "Launching nginx ..."
exec nginx -g 'daemon off;'

