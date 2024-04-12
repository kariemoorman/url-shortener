import argparse
import string
import random
import sqlite3

class URLShortener:
    def __init__(self):
        self.db_file = 'url_shortener.db'
        self._create_table_if_not_exists()
        self.tld = 'https://xyz.lol/'

    def _create_table_if_not_exists(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS url_mapping
                     (short_code TEXT PRIMARY KEY, original_url TEXT)''')
        conn.commit()
        conn.close()

    def generate_short_code(self, length=6):
        characters = string.ascii_letters + string.digits
        short_code = ''.join(random.choice(characters) for _ in range(length))
        output = f'{self.tld}{short_code}'
        return output

    def shorten_url(self, url):
        short_code = self.generate_short_code()
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("INSERT INTO url_mapping (short_code, original_url) VALUES (?, ?)", (short_code, url))
        conn.commit()
        conn.close()
        return short_code

    def get_original_url(self, short_code):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT original_url FROM url_mapping WHERE short_code=?", (short_code,))
        row = c.fetchone()
        conn.close()
        return row[0] if row else None

def main(): 
    parser = argparse.ArgumentParser(description='URL Shortener')
    parser.add_argument('--url', '-u', type=str, help='URL')
    args = parser.parse_args()
    
    shortener = URLShortener()
    short_code = shortener.shorten_url(args.url)
    original_url = shortener.get_original_url(short_code)
    print("Original URL:", original_url)
    print("Shortened URL:", short_code)

if __name__ == '__main__':
    main()
