#!/bin/bash
docker run --name api-button-recorder \
           -d \
           -p 8000:8000 \
           --env-file envs.env \
           --add-host=database:192.168.1.32 \
           api/button-recorder:0.0