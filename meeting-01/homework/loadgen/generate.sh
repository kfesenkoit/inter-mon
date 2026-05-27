#!/bin/sh
set -eu

# Wait until NGINX is reachable so the loop does not exit on startup races.
until curl -s -o /dev/null "http://nginx/"; do
  sleep 1
done

i=0
while true; do
  i=$((i + 1))

  # High-volume healthy traffic.
  curl -s -o /dev/null "http://nginx/" || true

  # Deterministic error traffic every 10th request.
  if [ $((i % 10)) -eq 0 ]; then
    curl -s -o /dev/null -w "" "http://nginx/error" || true
  fi

  # Deterministic 404 traffic every 15th request.
  if [ $((i % 15)) -eq 0 ]; then
    curl -s -o /dev/null -w "" "http://nginx/notfound" || true
  fi

  sleep 0.3
done
