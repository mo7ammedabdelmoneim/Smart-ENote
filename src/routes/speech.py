import os
from flask import Flask, json, render_template, request, jsonify
from groq import Groq
from app import app

# Groq Client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


@app.route("/pronunciation/compare", methods=["GET", "POST"])
def compare_pronunciation():
    if request.method == "GET":
        return render_template("pronunciation/read_compare.html")
    data = request.get_json() or {}

    original_text = data.get("original_text", "")
    spoken_text = data.get("spoken_text", "")

    prompt = f"""
You are a pronunciation and text comparison AI.

Original text: "{original_text}"
Spoken text: "{spoken_text}"

Tasks:
1. Compare the spoken text to the original.
2- ignore the punctuation diffences, case senstivity and focus on the words and context
3. In your output, return the spoken text but **highlight incorrect or missing words** by wrapping them in <span class="wrong-word">...</span>.
4. Give a pronunciation score between 0 and 100 based on accuracy.
5. Provide a brief feedback message explaining errors and what to improve.
6. Return your result as a JSON object with keys: "score", "highlighted_text", "feedback".
"""

    try:
        chat_completion = client.chat.completions.create(
            model="groq/compound-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": spoken_text},
            ],
        )

        result_text = chat_completion.choices[0].message.content.strip()

        import json

        result_json = json.loads(result_text)
        return jsonify(result_json)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route("/pronunciation/ai-text", methods=["GET", "POST"])
def ai_text_generate():
    if request.method == "GET":
        return render_template("pronunciation/ai_text.html")
    data = request.get_json() or {}
    topic = data.get("topic", "").strip()
    level = data.get("level", "A1")

    prompt = f"""
    You are an English teacher. Generate a short English reading text.
    Level: {level}
    Topic: {topic if topic else 'general'}a
    Requirements:
    - 5 lines of text
    - challenging vocabulary for the level
    - best fit the topic
    Return only JSON in this format:
    {{
        "generated_text": "<the text here>"
    }}
    """

    try:
        chat_completion = client.chat.completions.create(
            model="groq/compound-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": topic},
            ],
        )

        result_text = chat_completion.choices[0].message.content.strip()
        result_json = json.loads(result_text)

        return jsonify(result_json)

    except Exception as e:
        print("Error generating AI text:", e)
        return jsonify({"generated_text": "", "error": str(e)}), 500


@app.route("/pronunciation/free-speech", methods=["GET", "POST"])
def free_speech():
    if request.method == "GET":
        return render_template("pronunciation/free_speech.html")
    data = request.get_json()
    spoken_text = data.get("text", "").strip()

    if not spoken_text:
        return jsonify({"error": "No speech text provided"}), 400

    FREE_SPEECH_PROMPT = """
You are an English speaking coach.

Analyze the following spoken English text and return the result strictly in JSON.

Evaluation rules:
- Fluency: rate from 1 to 10 with short comment
- Pronunciation: rate from 1 to 10 with short comment
- Grammar: rate from 1 to 10 with short comment
- CEFR Level: A1, A2, B1, B2, C1, or C2
- Improved text: rewrite the text in correct, natural English
- Feedback: short constructive feedback for the learner

Return ONLY valid JSON in this exact format:
{
  "fluency": "",
  "pronunciation": "",
  "grammar": "",
  "level": "",
  "improved_text": "",
  "feedback": ""
}
"""

    try:
        chat_completion = client.chat.completions.create(
            model="groq/compound-mini",
            messages=[
                {"role": "system", "content": FREE_SPEECH_PROMPT},
                {"role": "user", "content": spoken_text},
            ],
            temperature=0.4,
        )

        result_text = chat_completion.choices[0].message.content.strip()

        result_json = json.loads(result_text)

        return jsonify(result_json)

    except json.JSONDecodeError:
        return (
            jsonify({"error": "AI returned invalid JSON", "raw_response": result_text}),
            500,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
