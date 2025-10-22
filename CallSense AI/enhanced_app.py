import os
import csv
import json
import requests
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
import re

load_dotenv()

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
CSV_FILE = "call_analysis.csv"

def call_groq_api(prompt, model="llama-3.1-8b-instant"):
    if not GROQ_API_KEY:
        return generate_mock_response(prompt)
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 150,
        "temperature": 0.1,
        "top_p": 1,
        "stream": False
    }
    
    try:
        response = requests.post(GROQ_ENDPOINT, headers=headers, json=data, timeout=30)
        
        print(f"API Response Status: {response.status_code}")
        if response.status_code != 200:
            print(f"API Response Text: {response.text}")
        
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    
    except requests.exceptions.RequestException as e:
        print(f"Request error details: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
        raise Exception(f"Groq API request failed: {str(e)}")
    except KeyError as e:
        print(f"JSON parsing error: {str(e)}")
        print(f"Full response: {result}")
        raise Exception(f"Unexpected Groq API response format: {str(e)}")

def generate_mock_response(prompt):
    transcript_text = prompt.lower()
    
    if "summarize" in prompt.lower():
        if any(word in transcript_text for word in ['order', 'shipping', 'delivery', 'package']):
            return "Customer inquired about their order status and shipping details. Agent provided tracking information and estimated delivery timeline."
        elif any(word in transcript_text for word in ['refund', 'return', 'money', 'cancel']):
            return "Customer requested a refund for their recent purchase. Agent processed the return and explained the refund timeline."
        elif any(word in transcript_text for word in ['technical', 'error', 'bug', 'not working', 'problem']):
            return "Customer experienced technical difficulties with the service. Agent provided troubleshooting steps and escalated to technical support."
        elif any(word in transcript_text for word in ['account', 'login', 'password', 'access']):
            return "Customer had issues accessing their account. Agent helped reset credentials and verified account security."
        elif any(word in transcript_text for word in ['billing', 'charge', 'payment', 'credit card']):
            return "Customer questioned billing charges on their account. Agent reviewed the charges and provided detailed explanation."
        elif any(word in transcript_text for word in ['subscription', 'plan', 'upgrade', 'downgrade']):
            return "Customer wanted to modify their subscription plan. Agent explained available options and processed the requested changes."
        elif any(word in transcript_text for word in ['complaint', 'disappointed', 'unsatisfied', 'poor service']):
            return "Customer expressed dissatisfaction with recent service experience. Agent apologized and offered compensation to resolve the issue."
        elif any(word in transcript_text for word in ['praise', 'excellent', 'wonderful', 'amazing', 'great job']):
            return "Customer called to express appreciation for outstanding service received. Agent thanked the customer and noted the positive feedback."
        elif any(word in transcript_text for word in ['information', 'question', 'how to', 'help']):
            return "Customer sought information about product features and usage. Agent provided comprehensive guidance and additional resources."
        else:
            summaries = [
                "Customer contacted support regarding general service inquiries. Agent provided helpful information and resolved all questions.",
                "Customer discussed account management and service options. Agent explained available features and assisted with setup.",
                "Customer needed assistance with product usage and best practices. Agent provided step-by-step guidance and tips.",
                "Customer inquired about company policies and procedures. Agent clarified terms and conditions thoroughly.",
                "Customer requested information about new features and updates. Agent demonstrated functionality and provided documentation."
            ]
            import random
            return random.choice(summaries)
    
    elif "sentiment" in prompt.lower():
        if any(word in transcript_text for word in ['frustrated', 'angry', 'upset', 'terrible', 'awful', 'horrible', 'disappointed', 'unacceptable']):
            return "negative"
        elif any(word in transcript_text for word in ['happy', 'satisfied', 'great', 'excellent', 'wonderful', 'amazing', 'fantastic', 'perfect', 'love']):
            return "positive"
        elif any(word in transcript_text for word in ['okay', 'fine', 'alright', 'neutral', 'average']):
            return "neutral"
        else:
            sentiments = ['positive', 'neutral', 'negative']
            import random
            return random.choice(sentiments)

def get_summary(transcript):
    prompt = f"Summarize the following customer call transcript in 2–3 sentences. Be concise and use plain English. Transcript: {transcript}"
    return call_groq_api(prompt)

def get_sentiment(transcript):
    prompt = f"Read the following transcript and classify the customer's sentiment as one of: positive, neutral, or negative. Return the single word only. Transcript: {transcript}"
    
    sentiment_raw = call_groq_api(prompt).lower().strip()
    
    if any(word in sentiment_raw for word in ['positive', 'good', 'happy', 'satisfied']):
        return 'positive'
    elif any(word in sentiment_raw for word in ['negative', 'bad', 'angry', 'frustrated', 'upset']):
        return 'negative'
    else:
        return 'neutral'

def save_to_csv(transcript, summary, sentiment):
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=['Transcript', 'Summary', 'Sentiment'])
        df.to_csv(CSV_FILE, index=False, encoding='utf-8')
    
    new_row = pd.DataFrame({
        'Transcript': [transcript],
        'Summary': [summary],
        'Sentiment': [sentiment]
    })
    
    try:
        existing_df = pd.read_csv(CSV_FILE, encoding='utf-8')
        updated_df = pd.concat([existing_df, new_row], ignore_index=True)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        updated_df = new_row
    
    updated_df.to_csv(CSV_FILE, index=False, encoding='utf-8')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/analyze', methods=['POST'])
def analyze_transcript():
    try:
        data = request.get_json()
        if not data or 'transcript' not in data:
            return jsonify({'error': 'Missing transcript in request'}), 400
        
        transcript = data['transcript'].strip()
        if not transcript:
            return jsonify({'error': 'Transcript cannot be empty'}), 400
        
        print(f"\n{'='*60}")
        print("PROCESSING NEW TRANSCRIPT")
        print(f"{'='*60}")
        print(f"Original Transcript:\n{transcript}")
        print(f"{'='*60}")
        
        try:
            summary = get_summary(transcript)
            sentiment = get_sentiment(transcript)
        except Exception as e:
            print(f"Error calling Groq API: {str(e)}")
            return jsonify({'error': f'API error: {str(e)}'}), 500
        
        summary = summary.replace('\n', ' ').strip()
        sentiment = sentiment.lower().strip()
        
        print(f"Generated Summary:\n{summary}")
        print(f"{'='*60}")
        print(f"Detected Sentiment: {sentiment}")
        print(f"{'='*60}")
        
        try:
            save_to_csv(transcript, summary, sentiment)
            print(f"Results saved to {CSV_FILE}")
        except Exception as e:
            print(f"Error saving to CSV: {str(e)}")
            return jsonify({'error': f'CSV save error: {str(e)}'}), 500
        
        print(f"{'='*60}\n")
        
        return jsonify({
            'transcript': transcript,
            'summary': summary,
            'sentiment': sentiment
        })
    
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/history', methods=['GET'])
def get_analysis_history():
    try:
        if not os.path.exists(CSV_FILE):
            return jsonify({'history': []})
        
        df = pd.read_csv(CSV_FILE, encoding='utf-8')
        history = []
        
        for _, row in df.iterrows():
            history.append({
                'transcript': row['Transcript'],
                'summary': row['Summary'],
                'sentiment': row['Sentiment'],
                'timestamp': pd.Timestamp.now().isoformat()
            })
        
        return jsonify({'history': history})
    
    except Exception as e:
        print(f"Error loading history: {str(e)}")
        return jsonify({'error': f'Failed to load history: {str(e)}'}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        if not os.path.exists(CSV_FILE):
            return jsonify({'total': 0, 'positive': 0, 'neutral': 0, 'negative': 0})
        
        df = pd.read_csv(CSV_FILE, encoding='utf-8')
        sentiment_counts = df['Sentiment'].value_counts().to_dict()
        
        stats = {
            'total': len(df),
            'positive': sentiment_counts.get('positive', 0),
            'neutral': sentiment_counts.get('neutral', 0),
            'negative': sentiment_counts.get('negative', 0)
        }
        
        return jsonify(stats)
    
    except Exception as e:
        print(f"Error loading stats: {str(e)}")
        return jsonify({'error': f'Failed to load stats: {str(e)}'}), 500

@app.route('/api/export', methods=['GET'])
def export_data():
    try:
        if not os.path.exists(CSV_FILE):
            return jsonify({'error': 'No data to export'}), 404
        
        return send_from_directory('.', CSV_FILE, as_attachment=True, 
                                 download_name=f'call_analysis_export_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.csv')
    
    except Exception as e:
        print(f"Error exporting data: {str(e)}")
        return jsonify({'error': f'Failed to export data: {str(e)}'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🚀 Starting CallAnalyzer Pro - Enhanced Edition...")
    print("=" * 60)
    
    if not GROQ_API_KEY:
        print("⚠️  WARNING: GROQ_API_KEY not found. Running in MOCK MODE.")
        print("   Set GROQ_API_KEY environment variable for full functionality.")
    else:
        print("✅ Groq API key detected. Running in FULL MODE.")
    
    print(f"📊 CSV file will be saved as: {CSV_FILE}")
    print("🌐 Server starting on http://127.0.0.1:5000")
    print("🎨 Modern UI available at http://127.0.0.1:5000")
    print("🔌 API endpoints:")
    print("   POST /analyze - Analyze transcript")
    print("   GET /api/history - Get analysis history")
    print("   GET /api/stats - Get statistics")
    print("   GET /api/export - Export data as CSV")
    print("=" * 60)
    
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    app.run(debug=True, host='127.0.0.1', port=5000)
