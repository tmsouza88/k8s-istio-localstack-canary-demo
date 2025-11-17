from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "v1")


@app.route("/")
def index():
    return render_template("index.html", version=APP_VERSION)


@app.route("/health")
def health():
    return jsonify({"status": "ok", "version": APP_VERSION})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)