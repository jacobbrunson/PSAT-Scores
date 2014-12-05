import os

from flask import Flask
from flask import request
from flask import render_template

import scores

template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=template_dir)

@app.route('/')
def main():
    return render_template('login.html')

@app.route('/scores', methods=['POST'])
def login():
    return render_template('results.html', data=scores.getScores(request.form['username'], request.form['password']))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
