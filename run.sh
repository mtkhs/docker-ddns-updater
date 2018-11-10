#!/bin/sh

docker run --rm -v `pwd`/crontab:/var/spool/cron/crontabs/root -v `pwd`/workspace:/workspace mtkhs/ddns-updater:latest

