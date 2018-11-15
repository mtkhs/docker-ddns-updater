#!/bin/sh

docker run --name ddns-updater --rm -d -v `pwd`/crontab:/var/spool/cron/crontabs/root -v `pwd`/workspace:/workspace mtkhs/ddns-updater
docker exec -it ddns-updater chown root:root /var/spool/cron/crontabs/root
