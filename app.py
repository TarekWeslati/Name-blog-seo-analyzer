from flask import Flask, render_template, request
from collections import Counter
import re
import random

app = Flask(__name__)

def extract_keywords(text):
    words = re.findall(r'\b\w+\b', text.lower())
    stop_words = set(['the', 'and', 'to', 'of', 'in', 'a', 'is', 'it', 'for', 'on', 'with', 'that', 'this'])
    filtered_words = [w for w in words if w not in stop_words and len(w) > 3]
    freq = Counter(filtered_words)
    common = freq.most_common(5)
    return [kw for kw, _ in common]

def keyword_density(text, keyword):
    words = re.findall(r'\b\w+\b', text.lower())
    return round((words.count(keyword.lower()) / len(words)) * 100, 2) if words else 0

def seo_score(text, main_keyword):
    score = 0
    word_count = len(re.findall(r'\b\w+\b', text))
    if word_count >= 300:
        score += 30
    density = keyword_density(text, main_keyword)
    if 1 <= density <= 3:
        score += 30
    if text.count('\n') >= 3:
        score += 20
    if any(h in text.lower() for h in ['introduction', 'conclusion']):
        score += 20
    return score

def suggest_headings(text):
    lines = text.split('\n')
    h1 = lines[0] if lines else 'Main Title'
    h2 = lines[1:3]
    h3 = lines[3:6]
    return h1.strip(), [h.strip() for h in h2], [h.strip() for h in h3]

def suggest_improvements(text, keyword):
    suggestions = []
    if keyword_density(text, keyword) < 1.0:
        suggestions.append("Increase the usage of the main keyword.")
    if len(text.split()) < 300:
        suggestions.append("The article is too short. Try expanding your content.")
    if '\n' not in text:
        suggestions.append("Use headings to structure your content.")
    if not any(tag in text.lower() for tag in ['h1', 'h2', 'h3']):
        suggestions.append("Consider adding heading tags like H1, H2, H3.")
    return suggestions

def rewrite_article(text):
    # Simplified pseudo-rewriter for now
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    rewritten = ["In summary, " + s if i % 2 == 0 else "Moreover, " + s for i, s in enumerate(sentences)]
    return " ".join(rewritten)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form['content']
        main_keyword = extract_keywords(content)[0] if extract_keywords(content) else "N/A"
        secondary_keywords = extract_keywords(content)[1:4]
        density = keyword_density(content, main_keyword)
        score = seo_score(content, main_keyword)
        h1, h2_list, h3_list = suggest_headings(content)
        suggestions = suggest_improvements(content, main_keyword)
        rewritten = rewrite_article(content)
        
        return render_template('index.html',
                               content=content,
                               main_keyword=main_keyword,
                               secondary_keywords=secondary_keywords,
                               density=density,
                               score=score,
                               h1=h1,
                               h2_list=h2_list,
                               h3_list=h3_list,
                               suggestions=suggestions,
                               rewritten=rewritten)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
