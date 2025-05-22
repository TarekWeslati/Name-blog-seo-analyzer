from flask import Flask, render_template, request
import re
import requests
import os

app = Flask(__name__)

# ضع مفتاح OpenRouter API هنا
OPENROUTER_API_KEY = "sk-or-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

def analyze_seo(article, keyword):
    word_count = len(re.findall(r'\w+', article))
    keyword_count = len(re.findall(r'\b' + re.escape(keyword) + r'\b', article, re.IGNORECASE))
    keyword_density = (keyword_count / word_count) * 100 if word_count > 0 else 0
    h1_count = len(re.findall(r'<h1.*?>.*?</h1>', article, re.IGNORECASE))
    h2_count = len(re.findall(r'<h2.*?>.*?</h2>', article, re.IGNORECASE))

    tips = []
    if word_count < 300:
        tips.append("🔴 المقال قصير جدًا. حاول كتابة أكثر من 300 كلمة.")
    if keyword_density < 1:
        tips.append("🟡 كثافة الكلمة المفتاحية منخفضة. حاول استخدامها أكثر.")
    elif keyword_density > 3:
        tips.append("🟡 كثافة الكلمة المفتاحية عالية جدًا. قد يعتبرها جوجل حشوًا.")
    else:
        tips.append("✅ كثافة الكلمة المفتاحية ممتازة.")
    if h1_count == 0:
        tips.append("🟡 لا يوجد عنوان H1. يجب تضمين عنوان رئيسي.")
    if h2_count < 2:
        tips.append("🟡 من الأفضل استخدام أكثر من عنوان فرعي (H2).")

    return {
        "word_count": word_count,
        "keyword_count": keyword_count,
        "keyword_density": round(keyword_density, 2),
        "h1_count": h1_count,
        "h2_count": h2_count,
        "tips": tips
    }

def improve_article(article, keyword):
    prompt = f"""أنت مساعد SEO محترف. قم بتحسين المقال التالي ليكون متوافقًا مع معايير السيو ومحسّنًا للظهور في محركات البحث. 
اجعل الكلمة المفتاحية "{keyword}" تظهر بكثافة مناسبة، مع تحسين العناوين والوضوح.

المقال الأصلي:
{article}
"""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5000",  # أو موقعك لاحقًا
        "X-Title": "SEO Analyzer"
    }

    data = {
        "model": "openai/gpt-4o",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"❌ خطأ في الاتصال بـ GPT-4: {response.text}"

@app.route("/", methods=["GET", "POST"])
def index():
    analysis = None
    improved_article = None
    if request.method == "POST":
        article = request.form["article"]
        keyword = request.form["keyword"]
        improve = request.form.get("improve")  # إرجاع None إذا لم يتم تحديده

        analysis = analyze_seo(article, keyword)

        if improve:
            improved_article = improve_article(article, keyword)

    return render_template("index.html", analysis=analysis, improved_article=improved_article)

if __name__ == "__main__":
    app.run(debug=True)
