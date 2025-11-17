from flask import Flask, jsonify
import os
import boto3
from botocore.config import Config

app = Flask(__name__)

AWS_ENDPOINT = os.getenv("AWS_ENDPOINT", "http://localstack:4566")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "test")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "test")
APP_VERSION = os.getenv("APP_VERSION", "v1")
S3_BUCKET = os.getenv("S3_BUCKET", "demo-bucket")
SQS_QUEUE_NAME = os.getenv("SQS_QUEUE_NAME", "demo-queue")

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)
config = Config(signature_version="s3v4")

s3 = session.client("s3", endpoint_url=AWS_ENDPOINT, config=config)
sqs = session.client("sqs", endpoint_url=AWS_ENDPOINT)


@app.route("/")
def root():
    # Tenta listar objetos no bucket e enviar uma mensagem na fila
    try:
        s3_objects = s3.list_objects_v2(Bucket=S3_BUCKET)
        keys = [obj["Key"] for obj in s3_objects.get("Contents", [])]
    except Exception as e:
        keys = []
        app.logger.error(f"Erro ao acessar S3: {e}")

    try:
        queue_url_resp = sqs.get_queue_url(QueueName=SQS_QUEUE_NAME)
        queue_url = queue_url_resp["QueueUrl"]
        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=f"Hello from {APP_VERSION}",
        )
        sqs_ok = True
    except Exception as e:
        sqs_ok = False
        app.logger.error(f"Erro ao acessar SQS: {e}")

    return jsonify(
        {
            "message": "Hello from demo-app",
            "version": APP_VERSION,
            "s3_bucket": S3_BUCKET,
            "s3_objects": keys,
            "sqs_queue": SQS_QUEUE_NAME,
            "sqs_send_ok": sqs_ok,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)