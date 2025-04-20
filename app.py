import openai
from flask import Flask, render_template, request
import os
from pytrends.request import TrendReq

# إعداد مفتاح API من OpenAI
openai.api_key = "YOUR_OPENAI_API_KEY"  # ضع هنا مفتاح OpenAI الخاص بك

app = Flask(__name__)

# إعداد Pytrends
pytrends = TrendReq(hl='ar', tz=360)

# دالة لإعادة صياغة النص باستخدام OpenAI
def rephrase_text(text):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"إعادة صياغة النص التالي بشكل أفضل:\n\n{text}",
            max_tokens=1000
        )
        return response.choices[0].text.strip()  # إعادة النص المعاد صياغته
    except Exception as e:
        return f"خطأ في الاتصال بـ OpenAI: {str(e)}"

# دالة لتحليل سيو النص
def analyze_text(text):
    word_count = len(text.split())
    fluff_percentage = 0
    keywords = extract_keywords_from_trends(text)  # استخراج الكلمات المفتاحية من تريند
    return {
        "word_count": word_count,
        "fluff": fluff_percentage,
        "keywords": keywords
    }

# دالة لاستخراج الكلمات المفتاحية من جوجل تريند
def extract_keywords_from_trends(text):
    pytrends.build_payload([text], cat=0, timeframe='now 1-d', geo='US', gprop='')
    related_queries = pytrends.related_queries()
    
    if text in related_queries:
        return related_queries[text]['top'].head(5).to_dict()['query']
    return ["لا توجد كلمات مفتاحية مرتبطة بهذا النص"]

@app.route("/", methods=["GET", "POST"])
def index():
    blog_content = ""
    analysis = None
    rephrased_content = None

    if request.method == "POST":
        blog_content = request.form.get("blogContent")
        action = request.form.get("action")

        # تحليل النص إذا تم إرساله
        if blog_content:
            analysis = analyze_text(blog_content)

        # إذا كان المستخدم يريد إعادة الصياغة
        if action == "rephrase" and blog_content:
            rephrased_content = rephrase_text(blog_content)

    return render_template("index.html", blogContent=blog_content, analysis=analysis, rephrased_content=rephrased_content)

if __name__ == "__main__":
    app.run(debug=True)
