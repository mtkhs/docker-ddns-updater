FROM mtkhs/alpine-py3-curl:latest

RUN apk add --update --no-cache tzdata \
    && pip install pyyaml requests \
    && mkdir /workspace

ENV TZ='Asia/Tokyo'

COPY crontab /var/spool/cron/crontabs/root

CMD [ "/usr/sbin/crond", "-f", "-d", "8" ]

