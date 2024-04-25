
from flask import Flask, render_template, request, redirect, url_for
from shorten_url import URLShortener


app = Flask(__name__)

shortener = URLShortener()

def sanitize_url(url):
    forbidden_chars = ['@', '?', '{', '}', "\\", '|', ' ']
    for char in forbidden_chars:
        if char in url:
            return None, f"URL cannot contain '{char}'"
    if url.startswith('http://'):
        url = 'https://' + url[len('http://'):]
    elif not url.startswith('https://'):
        url = 'https://' + url
    return url, None

@app.route('/', methods=['GET', 'POST'])
def index():
    original_url = None
    short_url = None
    error_message = None
    if request.method == 'POST':
        original_url = request.form['url']
        original_url, error_message = sanitize_url(original_url)
        if error_message is None:
            short_code = shortener.shorten_url(original_url)
            short_url = short_code
        else: 
            return render_template('index.html', original_url=original_url, short_url=short_url, error_message=error_message)
    return render_template('index.html', original_url=original_url, short_url=short_url, error_message=error_message) 

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
