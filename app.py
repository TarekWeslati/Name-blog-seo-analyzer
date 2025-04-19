from flask import Flask, render_template, request
import re
import os
from collections import Counter

app = Flask(__name__)

# دالة مبسطة لاستخراج الكلمات المفتاحية
def extract_keywords(text):
    words = re.findall(r'\b\w{4,}\b', text.lower())
    common = Counter(words).most_common(10)
    primary = common[0][0] if common else ""
    secondary = [word for word, count in common[1:5]]
    return primary, secondary

# دالة اقتراح العناوين
def suggest_headings(text):
    paragraphs = [p.strip() for p in text.split('\n') if len(p.strip()) > 20]
    headings = {
        "h1": paragraphs[0] if paragraphs else "Title Suggestion",
        "h2": paragraphs[1:3],
        "h3": paragraphs[3:6]
    }
    return headings

# دالة إعادة الصياغة بشكل بسيط
def simple_rewrite(text):
    sentences = re.split(r'(?<=[.!?]) +', text)
    rewritten = [s[::-1] for s in sentences if s]
    return ' '.join(rewritten[::-1])

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        article = request.form.get("article", "")

        total_words = len(article.split())
        primary_kw, secondary_kws = extract_keywords(article)
        keyword_count = article.lower().count(primary_kw.lower())
        density = round((keyword_count / total_words) * 100, 2) if total_words > 0 else 0

        headings = suggest_headings(article)
        rewritten = simple_rewrite(article)

        result = {
            "total_words": total_words,
            "primary_kw": primary_kw,
            "secondary_kws": secondary_kws,
            "keyword_count": keyword_count,
            "density": density,
            "headings": headings,
            "rewritten": rewritten
        }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
