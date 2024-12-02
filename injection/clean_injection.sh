#!/usr/bin/env bash

docker stop injection_web 
docker stop injection_webapp
docker rm injection_web 
docker rm injection_webapp