from flask import Flask, render_template, request, redirect
import connection
import os
from werkzeug.utils import secure_filename
import data_manager



ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = 'static/uploads/'
app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


# allowed file extension for file uploads
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# upload image on server
def upload_image(image):
    if image.filename == '':
        image_path = 'no_image'
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        image_path = filename
    return image_path



# load home page
@app.route("/")
def home_page():
    headers, data_questions = data_manager.list_prepare_question_to_show()
    order = 'Submission time'
    direction = "from highest"
    data_questions = connection.sort_questions(order, direction)
    data_five_questions = data_questions[:5]
    return render_template('index.html', data=data_five_questions, headers=headers)


# load question list page
@app.route("/list")
def list_questions():
    headers, data_questions = data_manager.list_prepare_question_to_show()
    order = request.args.get('order_by')
    direction = request.args.get('order_direction')
    if order or direction:
        data_questions = connection.sort_questions(order, direction)
    return render_template('list.html', data=data_questions, headers=headers)


# load question detail page
@app.route('/question/<question_id>')
def question_display(question_id):
    connection.change_value_db('question', 'view_number', '+', 'id', question_id)
    question, answers = data_manager.question_display_by_id_with_answers(question_id)
    return render_template('display_question_and_answers.html', question=question[0], answers=answers)


# load add question page
@app.route("/add-question", methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add-question.html')
    title = request.form.get('title')
    question = request.form.get('question')
    image = request.files['image']
    question_id = data_manager.add_question_to_file(title, question, image)
    return redirect('/question/' + str(question_id))


# add new answer to question
@app.route("/question/<question_id>/new-answer", methods=['GET', 'POST'])
def add_answer(question_id):
    if request.method == 'POST':
        message = request.form['new_answer']
        image = request.files['image']
        data_manager.add_answer_to_file(question_id, message, image)
        return redirect('/question/' + str(question_id))
    title = connection.get_title_by_id(question_id)
    return render_template('add_new_answer.html', question_id=question_id, title=title)


# delete question
@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    images_to_delete = []
    images_to_delete.append(connection.get_from_db('image', 'question', 'id', question_id))
    answers_id = connection.get_answer_id_connected_to_question(question_id)
    for id in answers_id:
        images_to_delete.append(connection.get_from_db('image', 'answer', 'id', id))
        connection.delete_from_db('comment', 'answer_id', id)
    for image in images_to_delete:
        if os.path.isfile(f"static/uploads/{image}"):
            os.remove(f"static/uploads/{image}")
    connection.delete_from_db('comment', 'question_id', question_id)
    connection.delete_from_db('question_tag', 'question_id', question_id)
    connection.delete_from_db('answer', 'question_id', question_id)
    connection.delete_from_db('question', 'id', question_id)
    return redirect('/list')


# edit question
@app.route("/question/<question_id>/edit", methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == 'GET':
        question_to_edit = connection.get_question_to_edit(question_id)
        return render_template('edit-question.html', question_to_edit=question_to_edit)
    edited_title = request.form.get('title')
    edited_question = request.form.get('question')
    connection.update_question(question_id, edited_title, edited_question)
    return redirect('/list')


# delete answer
@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    image_to_delete = connection.get_from_db('image', 'answer', 'id', answer_id)
    if os.path.isfile(f"static/uploads/{image_to_delete}"):
        os.remove(f"static/uploads/{image_to_delete}")
    question_id = connection.get_from_db('question_id', 'answer', 'id', answer_id)
    connection.delete_from_db('answer', 'id', answer_id)
    connection.delete_from_db('comment', 'answer_id', answer_id)
    return redirect('/question/' + str(question_id))


@app.route("/question/<question_id>/vote_up")
def vote_up_question(question_id):
    connection.change_value_db('question', 'vote_number', '+', 'id', question_id)
    connection.change_value_db('question', 'view_number', '-', 'id', question_id)
    return redirect('/question/' + str(question_id))


@app.route("/question/<question_id>/vote_down")
def vote_down_question(question_id):
    connection.change_value_db('question', 'vote_number', '-', 'id', question_id)
    connection.change_value_db('question', 'view_number', '-', 'id', question_id)
    return redirect('/question/' + str(question_id))


@app.route("/answer/<answer_id>/vote_up")
def vote_up_answer(answer_id):
    connection.change_value_db('answer', 'vote_number', '+', 'id', answer_id)
    question_id = connection.get_from_db('question_id', 'answer', 'id', answer_id)
    connection.change_value_db('question', 'view_number', '-', 'id', question_id)
    return redirect('/question/' + str(question_id))


@app.route("/answer/<answer_id>/vote_down")
def vote_down_answer(answer_id):
    connection.change_value_db('answer', 'vote_number', '-', 'id', answer_id)
    question_id = connection.get_from_db('question_id', 'answer', 'id', answer_id)
    connection.change_value_db('question', 'view_number', '-', 'id', question_id)
    return redirect('/question/' + str(question_id))


@app.route("/show_image/<image>/<question_id>")
def show_image(image, question_id):
    return render_template('show_image.html', image=image, question_id=question_id)


# delete comment
@app.route("/comments/<comment_id>/delete")
def delete_comment(comment_id):
    question_id = connection.get_from_db("question_id", "comment", "comment_id", comment_id)
    connection.delete_from_db('comment', 'comment_id', comment_id)
    return redirect('/question/' + str(question_id))


if __name__ == "__main__":
    app.run()
