from flask import Flask, render_template, request, redirect, url_for
import time
import data_manager
import connection

from datetime import datetime



app = Flask(__name__)
adding_answer = {}


@app.route("/")
def home_page():
    q = connection.read_file('C:/Users/kamci/projects/ask-mate-1-python-MichalProsniak/sample_data/question.csv')
    return f'{q}'


@app.route("/list")
def list_questions():
    data = connection.read_file('sample_data/question.csv')
    data_sorted_by_id = sorted(data, key=lambda d: d['id'], reverse=True)
    return render_template('list.html', data=data_sorted_by_id)


@app.route("/question/<question_id>")
def display_question(question_id):
    question = connection.display_question(question_id)
    answers = connection.get_answers_for_question(question_id)
    return render_template("display_question.html", question_id=question_id, question=question, answers=answers)



@app.route("/add-question", methods=['GET','POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add-question.html')
    elif request.method == 'POST':
        title = request.form.get('title')
        question = request.form.get('question')
        submission_time = time.time()
        id = connection.add_question_to_file(title,question,submission_time)
        return redirect(url_for('display_question',question_id=id))
    return "Hello World!"


@app.route("/question/<question_id>/new-answer", methods=['GET', 'POST'])
def add_answer(question_id):
    print(question_id)
    if request.method == 'POST':
        adding_answer['id'] = connection.create_new_id('sample_data/answer.csv')
        adding_answer['submission_time'] = time.time()
        adding_answer['vote_number'] = 0
        adding_answer['question_id'] = question_id
        adding_answer['message'] = request.form['new_answer']
        adding_answer['image'] = -1
        connection.write_new_answer_to_file(adding_answer)
        return redirect('/question/'+str(question_id))
    return render_template('add_new_answer.html', question_id=question_id)


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    connection.delete_question_from_file(question_id)
    return redirect('/list')


if __name__ == "__main__":
    app.run()
