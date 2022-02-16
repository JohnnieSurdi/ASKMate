import csv
import server
import os
from datetime import datetime
import database_common


@database_common.connection_handler
def delete_from_db(cursor, db_name, db_where, db_var):
    query = """
        DELETE FROM %s
        WHERE %s = '%s'""" % (db_name, db_where, db_var)
    cursor.execute(query)


@database_common.connection_handler
def get_images_by_id(cursor, db_name, id):
    query = """
        SELECT image
        FROM %s
        WHERE id = '%s'""" % (db_name, id)
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_data_questions_sort_by_id(cursor):
    query = """
        SELECT *
        FROM question
        ORDER BY id"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_data_question_with_id(cursor, question_id):
    query = """
        SELECT *
        FROM question
        WHERE id = %s
        ORDER BY id""" % (question_id)
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_data_answers_sort_by_vote_number(cursor,question_id):
    query = """
        SELECT *
        FROM answer
        WHERE question_id = '%s'
        ORDER BY vote_number DESC""" % (question_id)
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def add_question_to_db(cursor, title, question, submission_time, image_path):
    query = """
        INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
        VALUES ('%s','%s','%s','%s','%s','%s')""" % (submission_time, 0, 0, title, question, image_path)
    cursor.execute(query)


@database_common.connection_handler
def add_answer_to_db(cursor, question_id,message, submission_time, image_path):
    query = """
        INSERT INTO answer (submission_time, vote_number, question_id, message, image)
        VALUES ('%s','%s','%s','%s','%s')""" % (submission_time, 0, question_id, message, image_path)
    cursor.execute(query)


@database_common.connection_handler
def change_value_db(cursor, db_name, db_col, mark, db_where, db_where_equal):
    query = """
        UPDATE %s
        SET %s = %s %s 1
        WHERE %s = '%s'""" % (db_name, db_col, db_col, mark, db_where, db_where_equal)
    cursor.execute(query)


@database_common.connection_handler
def get_answer_id_connected_to_question(cursor, question_id):
    query = """
        SELECT id 
        FROM answer
        WHERE question_id = '%s'""" % (question_id)
    cursor.execute(query)
    lists = cursor.fetchall()
    list_to_return = [list['id'] for list in lists]
    return list_to_return


@database_common.connection_handler
def get_id(cursor, submission_time):
    query = """
        SELECT id FROM question
        WHERE submission_time = '%s'""" % (submission_time)
    cursor.execute(query)
    id = cursor.fetchall()
    id = list_of_dicts_to_str('id', id)
    return id


@database_common.connection_handler
def get_question_to_edit(cursor, question_id):
    query = """
        SELECT * FROM question
        WHERE id = '%s'""" % (question_id)
    cursor.execute(query)
    question = cursor.fetchall()
    question = question[0]
    return question


@database_common.connection_handler
def update_question(cursor, question_id, edited_title, edited_question):
    query = """
        UPDATE question
        SET title = '%s', message = '%s'
        WHERE id = '%s'""" % (edited_title, edited_question, question_id)
    cursor.execute(query)


@database_common.connection_handler
def get_from_db(cursor, db_select, db_name, db_where, db_var):
    query = """
        SELECT %s
        FROM %s
        WHERE %s = '%s'""" % (db_select, db_name, db_where, db_var)
    cursor.execute(query)
    var = cursor.fetchall()
    var = list_of_dicts_to_str(str(db_select),var)
    return var


@database_common.connection_handler
def get_title_by_id(cursor, question_id):
    query = """
        SELECT title FROM question
        WHERE id = '%s'""" % (question_id)
    cursor.execute(query)
    title = cursor.fetchall()
    title = list_of_dicts_to_str('title',title)
    return title

@database_common.connection_handler
def get_all_existing_tags(cursor):
    query = """
        SELECT name 
        FROM tag
        ORDER BY name"""
    cursor.execute(query)
    return cursor.fetchall()

def list_of_dicts_to_str(key,list):
    list = list[0]
    string = list[key]
    return string

def convert_order(order):
    if order == "from lowest":
        return 'ASC'
    elif order == "from highest":
        return 'DESC'

def convert_direction(direction):
    if direction == "Number of votes":
        return 'vote_number'
    elif direction == 'Submission time':
        return 'submission_time'
    elif direction == 'Title':
        return 'title'
    elif direction == 'Message':
        return 'message'
    elif direction == 'Number of views':
        return 'view_number'


@database_common.connection_handler
def sort_questions(cursor, direction, order):
    order = convert_order(order)
    direction = convert_direction(direction)
    query = """
            SELECT *
            FROM question
            ORDER BY %s %s""" % (direction, order)
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_tags_ids_for_question(cursor, question_id):
    query = """
            SELECT tag_id
            FROM question_tag
            WHERE question_id = %s""" % (question_id)
    cursor.execute(query)
    ids = cursor.fetchall()
    list_id = []
    for id in ids:
        list_id.append(id['tag_id'])
    return list_id


@database_common.connection_handler
def get_tag_by_id(cursor, id):
    query = """
            SELECT name
            FROM tag
            WHERE id = '%s'""" % (id)
    cursor.execute(query)
    tag = cursor.fetchall()
    tag = tag[0]
    tag_to_return = tag['name']
    return tag_to_return

@database_common.connection_handler
def get_id_by_tag(cursor, tag):
    query = """
            SELECT id
            FROM tag
            WHERE name = '%s'""" % (tag)
    cursor.execute(query)
    id = cursor.fetchall()
    id = id[0]
    id_to_return = id['id']
    return id_to_return


@database_common.connection_handler
def apply_tag_to_question(cursor, question_id,tag_id):
    query = """
            INSERT INTO question_tag (question_id,tag_id)
            VALUES (%s,%s)
            ON CONFLICT DO NOTHING""" % (question_id,tag_id)
    cursor.execute(query)

@database_common.connection_handler
def delete_tag_from_question(cursor, question_id,tag_id):
    query = """
            DELETE FROM question_tag
            WHERE question_id= '%s' AND tag_id = '%s'""" % (question_id, tag_id)
    cursor.execute(query)


@database_common.connection_handler
def add_new_defined_tags_to_db(cursor, new_defined_tags):
    query = """
            INSERT INTO tag (name)
            VALUES ('%s')
            """ % (new_defined_tags)
    cursor.execute(query)