import os

import yaml
from flask import Flask, request, render_template, redirect, url_for, flash

import scores

def path(name):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), name)

config = yaml.load(file(path('config.yml'), 'r'))

app = Flask(__name__, template_folder=path('templates'))
app.secret_key = config['app']['secret_key']

if config['app']['logging']:
    import logging
    file_handler = logging.FileHandler(filename=path('log.txt'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)


@app.route('/')
def main():
    return render_template('login.html')

@app.route('/scores', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return redirect(url_for('main'))
    data = scores.getScores(request.form['username'], request.form['password'], config)
    if data == -1:
        flash(config['messages']['credentials'])
        return redirect(url_for('main'))
    elif data == -2:
        flash(config['messages']['unavailable'])
        return redirect(url_for('main'))
    return render_template('results.html', data=data)

if __name__ == '__main__':
    if not config['server']['ssl']['enabled']:
        app.run(host=config['server']['host'], port=config['server']['port'], debug=config['app']['debug'])
    else:
        import ssl
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_cert_chain(path(config['server']['ssl']['certificate']), path(config['server']['ssl']['private_key']))
        app.run(host=config['server']['host'], port=config['server']['port'], debug=config['app']['debug'], ssl_context=context)
