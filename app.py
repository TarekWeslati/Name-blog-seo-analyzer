from flask import Flask, render_template, request
import re

app = Flask(__name__)

def analyze_text(content):
    word_count = len(content.split())
    keyword_suggestions = list(set(re.findall(r'\b\w{5,}\b', content)))[:10]
    fluff_percentage = min(round(content.lower().count('the') / word_count * 100, 2), 100) if word_count else 0
    return {
        'word_count': word_count,
        'fluff': fluff_percentage,
        'keywords': keyword_suggestions
    }

@app.route("/", methods=["GET", "POST"])
def index():
    analysis = {}
    blog_content = ""

    if request.method == "POST":
        blog_content = request.form.get("blogContent", "")
        analysis = analyze_text(blog_content)

    return render_template("index.html", blogContent=blog_content, analysis=analysis)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
