import os
from groq import Groq
from flask import json, render_template, request
from app import app
import re

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


@app.route("/quiz")
def quiz_page():
    return render_template("quiz/outside_quick_quiz.html")


@app.route("/quiz/quick_quiz", methods=["POST"])
def quiz():
    print("Received quiz request")
    content = request.form.get("content", "").strip()
    count = request.form.get("count", "10")
    print(content)
    if not content:
        return render_template("quiz/quiz.html", error="No content provided", quiz=[])

    system_prompt = f"""
You are SmartENote Quiz Generator.

Your task:
- Generate a short English quiz based ONLY on the provided content or topic.
- The quiz is for English learners.

Rules:
- Create {count} multiple-choice questions.
- Each question has 4 options.
- Only ONE option is correct.
- Use simple and clear English.
- Questions must be directly based on the content.
- Do NOT add information outside the content.
- Do NOT mention the "vocab" or "notes" in the questions, just focus on the content.
- Return the result strictly as JSON.
- Do NOT add any text outside the JSON.
"""
    system_prompt += """
JSON format:
{
  "quiz": [
    {
      "question": "",
      "options": ["", "", "", ""],
      "correct_index": 0,
      "explanation": ""
    }
  ]
}
"""
    try:
        completion = client.chat.completions.create(
            model="groq/compound-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f'Content/ topic:\n"""\n{content}\n"""'},
            ],
        )

        raw_output = completion.choices[0].message.content.strip()

        clean_json = re.sub(r"```json|```", "", raw_output).strip()

        quiz_data = json.loads(clean_json)

        if "quiz" not in quiz_data or not isinstance(quiz_data["quiz"], list):
            raise ValueError("Invalid quiz format")

        return render_template("quiz/quiz.html", quiz=quiz_data["quiz"])

    except Exception as e:
        return render_template("quiz/quiz.html", error=str(e), quiz=[])
