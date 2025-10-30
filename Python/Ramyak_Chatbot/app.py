# app.py
# Advanced Generative AI ChatBot with context memory using Flask and Hugging Face

from flask import Flask, render_template, request, jsonify
from transformers import pipeline
from utils.chat_memory import ChatMemory
from utils.prompts import system_prompt

app = Flask(__name__)
generator = pipeline("text-generation", model="gpt2")
memory = ChatMemory(max_memory=5)  # store last 5 exchanges

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    memory.add_message("User", user_input)

    full_prompt = system_prompt + memory.get_context()
    response = generator(full_prompt, max_length=180, num_return_sequences=1)
    ai_output = response[0]['generated_text'].split("AI:")[-1].strip()

    memory.add_message("AI", ai_output)
    return jsonify({"response": ai_output})

if __name__ == "__main__":
    app.run(debug=True)
