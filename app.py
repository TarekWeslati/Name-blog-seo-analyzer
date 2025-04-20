from flask import Flask, render_template, request
from collections import Counter
import re

app = Flask(__name__)

# أداة تحليل سيو المقال
def analyze_text(text):
    words = re.findall(r'\b\w+\b', text.lower())
    word_count = len(words)
    keyword_freq = Counter(words).most_common(10)
    fluff_words = [w for w in words if len(w) <= 2 or w in ['the', 'and', 'for', 'with']]
    fluff_ratio = round(len(fluff_words) / word_count * 100, 2) if word_count else 0
    return word_count, keyword_freq, fluff_ratio

# إقتراح عناوين H1 و H2 و H3 بناء على المحتوى

def suggest_headings(text):
    lines = text.split(". ")
    if len(lines) < 3:
        return {"h1": "Main Title", "h2": [], "h3": []}
    return {
        "h1": lines[0][:60],
        "h2": [l[:50] for l in lines[1:3]],
        "h3": [l[:40] for l in lines[3:6]]
    }

# إقتراح أماكن توزيع الكلمات المفتاحية

def keyword_placement_suggestions(keywords):
    suggestions = []
    if keywords:
        main_kw = keywords[0][0]
        suggestions.append(f"ضع الكلمة المفتاحية الرئيسية '{main_kw}' في العنوان الرئيسي h1.")
        suggestions.append(f"أدرج '{main_kw}' في أول فقرة وفي الوسوم ALT للصور.")
        for i, (kw, _) in enumerate(keywords[1:4], 1):
            suggestions.append(f"استخدم الكلمة '{kw}' مرة واحدة على الأقل في عنوان فرعي h2 أو h3.")
    return suggestions

# نصائح عامة لسيو المقال

def seo_tips(word_count, fluff_ratio):
    tips = []
    if word_count < 300:
        tips.append("المقال قصير جداً، حاول كتابة أكثر من 300 كلمة.")
    if fluff_ratio > 30:
        tips.append("نسبة الحشو مرتفعة، حاول تقليل الكلمات غير المفيدة.")
    tips.append("استخدم روابط داخلية وخارجية لتحسين السيو.")
    tips.append("احرص على تنسيق المقال بالعناوين والصور.")
    return tips

@app.route('/', methods=['GET', 'POST'])
def index():
    analysis = {}
    if request.method == 'POST':
        text = request.form['content']
        word_count, keyword_freq, fluff_ratio = analyze_text(text)
        headings = suggest_headings(text)
        placements = keyword_placement_suggestions(keyword_freq)
        tips = seo_tips(word_count, fluff_ratio)

        analysis = {
            'word_count': word_count,
            'keywords': keyword_freq,
            'fluff_ratio': fluff_ratio,
            'headings': headings,
            'placements': placements,
            'tips': tips,
        }

    return render_template('index.html', analysis=analysis)

if __name__ == '__main__':
    app.run(debug=True)
