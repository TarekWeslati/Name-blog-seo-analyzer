from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# أدخل مفتاحك هنا مباشرة
api_key = "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"

client = openai.OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

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
                    messages=[
                        {"role": "user", "content": prompt_template.format(content=content)}
                    ]
                )
                result = response.choices[0].message.content
            except Exception as e:
                result = f"❌ ERROR: {repr(e)}"
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
