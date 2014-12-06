import os

from flask import Flask, request, render_template, redirect, url_for, flash

import scores

template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=template_dir)
app.secret_key = 'supersecret'

@app.route('/')
def main():
    return render_template('login.html')

@app.route('/scores', methods=['POST'])
def login():
    data = scores.getScores(request.form['username'], request.form['password'])
    if data is -1:
        flash('Invalid username or password')
    elif data is -2:
        flash("Your PSAT scores are unavailable. This method only works for select people.")
        return redirect(url_for('main'))
    return render_template('results.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
