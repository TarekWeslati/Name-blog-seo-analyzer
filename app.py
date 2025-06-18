from flask import Flask, render_template, request
import openai
import os

app = Flask(__name__)

# إعداد مفتاح API من البيئة
openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

# النموذج التحليلي للمقال
prompt_template = """
You are an expert SEO and content analyst.
Analyze the following blog article (in any language), and provide:

1. Tone analysis (Is it human, robotic, emotional, technical, boring?)
2. SEO structure review (headings, keyword usage, meta relevance)
3. Readability assessment (paragraph structure, sentence flow)
4. Content value (is it useful, repetitive, insightful?)
5. Heading structure analysis (are H2s and H3s clear and organized?)
6. Suggestions for improvement (detailed and practical)
7. Overall score from 100

Return the result in the same language as the input.
Article:
\"\"\"
{content}
\"\"\"
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        content = request.form["content"]
        if content:
            try:
                response = openai.ChatCompletion.create(
                    model="openrouter/gpt-4-turbo",
                    messages=[
                        {"role": "user", "content": prompt_template.format(content=content)}
                    ]
                )
                # قراءة النتيجة حسب بنية الاستجابة
                result = response['choices'][0]['message']['content']
            except Exception as e:
                # عرض الخطأ مباشرة في الصفحة
                result = f"❌ ERROR: {repr(e)}"
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
