from flask import Flask, render_template, request, jsonify
from collections import Counter
import re

app = Flask(__name__)

def calculate_keyword_density(text):
    words = re.findall(r'\b\w+\b', text.lower())
    total_words = len(words)
    frequency = Counter(words)
    density = {word: (count / total_words) * 100 for word, count in frequency.items() if len(word) > 3}
    return density

def extract_keywords(text):
    words = re.findall(r'\b\w+\b', text.lower())
    frequency = Counter(words)
    keywords = [word for word, count in frequency.most_common(10) if len(word) > 4]
    return keywords

def suggest_headings(text):
    lines = text.split('\n')
    headings = []
    for line in lines:
        if len(line.strip()) > 15 and line[0].isupper():
            headings.append(line.strip())
    return headings[:5]

def seo_tips(text):
    tips = []
    word_count = len(re.findall(r'\b\w+\b', text))

    if word_count < 300:
        tips.append("Your article is too short. Aim for at least 500+ words.")
    else:
        tips.append("Good word count! Aim for 800+ words for better SEO.")

    if "<h1>" not in text.lower() and "<h2>" not in text.lower():
        tips.append("Add H1/H2 headings to improve readability and SEO.")

    if "alt=" not in text:
        tips.append("Add alt text to your images for better image SEO.")

    if "meta" not in text.lower():
        tips.append("Don't forget to add a meta description with keywords.")

    if len(tips) == 0:
        tips.append("Your content looks well-optimized!")

    return tips

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    content = request.json.get('content', '')
    word_count = len(re.findall(r'\b\w+\b', content))
    density = calculate_keyword_density(content)
    return jsonify({
        'word_count': word_count,
        'keyword_density': density
    })

@app.route('/keywords', methods=['POST'])
def keywords():
    content = request.json.get('content', '')
    return jsonify({
        'suggested_keywords': extract_keywords(content)
    })

@app.route('/headings', methods=['POST'])
def headings():
    content = request.json.get('content', '')
    return jsonify({
        'suggested_headings': suggest_headings(content)
    })

@app.route('/tips', methods=['POST'])
def tips():
    content = request.json.get('content', '')
    return jsonify({
        'seo_tips': seo_tips(content)
    })

if __name__ == '__main__':
    app.run(debug=True)
