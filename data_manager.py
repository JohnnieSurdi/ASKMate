import datetime
import connection
import server
from psycopg2.extras import RealDictCursor


def list_prepare_question_to_show():
    headers = ["submission_time", "view_number", "vote_number", "title", "message"]
    data = connection.get_data_questions_sort_by_id()
    return headers, data

def slice_message(data):
    for element in data:
        if len(str(element['message'])) > 100:
            element['message'] = element['message'][:97]+'...'


def list_sort_question(data,order,direction):
    connection.sort_data(data, order, direction)



