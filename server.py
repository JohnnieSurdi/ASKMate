from flask import Flask, render_template, request, redirect, url_for
import time
import data_manager

from datetime import datetime

app = Flask(__name__)
adding_answer = {}


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
        submission_time = time.time()
        id = data_manager.add_question_to_file(title,question,submission_time)
        return redirect(url_for('display_question',question_id=id))
    return "Hello World!"


@app.route("/question/<question_id>/new-answer", methods=['GET', 'POST'])
def add_answer(question_id):
    if request.method == 'POST':
        adding_answer['id'] = 1
        adding_answer['submission_time'] = 1
        adding_answer['vote_number'] = 0
        adding_answer['question_id'] = question_id
        adding_answer['message'] = request.form['new_answer']
        adding_answer['image'] = ""
        return redirect('/question/<question_id>')
    return render_template('add_new_answer.html')


if __name__ == "__main__":
    app.run()
