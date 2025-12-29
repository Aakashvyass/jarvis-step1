from openai import OpenAI
import os

from flask import Flask, request, jsonify
from vector_memory import store_memory, recall_memory

app = Flask(__name__)

@app.route("/")
def home():
    return "Jarvis vector memory online."

@app.route("/teach", methods=["POST"])
def teach():
    data = request.get_json()
    text = data.get("text")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    store_memory(text, {"type": "user_taught"})
    return jsonify({"status": "stored"})

@app.route("/recall", methods=["POST"])
def recall():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "No query provided"}), 400

    memories = recall_memory(query)
    return jsonify({"memories": memories})
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message")

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # 1. Recall relevant memories
    memories = recall_memory(user_input)

    # 2. Build system prompt
    system_prompt = f"""
You are Jarvis, a supportive, intelligent personal assistant.
You know the user personally.

Relevant things you remember about the user:
{memories}

Guidelines:
- Be concise
- Be friendly
- Suggest gently, never command
- If nothing relevant, just respond normally
"""

    # 3. Ask the AI to think
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    )

    reply = response.choices[0].message.content

    return jsonify({
        "reply": reply,
        "used_memories": memories
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
