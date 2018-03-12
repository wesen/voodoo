import io

import re
from flask import Flask, render_template, request, Response

app = Flask(__name__)


@app.route('/')
def index():
    return 'audio - parse macosx dmesg for audio engine stops'


@app.route('/audio/description')
def audio_description():
    return """audio - parse macosx dmesg for audio engine stops
    
Usage:
   sudo dmesg | voodoo audio
"""


@app.route('/audio', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['data']

        while True:
            b = f.stream.readline()
            if len(b) == 0:
                break
            i = b.decode()
            if re.match(r'.*IOAudioEngine.*stop', i, re.IGNORECASE):
                return 'Audio engine stopped'

        return 'Audio engine still running'
    else:
        return 'Not Foobar'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
