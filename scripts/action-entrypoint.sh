#!/bin/sh

if [ "$INPUT_COMMAND" = "calculate-metrics" ]; then
  docker run --rm -v "$(pwd)/metrics":/app/metrics -v "$(pwd)/.git":/app/.git abhimishraa/dorametrics:latest --calculate-metrics -e True
elif [ "$INPUT_COMMAND" = "notify-compass" ]; then
  docker run --rm -v "$(pwd)/metrics":/app/metrics -e COMPASS_USER_EMAIL="$INPUT_COMPASS_USER_EMAIL" -e COMPASS_USER_API_KEY="$INPUT_COMPASS_USER_API_KEY" -e COMPASS_METRICS_BASE_URL="$INPUT_COMPASS_METRICS_BASE_URL" abhimishraa/dorametrics:latest --notify-compass "metrics/data.yaml" "metrics/target-metrics.yaml"
else
  echo "Invalid command specified. Please use 'calculate-metrics' or 'notify-compass'."
  exit 1
fi
