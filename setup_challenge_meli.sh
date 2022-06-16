#!/bin/bash

echo "Iniciando la configuracion..."

docker swarm init &>/dev/null

docker network create --driver overlay meli-net &>/dev/null

openssl rand -base64 12 | docker secret create db_root_password - &>/dev/null
openssl rand -base64 12 | docker secret create db_dba_password - &>/dev/null

echo "..."

docker build -f Dockerfile -t meli-python . &>/dev/null

echo "..."

docker stack deploy -c docker-compose.yaml apps &>/dev/null

echo "Configuracion finalizada"
