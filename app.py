import logging

from flask import Flask, jsonify, request
from flask_cors import CORS
from fugashi import Tagger
from waitress import serve

from load_env import API_KEY
from type import *

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)


@app.route("/")
def index():
    return "healthy"


@app.route("/tokenize", methods=["POST"])
def tokenize():
    authHeader = request.headers.get("Authorization")
    if not authHeader:
        return jsonify({"error": "unauthorized"}), 401
    token = authHeader.split(" ")[1]
    if token != API_KEY:
        return jsonify({"error": "unauthorized"}), 401
    if request.method != "POST":
        return jsonify({"error": "Invalid request method"}), 405
    if not request.is_json:
        return jsonify({"error": "Request is not JSON"}), 400

    data = request.get_json()
    lyrics: Lyrics = data.get("lyrics")
    app.logger.info(f"Received lyrics: {lyrics}")

    tagger = Tagger("-Owakati")

    tokens: TokenSet = set()
    for line in lyrics:
        words: list[Word] = tagger(line)
        for word in words:
            tokens.add(word.surface)

    token_list = [tk for tk in tokens]

    return jsonify({"tokens": token_list}), 200


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)
