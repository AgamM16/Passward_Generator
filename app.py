from flask import Flask, render_template, request, jsonify
from werkzeug.urls import url_quote
import random
import string
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_password', methods=['POST'])
def generate_password():
    try:
        length = int(request.form['length'])
        if length <= 0:
            return jsonify({'error': 'Please enter a valid positive length.'})
        else:
            password = generate_password_helper(length)
            save_to_history(password)
            return jsonify({'password': password})
    except ValueError:
        return jsonify({'error': 'Please enter a valid numeric length.'})

def generate_password_helper(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def save_to_history(password):
    with open("password_history.txt", "a") as file:
        file.write(password + "\n")

@app.route('/history')
def show_history():
    history = load_history()
    return render_template('history.html', history=history)

def load_history():
    if os.path.exists("password_history.txt"):
        with open("password_history.txt", "r") as file:
            return [line.strip() for line in file]
    else:
        return []

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

