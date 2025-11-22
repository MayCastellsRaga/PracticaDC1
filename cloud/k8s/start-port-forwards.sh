#!/bin/bash

pkill -f "kubectl proxy" 2>/dev/null
pkill -f "kubectl port-forward" 2>/dev/null

kubectl proxy --port=8001 --address=0.0.0.0 --accept-hosts='.*' > /dev/null 2>&1 &

kubectl port-forward service/influxdb 8086:8086 --address=0.0.0.0 > /dev/null 2>&1 &

kubectl port-forward service/kafka-ui 8080:8080 --address=0.0.0.0 > /dev/null 2>&1 &
