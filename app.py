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

    # Recall relevant memories
    memories = recall_memory(user_input)

    prompt = f"""
You are Jarvis, a supportive personal assistant.

Relevant memories about the user:
{memories}

User message:
{user_input}

Respond naturally and helpfully.
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    reply = response.output_text

    return jsonify({
        "reply": reply,
        "used_memories": memories
    })

gunicorn app:app --bind 0.0.0.0:$PORT

