#!/bin/bash

docker stack rm apps

docker swarm leave --force
