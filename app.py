from flask import Flask, request, render_template
import re
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'HEAD'])
def index():
    if request.method == 'HEAD':
        return '', 200

    result = None
    if request.method == 'POST':
        article = request.form.get('article', '')
        keyword = request.form.get('keyword', '')
        
        total_words = len(article.split())
        keyword_count = len(re.findall(re.escape(keyword), article, re.IGNORECASE))
        density = round((keyword_count / total_words) * 100, 2) if total_words > 0 else 0

        result = {
            'total_words': total_words,
            'keyword': keyword,
            'keyword_count': keyword_count,
            'density': density
        }

    return render_template('index.html', result=result)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
