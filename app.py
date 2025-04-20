from flask import Flask, render_template, request, jsonify
from collections import Counter
import re

app = Flask(__name__)

def extract_keywords(text):
    words = re.findall(r'\b\w+\b', text.lower())
    stopwords = set(['the', 'is', 'in', 'and', 'to', 'a', 'of', 'for', 'on', 'with', 'as', 'this', 'that'])
    filtered_words = [word for word in words if word not in stopwords and len(word) > 2]
    return Counter(filtered_words).most_common(10)

def suggest_headings(text):
    sentences = re.split(r'[.!?]', text)
    return [s.strip().capitalize() for s in sentences if len(s.strip()) > 20][:5]

def seo_tips(text):
    word_count = len(re.findall(r'\b\w+\b', text))
    keyword_suggestions = extract_keywords(text)
    tips = []
    if word_count < 300:
        tips.append("Increase your content length to at least 300 words.")
    if len(keyword_suggestions) == 0:
        tips.append("Add relevant keywords to improve SEO.")
    else:
        tips.append("Ensure keywords are included in title, headers, and first paragraph.")
    return tips

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    content = request.form['content']
    word_count = len(re.findall(r'\b\w+\b', content))
    keywords = extract_keywords(content)
    headings = suggest_headings(content)
    tips = seo_tips(content)

    response = {
        'word_count': word_count,
        'keywords': keywords,
        'headings': headings,
        'tips': tips,
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
    
