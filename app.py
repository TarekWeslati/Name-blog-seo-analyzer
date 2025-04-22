from flask import Flask, render_template, request, jsonify
from collections import Counter
import re

app = Flask(__name__)

# Helper function to extract keywords
def extract_keywords(text):
    words = re.findall(r'\b\w{4,}\b', text.lower())
    common_words = set(['this', 'that', 'with', 'from', 'have', 'will', 'your', 'about', 'what', 'when', 'where'])
    filtered_words = [word for word in words if word not in common_words]
    keyword_counts = Counter(filtered_words)
    return keyword_counts.most_common(10)

# SEO suggestions engine
def seo_suggestions(text):
    suggestions = []
    if not re.search(r'<h1>.*?</h1>', text):
        suggestions.append("Add an H1 title to improve structure.")
    if len(text.split()) < 300:
        suggestions.append("Add more content (at least 300 words recommended).")
    if 'alt=' not in text:
        suggestions.append("Add alt text to images for better image SEO.")
    return suggestions

# Keyword placement suggestions
def keyword_distribution_suggestions(keyword):
    return {
        "title": f"Include the keyword '{keyword}' in the title tag.",
        "intro": f"Use the keyword '{keyword}' within the first 100 words.",
        "headings": f"Include '{keyword}' in at least one subheading.",
        "meta": f"Add '{keyword}' in your meta description."
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    content = request.form['content']
    keywords = extract_keywords(content)
    return jsonify({"keywords": keywords})

@app.route('/seo-tips', methods=['POST'])
def seo_tips():
    content = request.form['content']
    tips = seo_suggestions(content)
    return jsonify({"seo_tips": tips})

@app.route('/keyword-placement', methods=['POST'])
def keyword_placement():
    keyword = request.form['keyword']
    placement = keyword_distribution_suggestions(keyword)
    return jsonify(placement)

if __name__ == '__main__':
    app.run(debug=True)
    
