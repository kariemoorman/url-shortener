
from flask import Flask, render_template, request, redirect, url_for
from shorten_url import URLShortener


app = Flask(__name__)

shortener = URLShortener()

@app.route('/', methods=['GET', 'POST'])
def index():
    original_url = None
    short_url = None
    if request.method == 'POST':
        original_url = request.form['url']
        short_code = shortener.shorten_url(original_url)
        short_url = short_code
    return render_template('index.html', original_url=original_url, short_url=short_url)

@app.route('/<short_code>')
def redirect_to_original_url(short_code):
    original_url = shortener.get_original_url(short_code)
    if original_url:
        print(original_url)
        return redirect(original_url)
    else:
        return "URL not found", 404

if __name__ == '__main__':
    app.run(debug=True)
