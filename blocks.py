from flask import Flask, render_template, url_for, redirect, request, session

import config
import json

app = Flask(__name__)
app.config.from_object('config')

with open('blocks.json', 'r') as f:
    blocks = json.load(f)

def save_blocks():
    with open('blocks.json', 'w') as f:
        json.dump(blocks, f, indent=4)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        if 'enter' in request.form:
            pwd = request.form.get('pwd', None)
            if pwd == app.config['PASSWORD']:
                session['logged_in'] = True
                return redirect(url_for('.blocks_route'))
            else:
                return render_template('home.html', wrong_password=True)
    else:
        return render_template('home.html', wrong_password=False)


@app.route('/blocks', methods=['GET', 'POST'])
def blocks_route():
    if not 'logged_in' in session:
        return redirect(url_for('.home'))

    if request.method == "POST":
        if 'add' in request.form:
            blocks['count'] += 1
        elif 'remove' in request.form:
            blocks['count'] -= 1
        save_blocks()

    return render_template('blocks.html', blocks=blocks['count'])



app.run()
