from flask import Flask, request, render_template
import openai

app = Flask(__name__)

# ضع مفتاح OpenRouter API مباشرة هنا
openai.api_key = "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"
openai.api_base = "https://openrouter.ai/api/v1"

@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    if request.method == "POST":
        user_input = request.form["prompt"]
        try:
            response = openai.ChatCompletion.create(
                model="openai/gpt-4o",
                messages=[
                    {"role": "user", "content": user_input}
                ]
            )
            answer = response.choices[0].message["content"]
        except Exception as e:
            answer = f"Error: {e}"
    return render_template("index.html", answer=answer)
