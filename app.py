import openai
import os
import sys
from flask import Flask, render_template, request

# تأكد من ترميز UTF-8 لتجنب مشاكل الترميز
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__)

# قراءة وتنظيف مفتاح OpenRouter API
api_key = os.getenv("OPENROUTER_API_KEY", "").strip().replace('\u200e', '')
if not api_key:
    raise RuntimeError("❌ Missing or invalid OPENROUTER_API_KEY.")

# إعداد الاتصال بـ OpenRouter API
client = openai.OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

# نموذج الطلب المرسل لتحليل المقال
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
                response = client.chat.completions.create(
                    model="openrouter/gpt-4-turbo",
                    messages=[{"role": "user", "content": prompt_template.format(content=content)}]
                )
                result = response.choices[0].message.content
            except Exception as e:
                result = f"❌ ERROR: {repr(e)}"
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
