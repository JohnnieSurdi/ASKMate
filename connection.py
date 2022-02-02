import csv
import server
import os


def write_new_answer_to_file(new_answer):
    with open(server.answer_path(), 'a', newline='') as csvfile:
        fieldnames = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'id': new_answer['id'], 'submission_time': new_answer['submission_time'],
                         'vote_number': new_answer['vote_number'], 'question_id': new_answer['question_id'],
                         'message': new_answer['message'], 'image': new_answer['image']})


def create_new_id(file):
    data_list = read_file(file)
    new_id = len(data_list) + 1
    return new_id


def add_question_to_file(title, question, submission_time, image):
    file = server.question_path()
    new_id = create_new_id(file)
    view_number = 0
    vote_number = 0
    with open(server.question_path(), 'a', newline='') as csvfile:
        fieldnames = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'id': new_id, 'submission_time': submission_time, 'view_number': view_number,
                         'vote_number': vote_number, 'title': title, 'message': question, 'image': image})
    return new_id


def delete_item_from_list(data_id, data_list):
    list_updated = []
    for item in data_list:
        if item['id'] == data_id:
            if len(item) == 6:
                question_id = item['question_id']
            continue
        else:
            list_updated.append(item)
    if len(data_list[0]) == 6:
        return list_updated, question_id
    else:
        return list_updated


def delete_item_from_answers(data_id, data_list):
    list_updated = []
    for item in data_list:
        if item['question_id'] == data_id:
            continue
        else:
            list_updated.append(item)
    return list_updated


def delete_from_file(data_id, file_questions, file_answers):
    question_list = read_file(file_questions)
    answer_list = read_file(file_answers)
    if len(question_list[0]) == 6:
        question_list_updated, question_id = delete_item_from_list(data_id, question_list)
    else:
        question_list_updated = delete_item_from_list(data_id, question_list)
        answer_list_updated = delete_item_from_answers(data_id, answer_list)
    update_file(file_questions, question_list_updated)
    update_answers_question_id(file_answers, answer_list_updated,data_id)
    if len(question_list[0]) == 6:
        return question_id


def update_answers_question_id(file, list_updated,data_id):
    with open(file, 'w', newline='') as csvfile:
        if len(list_updated) > 0:
            fieldnames = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for item in list_updated:
                if item['question_id'] >= data_id:
                    writer.writerow({'id': item['id'], 'submission_time': item['submission_time'],
                                     'vote_number': item['vote_number'], 'question_id': str(int(item['question_id']) - 1),
                                     'message': item['message'], 'image': item['image']})
                else:
                    writer.writerow({'id': item['id'], 'submission_time': item['submission_time'],
                                     'vote_number': item['vote_number'],
                                     'question_id': item['question_id'],
                                     'message': item['message'], 'image': item['image']})
        else:
            fieldnames = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()


def update_file(file, list_updated):
    with open(file, 'w', newline='') as csvfile:
        if len(list_updated) > 0:
            if len(list_updated[0]) == 7:
                fieldnames = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
            elif len(list_updated[0]) == 6:
                fieldnames = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            counter = 1
            for item in list_updated:
                if len(list_updated[0]) == 7:
                    writer.writerow(
                        {'id': counter, 'submission_time': item['submission_time'], 'view_number': item['view_number'],
                         'vote_number': item['vote_number'], 'title': item['title'], 'message': item['message'],
                         'image': item['image']})
                if len(list_updated[0]) == 6:
                    writer.writerow({'id': counter, 'submission_time': item['submission_time'],
                                     'vote_number': item['vote_number'], 'question_id': item['question_id'],
                                     'message': item['message'], 'image': item['image']})
                counter += 1
        else:
            if file == server.question_path():
                fieldnames = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
            elif file == server.answer_path():
                fieldnames = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

def get_path(filename:str):
    return os.path.join(os.path.dirname(__file__), filename)

def read_file(filename):
    file = get_path(filename)
    with open(file, mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        return list(csv_reader)


def get_question_to_edit(question_id):
    data_list = read_file(server.question_path())
    for item in data_list:
        if item['id'] == question_id:
            return item


def edit_question_in_file(question_id, edited_title, edited_question, new_submission_time):
    data_list = read_file(server.question_path())
    for item in data_list:
        if item['id'] == question_id:
            item['submission_time'] = new_submission_time
            item['title'] = edited_title
            item['message'] = edited_question
    update_file(server.question_path(), data_list)


def vote_up(file, data_id):
    data_list = read_file(file)
    for item in data_list:
        if item['id'] == data_id:
            if len(data_list[0]) == 6:
                question_id = item['question_id']
            new_vote_number = int(item['vote_number'])
            new_vote_number += 1
            item['vote_number'] = str(new_vote_number)
            break
    update_file(file, data_list)
    if len(data_list[0]) == 6:
        return question_id


def vote_down(file, data_id):
    data_list = read_file(file)
    for item in data_list:
        if item['id'] == data_id:
            if len(data_list[0]) == 6:
                question_id = item['question_id']
            new_vote_number = int(item['vote_number'])
            new_vote_number -= 1
            item['vote_number'] = str(new_vote_number)
            break
    update_file(file, data_list)
    if len(data_list[0]) == 6:
        return question_id
