from flask import Flask, render_template, request
from collections import Counter
import re
import os

app = Flask(__name__)

def extract_keywords(text):
    words = re.findall(r'\b\w{4,}\b', text.lower())
    common = Counter(words).most_common(10)
    main_kw = common[0][0] if common else ""
    secondary = [w[0] for w in common[1:]]
    return main_kw, secondary

def generate_headings(text):
    sentences = text.split('.')
    headings = {
        "h1": sentences[0] if sentences else "",
        "h2": sentences[1] if len(sentences) > 1 else "",
        "h3": sentences[2] if len(sentences) > 2 else ""
    }
    return headings

def keyword_distribution(text, keywords):
    result = {}
    for kw in keywords:
        indices = [m.start() for m in re.finditer(kw, text.lower())]
        result[kw] = indices
    return result

@app.route("/", methods=["GET", "POST"])
def index():
    analysis = {}
    if request.method == "POST":
        article = request.form["article"]
        action = request.form.get("action")

        if action == "word_count":
            analysis["word_count"] = len(article.split())

        elif action == "extract_keywords":
            main_kw, secondary_kw = extract_keywords(article)
            analysis["main_keyword"] = main_kw
            analysis["secondary_keywords"] = secondary_kw

        elif action == "generate_headings":
            analysis["headings"] = generate_headings(article)

        elif action == "keyword_distribution":
            main_kw, secondary_kw = extract_keywords(article)
            all_keywords = [main_kw] + secondary_kw
            distribution = keyword_distribution(article, all_keywords)
            analysis["distribution"] = distribution

        return render_template("index.html", article=article, analysis=analysis)

    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
