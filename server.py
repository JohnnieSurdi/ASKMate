from flask import Flask, render_template, request, redirect, url_for
import time
import connection
import os
from werkzeug.utils import secure_filename
import data_handler


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
adding_answer = {}
UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_image(image):
    if image.filename == '':
        image_path = 'no_image'
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image.save(
            'C:/Users/kamci/projects/ask-mate-1-python-MichalProsniak/' + os.path.join(app.config['UPLOAD_FOLDER'],
                                                                                       filename))
        image_path = filename
    return image_path

def answer_path():
    #return 'sample_data/answer.csv'
    return 'C:/Users/kamci/projects/ask-mate-1-python-MichalProsniak/sample_data/answer.csv'


def question_path():
    #return 'sample_data/question.csv'
    return 'C:/Users/kamci/projects/ask-mate-1-python-MichalProsniak/sample_data/question.csv'


@app.route("/")
def home_page():
    return render_template('index.html')


@app.route("/list")
def list_questions():
    headers = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
    data = connection.read_file(question_path())
    data_sorted_by_id = sorted(data, key=lambda d: d['id'], reverse=True)
    return render_template('list.html', data=data_sorted_by_id, headers=headers)


@app.route('/question/<question_id>')
def route_question_by_id(question_id):
    answers = data_handler.get_answers_by_id(question_id)
    for answer in answers:
        answer.pop('question_id', None)
    question = data_handler.get_data_by_id(question_path(), question_id)
    return render_template('display_question_and_answers.html', question=question, answers=answers)


@app.route('/question/<question_id>/')
def route_question_view_count(question_id):
    question = data_handler.get_data_by_id(question_path(), question_id)
    question['view_number'] = str(int(question['view_number']) + 1)
    final_data = data_handler.edit_data(question_id, question, question_path())
    data_handler.data_writer(question_path(), final_data, data_handler.QUESTION_TITLE)
    return redirect(f'/question/{question_id}')


@app.route("/add-question", methods=['GET','POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add-question.html')
    elif request.method == 'POST':
        title = request.form.get('title')
        question = request.form.get('question')
        submission_time = time.time()
        image = request.files['image']
        image_path = upload_image(image)
        id = connection.add_question_to_file(title,question,submission_time,image_path)
        return redirect('/question/'+str(id))
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
        image = request.files['image']
        image_path = upload_image(image)
        adding_answer['image'] = image_path
        connection.write_new_answer_to_file(adding_answer)
        return redirect('/question/'+str(question_id))
    return render_template('add_new_answer.html', question_id=question_id)


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    connection.delete_from_file(question_id, question_path(),answer_path())
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
    question_id = connection.delete_answer_from_file(answer_id, answer_path())
    return redirect('/question/'+str(question_id))


@app.route("/question/<question_id>/vote_up")
def vote_up_question(question_id):
    connection.vote_up(question_path(), question_id)
    return redirect('/question/'+str(question_id))


@app.route("/question/<question_id>/vote_down")
def vote_down_question(question_id):
    connection.vote_down(question_path(), question_id)
    return redirect('/question/'+str(question_id))


@app.route("/answer/<answer_id>/vote_up")
def vote_up_answer(answer_id):
    question_id = connection.vote_up(answer_path(), answer_id)
    return redirect('/question/'+str(question_id))


@app.route("/answer/<answer_id>/vote_down")
def vote_down_answer(answer_id):
    question_id = connection.vote_down(answer_path(), answer_id)
    return redirect('/question/'+str(question_id))


if __name__ == "__main__":
    app.run()
