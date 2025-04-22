from flask import Flask, request, jsonify
import openai
from googleapiclient.discovery import build
import os

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

# Route to analyze SEO of the article
@app.route('/analyze', methods=['POST'])
def analyze_seo():
    content = request.json
    text = content.get('text', '')
    
    # Here, you'd typically implement an SEO analysis function. For simplicity, we just return a placeholder response.
    return jsonify({
        'SEO Analysis': 'Analysis completed. Check keyword density, headings, and structure.'
    })

# Route to suggest keywords based on the text
@app.route('/keywords', methods=['POST'])
def suggest_keywords():
    content = request.json
    text = content.get('text', '')
    
    # Get keywords suggestion from Google Trends based on the first sentence or keyword of the input text
    trending_keywords = get_google_trends_keywords(text.split()[0])  # Take the first word as a search term
    return jsonify(trending_keywords)

# Route to suggest headings
@app.route('/headings', methods=['POST'])
def suggest_headings():
    content = request.json
    text = content.get('text', '')
    
    # Simple mock-up: split the content and suggest H2 or H3 tags based on the sections
    # This could be improved by analyzing the text more intelligently
    lines = text.split('\n')
    headings = []
    for line in lines[:5]:  # Limit to first 5 lines
        headings.append(f'H2: {line.strip()}')
    
    return jsonify(headings)

# Route to suggest keyword placement in the text
@app.route('/placement', methods=['POST'])
def keyword_placement():
    content = request.json
    text = content.get('text', '')
    
    # Simulate keyword placement suggestions
    keywords = ['SEO', 'content', 'optimization', 'blog', 'keywords']
    placements = []
    
    for keyword in keywords:
        if keyword in text:
            placements.append(f"Place '{keyword}' in the title or heading")
    
    return jsonify(placements)

# Route to provide SEO tips
@app.route('/tips', methods=['POST'])
def seo_tips():
    return jsonify({
        'SEO Tip 1': 'Use long-tail keywords.',
        'SEO Tip 2': 'Optimize images with alt tags.',
        'SEO Tip 3': 'Make sure your site is mobile-friendly.',
        'SEO Tip 4': 'Use internal linking effectively.',
        'SEO Tip 5': 'Focus on content quality over quantity.'
    })

if __name__ == '__main__':
    app.run(debug=True)
