FROM python:3.10.4-slim

RUN apt-get update && apt-get install -y net-tools tcpdump supervisor

COPY src/dottcp.py /usr/bin/dottcp
COPY src/dotudp.py /usr/bin/dotudp
COPY config/dnsovertls.conf /etc/supervisor/conf.d/dnsovertls.conf

RUN chmod 755 /usr/bin/dottcp
RUN chmod 755 /usr/bin/dotudp

EXPOSE 53
EXPOSE 53/udp

CMD ["/usr/bin/supervisord", "-n"]
