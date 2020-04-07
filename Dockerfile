FROM ubuntu:19.04

WORKDIR /nofrills_tablo_export

COPY nfte.py .
COPY nfte_class.py .
COPY nfte_defs.py .
COPY nfte_globals.py .
COPY init.sh .
COPY nfte-logrotate .

ENV TABLO_IP = 127.0.0.1 \
    DELETE_AFTER_EXPORT = false \
    EXEC_INTERVAL_MINUTES = 120

RUN apt-get update && \
    apt-get -y full-upgrade

RUN apt-get -y install ffmpeg python3 python3-requests && \
    apt-get -y autoremove

RUN chmod u+x init.sh && \
    chmod u+x nfte.py && \
    cp /nofrills_tablo_export/nfte-logrotate /etc/logrotate.d/nofrills_tablo_export && \
    mkdir /nofrills_tablo_export/export && \
    mkdir /nofrills_tablo_export/export/movies && \
    mkdir /nofrills_tablo_export/export/sports && \
    mkdir /nofrills_tablo_export/export/tv && \
    mkdir /nofrills_tablo_export/export/incomplete

VOLUME [ "/nofrills_tablo_export/export/movies", \
    "/nofrills_tablo_export/export/sports", \
    "/nofrills_tablo_export/export/tv", \
    "/nofrills_tablo_export/export/incomplete" ]

ENTRYPOINT [ "./init.sh" ]
