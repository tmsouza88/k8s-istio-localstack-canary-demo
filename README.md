# 🇺🇸 Kind + Istio + Helm + LocalStack - Canary Deployment Demo  
# 🇧🇷 Demonstração de Canary Deployment com Kind, Istio, Helm e LocalStack  

⚙️ Mini lab local para estudo de **Service Mesh**, **Canary Releases** e **integração com serviços AWS (via LocalStack)** em um cluster Kubernetes rodando com Kind.

---

## 📚 Table of Contents | Índice

- 🎯 [Project Goal | Objetivo do Projeto](#-project-goal--objetivo-do-projeto)
- ✅ [Features | Funcionalidades](#-features--funcionalidades)
- 🧱 [Architecture | Arquitetura](#-architecture--arquitetura)
- 📁 [File Structure | Estrutura dos Arquivos](#-file-structure--estrutura-dos-arquivos)
- 🚀 [Usage Guide | Guia de Uso](#-usage-guide--guia-de-uso)
  - 0️⃣ [Prerequisites | Pré-requisitos](#0️⃣-prerequisites--pré-requisitos)
  - 1️⃣ [Create Cluster | Criar Cluster Kind](#1️⃣-create-cluster--criar-cluster-kind)
  - 2️⃣ [Install Istio | Instalar Istio](#2️⃣-install-istio--instalar-istio)
  - 3️⃣ [Start LocalStack (Optional) | Subir LocalStack (Opcional)](#3️⃣-start-localstack-optional--subir-localstack-opcional)
  - 4️⃣ [Build & Push App | Build & Push da App](#4️⃣-build--push-app--build--push-da-app)
  - 5️⃣ [Helm Deploy | Deploy com Helm](#5️⃣-helm-deploy--deploy-com-helm)
  - 6️⃣ [Configure Istio Routing | Configurar Roteamento Istio](#6️⃣-configure-istio-routing--configurar-roteamento-istio)
  - 7️⃣ [Access the App | Acessar a Aplicação](#7️⃣-access-the-app--acessar-a-aplicação)
- 📊 [Observability (Basic) | Observabilidade (Básica)](#-observability-basic--observabilidade-básica)
- 🧪 [Canary & Traffic Split | Canary & Divisão de Tráfego](#-canary--traffic-split--canary--divisão-de-tráfego)
- 🧠 [Conclusion | Conclusão](#-conclusion--conclusão)

---

## 🎯 Project Goal | Objetivo do Projeto

**🇺🇸**  
Create a reproducible local lab to experiment with:

- Kind-based local Kubernetes clusters  
- Istio service mesh for traffic management  
- Helm-based deployments of multiple app versions  
- Canary releases and traffic splitting (v1 vs v2)  
- Integration with AWS-like services (S3, SQS) through LocalStack  

**🇧🇷**  
Criar um laboratório local reprodutível para praticar:

- Clusters Kubernetes locais com Kind  
- Istio como service mesh para controle de tráfego  
- Deployments com Helm de múltiplas versões da aplicação  
- Canary releases e divisão de tráfego (v1 vs v2)  
- Integração com serviços estilo AWS (S3, SQS) usando LocalStack  

---

## ✅ Features | Funcionalidades

- 🌐 **Kind cluster** (Kubernetes local em Docker)
- 🧮 **Aplicação de exemplo**: calculadora web em Python/Flask
- ⚙️ **Deploy com Helm** de duas versões da app: `demo-app-v1` e `demo-app-v2`
- 🎯 **Canary deployment com Istio** (VirtualService + DestinationRule)
- 🧩 **Sidecar Envoy** injetado automaticamente (Istio)
- 🪣 **LocalStack** para emular serviços AWS (S3, SQS) localmente
- 🔁 **Divisão de tráfego por peso** entre v1 e v2 (ex.: 90% / 10%)
- 🧪 Fácil de estender para testes A/B e políticas de segurança

---

## 🧱 Architecture | Arquitetura

```text
                +----------------------------+
                |        Web Browser        |
                |    (http://localhost)     |
                +-------------+-------------+
                              |
                              v
                   +----------------------+
                   |  Istio Ingress GW   |
                   | (istio-ingressgateway)
                   +----------+-----------+
                              |
                              v
                    +------------------+
                    |  VirtualService  |
                    |  (Canary v1/v2)  |
                    +---------+--------+
                              |
          +-------------------+-------------------+
          |                                       |
          v                                       v
+--------------------+                  +--------------------+
|  demo-app-v1       |                  |  demo-app-v2       |
|  Flask Calculator  |                  |  Flask Calculator  |
|  + Istio sidecar   |                  |  + Istio sidecar   |
+--------------------+                  +--------------------+

                (Optional AWS Emulation)
                +----------------------+
                |      LocalStack      |
                |   S3 / SQS / etc.    |
                +----------------------+

📁 File Structure | Estrutura dos Arquivos
.
├── kind/
│   └── create-cluster.sh           # Script para criar o cluster Kind
│
├── istio/
│   ├── install-istio.sh            # Script para instalar o Istio
│   ├── gateway.yaml                # Istio Gateway
│   ├── virtualservice.yaml         # Istio VirtualService (roteamento canary)
│   └── destinationrule.yaml        # Istio DestinationRule (subsets v1/v2)
│
├── localstack/
│   ├── docker-compose.yml          # LocalStack (S3, SQS, etc.)
│   └── init-localstack.sh          # Criação de bucket, fila, etc. (exemplo)
│
├── app/
│   ├── calculator/
│   │   ├── app.py                  # Backend Flask da calculadora
│   │   ├── requirements.txt
│   │   ├── Dockerfile
│   │   ├── templates/
│   │   │   └── index.html          # Interface da calculadora
│   │   └── static/
│   │       ├── style.css           # Estilos
│   │       └── app.js              # Lógica de front-end
│   │
│   └── charts/
│       └── demo-app/               # Helm chart da aplicação
│           ├── Chart.yaml
│           ├── values.yaml         # Configura repositório da imagem, tags v1/v2
│           └── templates/
│               ├── service.yaml
│               ├── deployment-v1.yaml
│               └── deployment-v2.yaml
│
└── README.md                       


🚀 Usage Guide | Guia de Uso
0️⃣ Prerequisites | Pré-requisitos
🇺🇸 Make sure you have installed:
🇧🇷 Certifique-se de ter instalado:

Docker
kubectl
kind
helm
curl
docker-compose (para LocalStack)

Quick check:
docker --version
kubectl version --client
kind version
helm version
curl --version


1️⃣ Create Cluster | Criar Cluster Kind

cd kind
./create-cluster.sh
🇺🇸 Expected: a Kind cluster named istio-localstack-demo and kubectl pointing to it.
🇧🇷 Esperado: um cluster Kind chamado istio-localstack-demo e o kubectl já usando esse contexto.

Verify:
bash
Copy
kubectl get nodes
kubectl cluster-info

2️⃣ Install Istio | Instalar Istio

cd ../istio
./install-istio.sh

This should:

Create istio-system namespace
Install Istio control plane + ingress gateway
Enable sidecar injection (namespace default)

Check:
kubectl -n istio-system get pods
kubectl -n istio-system get svc istio-ingressgateway
All pods should be Running.

3️⃣ Start LocalStack (Optional) | Subir LocalStack (Opcional)
cd ../localstack
docker-compose up -d
./init-localstack.sh
🇺🇸 LocalStack will start and (optionally) create an S3 bucket and SQS queue.
🇧🇷 O LocalStack será iniciado e (opcionalmente) criará um bucket S3 e uma fila SQS.

Check:
docker ps | grep localstack
💡 A calculadora funciona mesmo sem LocalStack. Use LocalStack se quiser praticar integração com “AWS local”.

4️⃣ Build & Push App | Build & Push da App
cd ../app/calculator

# Substitua <seu-usuario> pelo seu usuário do Docker Hub
docker build -t docker.io/<seu-usuario>/demo-calculator:v1 .

docker push docker.io/<seu-usuario>/demo-calculator:v1
Sempre que mudar o código da calculadora, refaça o build e o push para garantir que o cluster usa a versão nova.

5️⃣ Helm Deploy | Deploy com Helm
Edite app/charts/demo-app/values.yaml:

image:
  repository: docker.io/<seu-usuario>/demo-calculator
  tagV1: "v1"
  tagV2: "v1"  # inicialmente, v2 pode usar a mesma imagem de v1
Depois:

cd ../
cd app

helm install demo-app charts/demo-app
Check:

kubectl get pods
kubectl get svc
Você deve ver algo como:

demo-app-v1-xxxxx → 2/2 Running
demo-app-v2-xxxxx → 2/2 Running
Service demo-app do tipo ClusterIP

6️⃣ Configure Istio Routing | Configurar Roteamento Istio

cd ..
kubectl apply -f istio/gateway.yaml
kubectl apply -f istio/virtualservice.yaml
kubectl apply -f istio/destinationrule.yaml
Check:

kubectl get gateway
kubectl get virtualservice
kubectl get destinationrule
7️⃣ Access the App | Acessar a Aplicação
Crie um port-forward para o Istio Ingress Gateway:

kubectl -n istio-system port-forward svc/istio-ingressgateway 8080:80
Agora acesse no navegador:

http://localhost:8080/
Você deve ver a calculadora web rodando.

Test via terminal:

curl -i http://localhost:8080/
curl http://localhost:8080/health
📊 Observability (Basic) | Observabilidade (Básica)
Este lab não instala automaticamente Kiali/Prometheus/Grafana, mas você pode:

Usar kubectl para ver status de pods e services
Usar kubectl logs para ver logs da app e do sidecar
Exemplos:

kubectl get pods
kubectl logs <nome-do-pod-v1> -c demo-app
kubectl logs <nome-do-pod-v1> -c istio-proxy
Se quiser expandir:

Adicione Prometheus + Grafana (addons do Istio)
Adicione Kiali para visualizar o mesh
🧪 Canary & Traffic Split | Canary & Divisão de Tráfego
O VirtualService do Istio está configurado para dividir o tráfego entre v1 e v2 usando weights (por exemplo, 90% / 10%).

🔍 Verificando o Canary via /health
Com o port-forward ainda ativo:

for i in {1..20}; do
  curl -s http://localhost:8080/health | jq .version
done


Você deve ver maioria "v1" e algumas respostas "v2" (dependendo dos pesos configurados em virtualservice.yaml).

⚙️ Ajustando os pesos
Edite istio/virtualservice.yaml:

http:
  - route:
      - destination:
          host: demo-app
          subset: v1
        weight: 50
      - destination:
          host: demo-app
          subset: v2
        weight: 50


Reaplique:

kubectl apply -f istio/virtualservice.yaml
Agora o tráfego deve ficar aproximadamente 50/50 entre v1 e v2.

🧠 Conclusion | Conclusão

🇺🇸
This project provides a small but realistic sandbox to understand:

How to run a local Kubernetes cluster with Kind
How Istio controls traffic between multiple versions of the same service
How Helm helps you package and deploy applications
How to start integrating with AWS-style services using LocalStack

🇧🇷
Este projeto oferece um laboratório pequeno, mas realista, para entender:

Como rodar um cluster Kubernetes local com Kind
Como o Istio controla o tráfego entre múltiplas versões de um mesmo serviço
Como o Helm facilita o empacotamento e o deploy da aplicação
Como começar a integrar com serviços estilo AWS usando LocalStack


📌 Repo criado para fins educacionais — sinta-se à vontade para clonar, adaptar e evoluir (por exemplo: adicionar Kiali, Prometheus, Grafana, AuthorizationPolicy, A/B testing por header, etc.).