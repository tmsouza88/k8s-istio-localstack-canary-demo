#!/usr/bin/env bash
set -e

AWS_ENDPOINT="http://localhost:4566"
AWS_REGION="us-east-1"
AWS_ACCESS_KEY_ID="test"
AWS_SECRET_ACCESS_KEY="test"

export AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_REGION

echo "Criando bucket S3 demo-bucket..."
aws --endpoint-url="$AWS_ENDPOINT" s3 mb s3://demo-bucket || true

echo "Criando fila SQS demo-queue..."
aws --endpoint-url="$AWS_ENDPOINT" sqs create-queue --queue-name demo-queue || true

echo "Recursos criados no LocalStack."