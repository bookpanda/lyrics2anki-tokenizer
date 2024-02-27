import logging

from flask import Flask, jsonify, request
from fugashi import Tagger
from waitress import serve

from type import *

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route("/")
def index():
    return "healthy"


@app.route("/tokenize", methods=["POST"])
def tokenize():
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
