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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
