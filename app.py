from flask import Flask, request, jsonify
import openai
from googleapiclient.discovery import build
import os
import re
from collections import Counter

app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = 'your_openai_api_key_here'

# Google API key setup
GOOGLE_API_KEY = 'your_google_api_key_here'
CX = 'your_google_custom_search_engine_id_here'

# Helper function to get Google Trends Keywords
def get_google_trends_keywords(query):
    service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
    res = service.cse().list(q=query, cx=CX).execute()
    trends = []
    if 'items' in res:
        for item in res['items']:
            trends.append(item['title'])
    return trends

# Helper function to calculate keyword density
def calculate_keyword_density(text):
    words = re.findall(r'\w+', text.lower())  # Using regex to extract words
    word_count = len(words)
    word_freq = Counter(words)
    keyword_density = {word: (count / word_count) * 100 for word, count in word_freq.items()}
    return keyword_density, word_count

# Route to analyze SEO of the article
@app.route('/analyze', methods=['POST'])
def analyze_seo():
    content = request.json
    text = content.get('content', '')
    
    # Calculate keyword density and word count
    keyword_density, word_count = calculate_keyword_density(text)
    
    return jsonify({
        'word_count': word_count,
        'keyword_density': keyword_density
    })

# Route to suggest keywords based on the text
@app.route('/keywords', methods=['POST'])
def suggest_keywords():
    content = request.json
    text = content.get('content', '')
    
    # Get keywords suggestion from Google Trends based on the first sentence or keyword of the input text
    trending_keywords = get_google_trends_keywords(text.split()[0])  # Take the first word as a search term
    return jsonify({'suggested_keywords': trending_keywords})

# Route to suggest headings
@app.route('/headings', methods=['POST'])
def suggest_headings():
    content = request.json
    text = content.get('content', '')
    
    # Simple mock-up: split the content and suggest H2 or H3 tags based on the sections
    # This could be improved by analyzing the text more intelligently
    lines = text.split('\n')
    headings = []
    for line in lines[:5]:  # Limit to first 5 lines
        headings.append(f'H2: {line.strip()}')
    
    return jsonify({'suggested_headings': headings})

# Route to provide SEO tips
@app.route('/tips', methods=['POST'])
def seo_tips():
    return jsonify({
        'seo_tips': [
            'Use long-tail keywords.',
            'Optimize images with alt tags.',
            'Make sure your site is mobile-friendly.',
            'Use internal linking effectively.',
            'Focus on content quality over quantity.'
        ]
    })

if __name__ == '__main__':
    app.run(debug=True)
