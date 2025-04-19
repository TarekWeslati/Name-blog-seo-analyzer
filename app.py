import openai
import re
from flask import Flask, render_template, request
import os

# إعداد API Key لـ OpenAI (تأكد من أنك أضفت مفتاح OpenAI في بيئة التشغيل)
openai.api_key = "YOUR_OPENAI_API_KEY"

app = Flask(__name__)

# دالة تحليل السيو
def seo_analysis(content):
    # استخراج الكلمة الرئيسية
    main_keyword = extract_main_keyword(content)
    # استخراج الكلمات الثانوية
    secondary_keywords = extract_secondary_keywords(content)
    # حساب كثافة الكلمات المفتاحية
    density = calculate_keyword_density(content, main_keyword)
    # تقديم العناوين H1، H2، H3
    headings = suggest_headings(content)
    # حساب درجة سيو بسيطة
    score = calculate_seo_score(content, main_keyword)

    # تحسينات مقترحة (مثال بسيط)
    suggestions = []
    if density < 1.5:
        suggestions.append("Increase the keyword density for better SEO.")
    if len(headings['h1']) == 0:
        suggestions.append("Consider adding a clear H1 tag.")

    return {
        "main_keyword": main_keyword,
        "secondary_keywords": secondary_keywords,
        "density": density,
        "headings": headings,
        "score": score,
        "suggestions": suggestions
    }

# دالة استخراج الكلمة الرئيسية
def extract_main_keyword(content):
    # من الممكن تحسين هذا بإضافة خوارزميات متقدمة
    words = content.split()
    most_frequent = max(set(words), key = words.count)
    return most_frequent

# دالة استخراج الكلمات الثانوية
def extract_secondary_keywords(content):
    # هنا يمكن استخدام أدوات أكثر تطورًا لاستخراج الكلمات الثانوية
    return ["example", "secondary", "keyword"]

# دالة حساب كثافة الكلمات
def calculate_keyword_density(content, keyword):
    words = content.split()
    keyword_count = words.count(keyword)
    return (keyword_count / len(words)) * 100

# دالة اقتراح العناوين
def suggest_headings(content):
    # باستخدام قاعدة بيانات بسيطة للعناوين
    headings = {
        "h1": "Blog SEO Best Practices",
        "h2": ["Keyword Strategy", "Content Optimization"],
        "h3": ["How to Choose Keywords", "Avoid Keyword Stuffing"]
    }
    return headings

# دالة حساب درجة السيو
def calculate_seo_score(content, main_keyword):
    density = calculate_keyword_density(content, main_keyword)
    return min(int(density * 2), 100)

# دالة لإعادة صياغة المقال باستخدام OpenAI API
def rewrite_article_with_ai(text):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Rewrite the following article to improve clarity and readability:\n\n{text}",
            max_tokens=1500
        )
        rewritten_text = response.choices[0].text.strip()
        return rewritten_text
    except Exception as e:
        print(f"Error in OpenAI API: {e}")
        return text  # إذا حدث خطأ، نعيد النص كما هو

# الصفحة الرئيسية
@app.route("/", methods=["GET", "POST"])
def index():
    content = request.form.get("content")
    seo_results = None
    rewritten_article = ""
    
    if content:
        seo_results = seo_analysis(content)
        rewritten_article = rewrite_article_with_ai(content)

    return render_template("index.html", content=content, rewritten=rewritten_article, **seo_results)

if __name__ == "__main__":
    app.run(debug=True)
