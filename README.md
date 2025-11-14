# k8s-istio-localstack-canary-demo

Demo de canary deployment usando:

- Kind (Kubernetes local)
- Istio (service mesh e roteamento de tráfego)
- Helm (deploy da aplicação)
- LocalStack (emulação de serviços AWS como S3 e SQS)

## 1. Pré-requisitos

- Docker
- kubectl
- kind
- helm
- curl
- docker-compose

## 2. Subir o LocalStack

```bash
cd localstack
docker-compose up -d
./init-localstack.sh