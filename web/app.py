import io

import re
from flask import Flask, render_template, request, Response

app = Flask(__name__)


@app.route('/')
def hello_whale():
    return 'Whale 5 !'


@app.route('/hello')
def hello2():
    return 'Foobar'


@app.route('/user/<username>')
def show_user_profile(username):
    return 'User {}'.ormat(username)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post {}'.format(post_id)

# function voodoo() {
#    curl -F 'dmesg=@-' http://0.0.0.0:5000/$1
# }


class StringParser:
    def __init__(self, f: io.BytesIO):
        self.f = f
        self.lines = []
        self.buf = None

    def get_lines(self):
        while True:
            fs = self.next_line()
            if fs is not None:
                yield fs
            else:
                break

    def next_line(self):
        if len(self.lines) > 0:
            return self.lines.pop(0)
        else:
            s = self.f.read1(256).decode()
            if len(s) == 0:
                return None

            lines = s.split('\n')
            if self.buf is not None:
                lines[0] = self.buf + lines[0]
                self.buf = None

            if not s.endswith('\n'):
                self.lines = lines
            else:
                self.lines = lines[:-1]
                self.buf = lines[-1]

            return self.lines.pop(0)


@app.route('/audio', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['dmesg']

        p = StringParser(f.stream)
        for i in p.get_lines():
            # STORE LINE IN MONGODB
            if re.match(r'.*IOAudioEngine.*stop', i, re.IGNORECASE):
                return 'Audio engine stopped'

        return 'Audio engine still running'
    else:
        return 'Not Foobar'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
