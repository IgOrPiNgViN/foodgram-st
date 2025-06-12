#!/bin/bash

mkdir -p footgram-st && cd footgram-st

if [ ! -f "docker-compose.yaml" ]; then
  wget https://raw.githubusercontent.com/IgOrPiNgViN/foodgram-st/main/docker-compose.yaml -O docker-compose.yaml
else
  echo "docker-compose.yaml already exists!"
fi

if [ ! -f docker.env ]; then
  wget https://raw.githubusercontent.com/IgOrPiNgViN/foodgram-st/main/docker-example.env -O docker.env
  
  LOCAL_IP=$(ip -4 addr show | grep -v "127.0.0.1" | grep -Po 'inet \K[\d.]+' | head -1)
  
  if [ -z "$LOCAL_IP" ]; then
    echo "Could not determine local IP, using 127.0.0.1"
    LOCAL_IP="127.0.0.1"
  else
    echo "Using local network IP: $LOCAL_IP"
  fi
  
  sed -i "s/EXTERNAL_IP=\"127.0.0.1\"/EXTERNAL_IP=\"$LOCAL_IP\"/g" docker.env
else
  echo "docker.env already exists!"
fi

echo "Files downloaded. Launching containers..."

if [ -z "$USE_PODMAN" ] || [ "$USE_PODMAN" -eq 0 ]; then
  echo "Using docker-compose"
  sudo docker-compose up
else
  echo "Using podman-compose"
  podman-compose up
fi
