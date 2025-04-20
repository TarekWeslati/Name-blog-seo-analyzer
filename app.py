from flask import Flask, request, jsonify
import re
from collections import Counter

app = Flask(__name__)

# Helper function to analyze SEO
def analyze_seo(content):
    word_count = len(content.split())
    keyword_density = {}
    
    # Remove unwanted characters for analysis
    content = re.sub(r'[^\w\s]', '', content.lower())
    
    # Calculate word frequency
    word_freq = Counter(content.split())
    
    # Calculate keyword density
    for word, freq in word_freq.items():
        keyword_density[word] = (freq / word_count) * 100
    
    return {
        "word_count": word_count,
        "keyword_density": keyword_density
    }

# Function to suggest keywords based on content
def suggest_keywords(content):
    # Here you can add logic for extracting keyword ideas or integrating with Google Trends API
    return {
        "suggested_keywords": [
            "SEO tips", "keyword optimization", "content marketing", "blog SEO", "backlink strategies"
        ]
    }

# Function to suggest headings based on content
def suggest_headings(content):
    return {
        "suggested_headings": [
            "Introduction to SEO",
            "How to Optimize Your Blog for Search Engines",
            "Top SEO Techniques for Bloggers",
            "Common SEO Mistakes to Avoid"
        ]
    }

# Function to generate SEO tips
def seo_tips():
    return {
        "seo_tips": [
            "Use keywords in your titles and headings.",
            "Ensure content is original and valuable.",
            "Include high-quality outbound and inbound links.",
            "Optimize for mobile and page speed."
        ]
    }

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    content = data.get('content', '')
    if content:
        seo_analysis = analyze_seo(content)
        return jsonify(seo_analysis)
    return jsonify({"error": "No content provided."}), 400

@app.route('/keywords', methods=['POST'])
def keywords():
    data = request.get_json()
    content = data.get('content', '')
    if content:
        keywords = suggest_keywords(content)
        return jsonify(keywords)
    return jsonify({"error": "No content provided."}), 400

@app.route('/headings', methods=['POST'])
def headings():
    data = request.get_json()
    content = data.get('content', '')
    if content:
        headings = suggest_headings(content)
        return jsonify(headings)
    return jsonify({"error": "No content provided."}), 400

@app.route('/tips', methods=['POST'])
def tips():
    tips = seo_tips()
    return jsonify(tips)

if __name__ == '__main__':
    app.run(debug=True)
    
