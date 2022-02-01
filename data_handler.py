import csv
import server


QUESTION_TITLE = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWER_TITLE = ["id", "submission_time", "vote_number", "question_id", "message", "image"]


def get_all_data(filename):
    with open(filename, "r") as data_file:
        reader = csv.DictReader(data_file)
        return [*reader]


def get_data_by_id(filename, id_):
    list_of_data = get_all_data(filename)
    for row in list_of_data:
        if row['id'] == id_:
            return row


def get_answers_by_id(id_):
    list_of_answers = get_all_data(server.answer_path())
    return [answer for answer in list_of_answers if answer['question_id'] == id_]


def data_writer(filename, to_write, fieldnames):
    with open(filename, "w") as file_to_write:
        writer = csv.DictWriter(file_to_write, fieldnames)
        writer.writeheader()
        for row in to_write:
            writer.writerow(row)


def edit_data(id_, new_line, filename):
    list_of_data = get_all_data(filename)
    for i, row in enumerate(list_of_data):
        if row["id"] == id_:
            list_of_data[i] = new_line
    return list_of_data
