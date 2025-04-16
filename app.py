from flask import Flask, render_template, request
import re

app = Flask(__name__)

def count_words(text):
    words = re.findall(r'\w+', text)
    return len(words)

def keyword_density(text, keyword):
    words = re.findall(r'\w+', text.lower())
    total_words = len(words)
    keyword_count = words.count(keyword.lower())
    density = (keyword_count / total_words) * 100 if total_words > 0 else 0
    return keyword_count, round(density, 2)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        article = request.form['article']
        keyword = request.form['keyword']
        total_words = count_words(article)
        keyword_count, density = keyword_density(article, keyword)
        result = {
            'total_words': total_words,
            'keyword_count': keyword_count,
            'density': density,
            'keyword': keyword
        }
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
