import re
from flask import Flask, render_template, request

app = Flask(__name__)

# تحليل النص
def analyze_text(content):
    word_count = len(content.split())
    keyword_suggestions = list(set(re.findall(r'\b\w{5,}\b', content)))[:10]
    fluff_percentage = min(round(content.lower().count('the') / word_count * 100, 2), 100) if word_count else 0
    return {
        'word_count': word_count,
        'fluff': fluff_percentage,
        'keywords': keyword_suggestions
    }

# إعادة الصياغة (بدون OpenAI)
def simple_rephrase(content):
    words = content.split()
    if len(words) > 10:
        # إعادة ترتيب الجمل بشكل بسيط لتغيير هيكل النص
        words = words[::-1]  # هذا هو المثال الأبسط: عكس ترتيب الكلمات
    return ' '.join(words)

@app.route("/", methods=["GET", "POST"])
def index():
    analysis = {}
    blog_content = ""
    rephrased_content = ""

    if request.method == "POST":
        blog_content = request.form.get("blogContent", "")
        action = request.form.get("action", "")

        # تحليل النص
        analysis = analyze_text(blog_content)

        # إعادة الصياغة إذا تم اختيار ذلك
        if action == "rephrase":
            rephrased_content = simple_rephrase(blog_content)

    return render_template("index.html", blogContent=blog_content, analysis=analysis, rephrased_content=rephrased_content)

if __name__ == "__main__":
    app.run(debug=True)
    
