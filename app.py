import http.cookiejar
import urllib.parse
import urllib.request
import requests
import time
import db
import threading
from flask import Flask, render_template


def start_runner():
    username = ''
    password = ''

    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))

    def login():
        payload = {
            'username': username,
            'password': password,
            'dst': '',
            'popup': 'true',
            'sendin': 'sendin'
        }

        payload = urllib.parse.urlencode(payload).encode("utf-8")
        try:
            opener.open("http://10.1.113.1/login", payload)
            db.write()
        except:
            db.write()

    def start_loop():
        while True:
            try:
                page = requests.get('http://10.1.113.1/status').text
                if not 'Welcome ' + username in page:
                    try:
                        login()
                    except:
                        login()
            except:
                db.write()

            time.sleep(1)

    print("Starting auto reconnect.")
    thread = threading.Thread(target=start_loop)
    thread.start()

app = Flask(__name__)


@app.route('/')
def index():
    dates, values = db.output()
    return render_template('index.html', dates=dates, values=values)

if __name__ == "__main__":
    start_runner()
    app.run(debug=False, host="127.0.0.1", port=6969)

