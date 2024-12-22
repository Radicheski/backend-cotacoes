FROM fedora:42
LABEL authors="erik.radicheski@gmail.com"

RUN dnf update -y
RUN dnf install -y \
    python3 \
    python3-pip \
    python3-virtualenv \
    cronie \
    wget \
    unzip
RUN dnf clean all

WORKDIR /app

RUN python3 -m venv venv
RUN . venv/bin/activate
RUN pip install --upgrade pip
RUN pip install flask

COPY update.sh app.py ./
COPY b3/* ./b3/

RUN chmod u+x update.sh

RUN echo "0 7 * * 2-6 /app/update.sh >> /var/log/update.log 2>&1" > /etc/cron.d/daily_update && \
    chmod 0644 /etc/cron.d/daily_update && \
    crontab /etc/cron.d/daily_update

RUN touch /var/log/update.log

EXPOSE 5000

ENV STOCK_DATA_DIR=/data
ENV STOCK_TEMP_DIR=/temp

ENTRYPOINT ["flask", "--app", "app", "run", "--host=0.0.0.0"]
