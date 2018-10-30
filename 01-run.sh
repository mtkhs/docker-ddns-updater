#!/bin/sh

docker run --rm -v `pwd`/workspace:/workspace mtkhs/ddns-updater:latest

