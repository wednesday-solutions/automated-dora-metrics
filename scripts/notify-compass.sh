#!/bin/bash

# Validate the number of arguments
if [ $# -ne 2 ]; then
    echo "Usage: $0 <source_yaml> <target_yaml>"
    exit 1
fi

# Assign arguments to variables
SOURCE_YAML="$1"
TARGET_YAML="$2"

# Convert current UTC time to IST
TIMESTAMP=$(TZ="Asia/Kolkata" date +'%Y-%m-%dT%H:%M:%SZ')

# Fetched from environment (ci)
USER_EMAIL=$COMPASS_USER_EMAIL
USER_API_KEY=$COMPASS_USER_API_KEY
URL=$COMPASS_METRICS_BASE_URL
COMMON_METRICS_ID=$(yq eval '.common_metrics_id' "$TARGET_YAML") # common_metrics_id must be stored beforehand

for metric in $(yq eval '.target_metrics | keys | .[]' "$TARGET_YAML"); do
    key_pair=$(yq eval ".target_metrics.$metric" "$TARGET_YAML")

    # Split the output into key and value using awk
    key=$(echo "$key_pair" | awk -F ': ' '{print $1}')
    id=$(echo "$key_pair" | awk -F ': ' '{print $2}')
    metric_value=$(yq eval ".$key" "$SOURCE_YAML" | tr -d '%')

    METRIC_SOURCE_ID="$COMMON_METRICS_ID/$id"
    PAYLOAD="{\"metricSourceId\": \"$METRIC_SOURCE_ID\", \"value\": "$metric_value", \"timestamp\": \"$TIMESTAMP\"}"
    echo $PAYLOAD

    curl --request POST \
    --url "$URL" \
    --user "$USER_EMAIL:$USER_API_KEY" \
    --header "Accept: application/json" \
    --header "Content-Type: application/json" \
    --data "$PAYLOAD"
done
