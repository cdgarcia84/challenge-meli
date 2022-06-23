FROM python:3-alpine

RUN apk update && \
    apk add mysql-client && \
    pip install --upgrade pip && \
    pip install mysql-connector-python-rf && \
    pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib tabulate requests tqdm && \
    rm -rf /var/cache/apk/*

COPY ./app.py /home/
COPY ./_dbhelper.py /home/
COPY ./_gghelper.py /home/
COPY ./credentials_drive.json /home/
COPY ./credentials_gmail.json /home/

WORKDIR /home

ENTRYPOINT ["tail", "-f", "/dev/null"]
