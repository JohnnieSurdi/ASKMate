import string
from random import sample
import ast

def add_question_to_file(title,question,submission_time):
    question_dict = {}
    id = generate_id()
    view_number = 0
    vote_number = 0
    image = ''
    question_dict['id'] = id
    question_dict['submission_time'] = submission_time
    question_dict['view_number'] = view_number
    question_dict['vote_number'] = vote_number
    question_dict['title'] = title
    question_dict['message'] = question
    question_dict['image'] = image
    with open('C:/Users/kamci/projects/ask-mate-1-python-MichalProsniak/sample_data/question.csv', "a") as f:
        f.write(str(question_dict) + '\n')
    return id


def generate_id():
    chars = string.ascii_letters + string.digits
    length = 8
    return ''.join(sample(chars, length))

def read_all_questions_from_file():
    list_of_dicts = []
    with open('sample_data/question.csv') as data_file:
        for line in data_file:
            line = line.replace('\n', '')
            list_of_dicts.append(ast.literal_eval(line))
    return list_of_dicts