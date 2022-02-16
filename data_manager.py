import datetime
import connection
import server


def list_prepare_question_to_show():
    headers = ["submission_time", "view_number", "vote_number", "title", "message"]
    data = connection.get_data_questions_sort_by_id()
    return headers, data


def slice_message(data):
    for element in data:
        if len(str(element['message'])) > 100:
            element['message'] = element['message'][:97]+'...'


def list_sort_question(data, order, direction):
    connection.sort_data(data, order, direction)


def question_display_by_id_with_answers(question_id):
    question = connection.get_data_question_with_id(question_id)
    answers = connection.get_data_answers_sort_by_vote_number(question_id)
    return question, answers


def add_question_to_file(title, question, image):
    submission_time = datetime.datetime.now()
    image_path = server.upload_image(image)
    connection.add_question_to_db(title, question, submission_time, image_path)
    question_id = connection.get_id(submission_time)
    return question_id


def add_comment_to_question(question_id, message):
    submission_time = datetime.datetime.now()
    edited_count = 0
    connection.add_comment_to_question(question_id, message, submission_time, edited_count)


def add_comment_to_answer(answer_id, message):
    submission_time = datetime.datetime.now()
    edited_count = 0
    connection.add_comment_to_answer(answer_id, message, submission_time, edited_count)


def add_answer_to_file(question_id, message, image):
    submission_time = datetime.datetime.now()
    image_path = server.upload_image(image)
    connection.add_answer_to_db(question_id, message, submission_time, image_path)
