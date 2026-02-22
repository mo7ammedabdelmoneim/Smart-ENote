import os
from flask import render_template, request, jsonify
from groq import Groq
from app import app

# Groq Client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


@app.route("/assistant", methods=["GET", "POST"])
def chatbot():
    if request.method == "POST":
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"reply": "Please enter a message."})

        try:
            system_prompt = """
                            You are SmartENote, an English language learning assistant and expert tutor inside the SmartENote app.

                            Guidelines:
                            - Explain grammar, vocabulary, and usage in a structured and beginner-friendly way.
                            - Answer in clear, simple English.
                            - Always clarify differences between similar words when relevant.
                            - Provide 2–3 short examples for each explanation.
                            - Use bullet points when explaining rules.
                            - If the user asks in Arabic, you may explain in Arabic but always include English examples.
                            - Avoid unnecessary complexity.
                            - Focus only on language-related questions: grammar, vocabulary, pronunciation, writing.
                            - Keep explanations short, concise, and step-by-step.
                            """
            chat_completion = client.chat.completions.create(
                model="groq/compound-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
            )

            assistant_message = chat_completion.choices[0].message.content

        except Exception as e:
            assistant_message = f"Error contacting Groq API ❌: {str(e)}"

        return jsonify({"reply": assistant_message})
    return render_template(
        "assistant/chat.html", response="This is a placeholder response from ChatGPT."
    )


if __name__ == "__main__":
    app.run(debug=True)
