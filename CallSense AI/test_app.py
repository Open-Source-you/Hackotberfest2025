"""
Unit tests for the Customer Call Transcript Analyzer
Tests the Flask application in mock mode (no API key required)
"""

import pytest
import json
import os
import tempfile
from app import app, save_to_csv

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    # Ensure we're in mock mode for testing
    if 'GROQ_API_KEY' in os.environ:
        del os.environ['GROQ_API_KEY']
    
    with app.test_client() as client:
        yield client

@pytest.fixture
def temp_csv():
    """Create a temporary CSV file for testing."""
    temp_fd, temp_path = tempfile.mkstemp(suffix='.csv')
    os.close(temp_fd)
    yield temp_path
    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)

def test_index_route(client):
    """Test that the index route returns the HTML interface."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Customer Call Transcript Analyzer' in response.data
    assert b'<form id="transcriptForm">' in response.data

def test_analyze_endpoint_success(client):
    """Test successful transcript analysis."""
    test_transcript = "Hi, I was trying to book a slot yesterday but the payment failed and I keep getting an error. I tried again and it charged me twice. I am frustrated and want a refund."
    
    response = client.post('/analyze', 
                          data=json.dumps({'transcript': test_transcript}),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert 'transcript' in data
    assert 'summary' in data
    assert 'sentiment' in data
    assert data['transcript'] == test_transcript
    assert data['sentiment'] in ['positive', 'neutral', 'negative']
    assert len(data['summary']) > 0

def test_analyze_endpoint_missing_transcript(client):
    """Test analyze endpoint with missing transcript."""
    response = client.post('/analyze', 
                          data=json.dumps({}),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Missing transcript' in data['error']

def test_analyze_endpoint_empty_transcript(client):
    """Test analyze endpoint with empty transcript."""
    response = client.post('/analyze', 
                          data=json.dumps({'transcript': ''}),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'cannot be empty' in data['error']

def test_analyze_endpoint_invalid_json(client):
    """Test analyze endpoint with invalid JSON."""
    response = client.post('/analyze', 
                          data='invalid json',
                          content_type='application/json')
    
    assert response.status_code == 400

def test_sentiment_classification_negative(client):
    """Test that negative sentiment is correctly identified."""
    negative_transcript = "I am very angry and frustrated with this terrible service. This is awful!"
    
    response = client.post('/analyze', 
                          data=json.dumps({'transcript': negative_transcript}),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['sentiment'] == 'negative'

def test_sentiment_classification_positive(client):
    """Test that positive sentiment is correctly identified."""
    positive_transcript = "Thank you so much! I am very happy and satisfied with the excellent service!"
    
    response = client.post('/analyze', 
                          data=json.dumps({'transcript': positive_transcript}),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['sentiment'] == 'positive'

def test_csv_saving(temp_csv):
    """Test CSV saving functionality."""
    # Temporarily change the CSV file path
    import app
    original_csv = app.CSV_FILE
    app.CSV_FILE = temp_csv
    
    try:
        # Test saving to CSV
        save_to_csv("Test transcript", "Test summary", "neutral")
        
        # Verify file exists and has correct content
        assert os.path.exists(temp_csv)
        
        import pandas as pd
        df = pd.read_csv(temp_csv)
        assert len(df) == 1
        assert df.iloc[0]['Transcript'] == "Test transcript"
        assert df.iloc[0]['Summary'] == "Test summary"
        assert df.iloc[0]['Sentiment'] == "neutral"
        
    finally:
        # Restore original CSV file path
        app.CSV_FILE = original_csv

def test_multiple_requests(client):
    """Test multiple requests to ensure CSV appending works."""
    transcripts = [
        "I love this service!",
        "This is okay I guess.",
        "I hate this terrible experience!"
    ]
    
    for transcript in transcripts:
        response = client.post('/analyze', 
                              data=json.dumps({'transcript': transcript}),
                              content_type='application/json')
        assert response.status_code == 200

if __name__ == '__main__':
    pytest.main([__file__])
