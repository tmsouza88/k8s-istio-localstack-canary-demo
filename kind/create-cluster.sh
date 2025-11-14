#!/usr/bin/env bash
set -e

kind delete cluster --name istio-localstack-demo || true
kind create cluster --name istio-localstack-demo --config kind-config.yaml

kubectl cluster-info --context kind-istio-localstack-demo