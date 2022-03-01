import datetime
import connection
import server
import bcrypt
import database_common


def list_prepare_question_to_show():
    headers = ["name", "submission_time", "view_number", "vote_number", "title", "message"]
    data = connection.get_data_questions_sort_by_id()
    return headers, data


def slice_message(data):
    for element in data:
        if len(str(element['message'])) > 100:
            element['message'] = element['message'][:97] + '...'


def list_sort_question(data, order, direction):
    connection.sort_data(data, order, direction)


def question_display_by_id_with_answers(question_id):
    question = connection.get_data_question_with_id(question_id)
    answers = connection.get_data_answers_sort_by_vote_number(question_id)
    comments_to_questions = connection.get_data_comments(question_id)
    return question, answers, comments_to_questions


def get_comments_for_answers(list_with_answer_id):
    list_with_comments = []
    for answer_id in list_with_answer_id:
        comments_to_answers = connection.get_comments_for_answers(answer_id)
        list_with_comments.append(comments_to_answers)
    return list_with_comments


def add_question_to_file(title, question, image):
    submission_time = datetime.datetime.now()
    image_path = server.upload_image(image)
    connection.add_question_to_db(title, question, submission_time, image_path)
    question_id = connection.get_id(submission_time)
    return question_id


def add_answer_to_file(question_id, message, image):
    submission_time = datetime.datetime.now()
    image_path = server.upload_image(image)
    connection.add_answer_to_db(question_id, message, submission_time, image_path)


def get_tags_for_question(question_id):
    tags_id_for_question = connection.get_tags_ids_for_question(question_id)
    tags = []
    for id in tags_id_for_question:
        tags.append(connection.get_tag_by_id(id))
    return tags


def add_new_defined_tags(new_defined_tags, question_id):
    existing_tags = connection.get_all_existing_tags()
    existing_tags_list = []
    for tags in existing_tags:
        existing_tags_list.append(tags['name'])
    print(existing_tags_list)
    if ',' in new_defined_tags:
        new_defined_tags = new_defined_tags.split(',')
        for tag in new_defined_tags:
            tag = tag.strip()
            if tag != '' and tag not in existing_tags_list:
                connection.add_new_defined_tags_to_db(tag)
                tag_id = connection.get_id_by_tag(tag)
                connection.apply_tag_to_question(question_id, tag_id)
    else:
        new_defined_tags = new_defined_tags.strip()
        if new_defined_tags != '' and new_defined_tags not in existing_tags_list:
            connection.add_new_defined_tags_to_db(new_defined_tags)
            tag_id = connection.get_id_by_tag(new_defined_tags)
            connection.apply_tag_to_question(question_id, tag_id)


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


def list_prepare_users_to_show():
    headers = ["user_name", "registration_date", "number_of_asked_questions", "number_of_answers", "number_of_comments",
               "reputation"]
    users_data = connection.get_all_users_data()
    return headers, users_data


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


def user_registration(username, password):
    password = hash_password(password)
    is_username_taken = connection.check_if_user_exist(username)
    registration_date = datetime.datetime.now()
    if not is_username_taken:
        connection.add_new_user_to_db(username, password, registration_date)
        return is_username_taken
    else:
        return is_username_taken


def user_profile_page(user_id):
    user_data = connection.get_user_data_by_id(user_id)
    num_questions = connection.get_number_of_questions_by_user_id(user_id)
    num_answers = connection.get_number_of_answers_by_user_id(user_id)
    num_comments = connection.get_number_of_comments_by_user_id(user_id)
    user_data['num_questions'] = num_questions
    user_data['num_answers'] = num_answers
    user_data['num_comments'] = num_comments
    user_questions = connection.get_user_questions(user_id)
    user_answers = connection.get_user_answers(user_id)
    user_comments = connection.get_user_comments(user_id)
    return user_data, user_questions, user_answers, user_comments


def is_logged(ses):
    alert = True
    if 'username' in ses:
        alert = False
    return alert