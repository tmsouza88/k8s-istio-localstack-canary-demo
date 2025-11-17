#!/usr/bin/env bash
set -e

ISTIO_VERSION="1.22.0"

if ! command -v istioctl >/dev/null 2>&1; then
  echo "istioctl não encontrado. Baixe o Istio $ISTIO_VERSION e adicione ao PATH."
  exit 1
fi

istioctl install --set profile=demo -y
kubectl label namespace default istio-injection=enabled --overwrite