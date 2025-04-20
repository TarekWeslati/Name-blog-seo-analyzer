from flask import Flask, render_template, request, jsonify
from collections import Counter
import re
import json

app = Flask(__name__)

# Home route that renders the index.html
@app.route('/')
def home():
    return render_template('index.html')

# Route to analyze text and return SEO results
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    content = data['content']
    
    # Calculate word count
    word_count = len(content.split())

    # Keyword Density calculation (for simplicity, let's check for common keywords)
    keywords = ['SEO', 'content', 'marketing', 'backlink', 'blog']
    keyword_density = {}

    word_list = re.findall(r'\w+', content.lower())  # Extract words and make them lowercase
    word_counter = Counter(word_list)

    for keyword in keywords:
        keyword_density[keyword] = (word_counter[keyword] / word_count) * 100
    
    # Return the results as a JSON response
    return jsonify({
        'word_count': word_count,
        'keyword_density': keyword_density
    })

# Route to suggest keywords based on the content (static list for now)
@app.route('/keywords', methods=['POST'])
def keywords():
    data = request.get_json()
    content = data['content']
    
    # A mockup of suggested keywords (ideally you'd connect to an API or perform keyword research)
    suggested_keywords = [
        "SEO tips",
        "keyword optimization",
        "content marketing",
        "blog SEO",
        "backlink strategies"
    ]
    
    return jsonify({
        'suggested_keywords': suggested_keywords
    })

# Route to suggest headings based on the content
@app.route('/headings', methods=['POST'])
def headings():
    data = request.get_json()
    content = data['content']
    
    # Sample static headings based on analysis of the content
    suggested_headings = [
        "Introduction to SEO",
        "Why SEO is Important",
        "How to Optimize Your Content",
        "Link Building Strategies",
        "SEO Best Practices"
    ]
    
    return jsonify({
        'suggested_headings': suggested_headings
    })

# Route to provide SEO tips
@app.route('/tips', methods=['POST'])
def tips():
    # Static SEO tips to improve SEO ranking
    seo_tips = [
        "Use relevant keywords in your titles and headers.",
        "Optimize your meta descriptions.",
        "Ensure your website is mobile-friendly.",
        "Use high-quality images with proper alt text.",
        "Build backlinks to your content."
    ]
    
    return jsonify({
        'seo_tips': seo_tips
    })

if __name__ == '__main__':
    app.run(debug=True)
