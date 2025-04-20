from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        blog_content = request.form.get("blogContent", "")
        return render_template("index.html", blogContent=blog_content)
    return render_template("index.html", blogContent="")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
