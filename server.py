from flask import Flask, render_template, request, redirect, url_for
import time
import data_manager


from datetime import datetime

app = Flask(__name__)


@app.route("/")
def home_page():
    return "Hello World!"

@app.route("/list")
def list_questions():
    return "Hello World!"

@app.route("/question/<question_id>")
def display_question():
    return "Hello World!"

@app.route("/add-question", methods=['GET','POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add-question.html')
    elif request.method == 'POST':
        title = request.form.get('title')
        question = request.form.get('question')
        timestamp = time.time()

        return render_template('index.html')
    return "Hello World!"

@app.route("/question/<question_id>/new-answer")
def add_answer():
    return "Hello World!"


if __name__ == "__main__":
    app.run()
