from flask import  request, jsonify
from deep_translator import GoogleTranslator
from app import app

@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"translation": "No text provided"}), 400

    try:
        translated_text = GoogleTranslator(
            source="en",
            target="ar"
        ).translate(text)

        return jsonify({"translation": translated_text})

    except Exception as e:
        return jsonify({"translation": "Translation failed"}), 500
