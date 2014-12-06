import os

import yaml
from flask import Flask, request, render_template, redirect, url_for, flash

import scores

config = yaml.load(file('config.yml', 'r'))

template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=template_dir)
app.secret_key = config['app']['secret_key']

@app.route('/')
def main():
    return render_template('login.html')

@app.route('/scores', methods=['POST'])
def login():
    data = scores.getScores(request.form['username'], request.form['password'], config)
    if data == -1:
        flash(config['messages']['credentials'])
        return redirect(url_for('main'))
    elif data == -2:
        flash(config['messages']['unavailable'])
        return redirect(url_for('main'))
    return render_template('results.html', data=data)

if __name__ == '__main__':
    app.run(host=config['server']['host'], port=config['server']['port'], debug=config['app']['debug'])
