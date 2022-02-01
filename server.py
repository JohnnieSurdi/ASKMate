from flask import Flask, render_template, request, redirect, url_for
import time
import data_manager
import connection

from datetime import datetime
def answer_path():
    #return 'sample_data/answer.csv'
    return 'C:/Users/kamci/projects/ask-mate-1-python-MichalProsniak/sample_data/answer.csv'

def question_path():
    #return 'sample_data/question.csv'
    return 'C:/Users/kamci/projects/ask-mate-1-python-MichalProsniak/sample_data/question.csv'

app = Flask(__name__)
adding_answer = {}


@app.route("/")
def home_page():
    q = connection.read_file(question_path())
    return f'{q}'


@app.route("/list")
def list_questions():
    data = connection.read_file(question_path())
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
        adding_answer['id'] = connection.create_new_id(answer_path())
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
    connection.delete_from_file(question_id)
    return redirect('/list')

@app.route("/question/<question_id>/edit", methods=['GET', 'POST'])
def edit_question(question_id):

    if request.method == 'GET':
        question_to_edit = connection.get_question_to_edit(question_id)
        return render_template('edit-question.html', question_to_edit=question_to_edit)
    if request.method == 'POST':
        edited_title = request.form.get('title')
        edited_question = request.form.get('question')
        new_submission_time = time.time()
        connection.edit_question_in_file(question_id,edited_title,edited_question,new_submission_time)
        return redirect('/list')

    pass

@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    question_id = connection.delete_from_file(answer_id, 'sample_data/answer.csv')
    return redirect('/question/'+str(question_id))



if __name__ == "__main__":
    app.run()
