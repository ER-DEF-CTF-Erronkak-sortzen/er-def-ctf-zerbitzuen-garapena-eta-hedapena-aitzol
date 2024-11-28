#!/usr/bin/env bash

docker stop injection_web_1 
docker stop injection_webapp_1
docker rm injection_web_1 
docker rm injection_webapp_1