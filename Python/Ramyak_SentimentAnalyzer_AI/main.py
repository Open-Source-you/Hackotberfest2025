# main.py
from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)


sentiment_analyzer = pipeline("sentiment-analysis")

@app.route('/')
def home():
    return "Welcome to the GenAI Sentiment Analyzer API!"

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({"error": "Please provide text for sentiment analysis"}), 400
    
    text = data['text']
    
    
    result = sentiment_analyzer(text)
    
    return jsonify({
        "text": text,
        "sentiment": result[0]['label'],
        "score": result[0]['score']
    })

if __name__ == '__main__':
    app.run(debug=True)
