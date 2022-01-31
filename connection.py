import ast


def create_new_answer_for_file(new_answer):
    new_answer_list = []
    for index, value in enumerate(new_answer.values()):
        if index == 4:
            value = "\"" + value + "\""
        new_answer_list.append(str(value))
    file_answer_message = ",".join(new_answer_list)
    file_answer_message += "\n"
    return file_answer_message


def write_new_answer_to_file(new_answer):
    file_answer_message = create_new_answer_for_file(new_answer)
    print(file_answer_message)
    with open('sample_data/answer.csv', 'a+') as answers:
        answers.write(file_answer_message)


def rows_from_file(file):
    csv_file_rows = []
    with open(file, 'r') as csvfile:
        for index, row in enumerate(csvfile):
            if index != 0:
                csv_file_rows.append(row)
    return csv_file_rows


def create_new_id(file):
    max_id = 0
    csv_file_rows = rows_from_file(file)
    for row in csv_file_rows:
        id_number = ""
        if row.count(',') >= 4:
            for element in row:
                if element.isdigit():
                    id_number += element
                else:
                    if id_number == "":
                        id_number = "0"
                    if int(id_number) > max_id:
                        max_id = int(id_number)
                    break
        new_id = max_id + 1
    return new_id


def add_question_to_file(title,question,submission_time):
    question_dict = {}
    global ID_NUMBER
    id = ID_NUMBER
    ID_NUMBER += 1
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


def read_all_questions_from_file():
    list_of_dicts = []
    with open('sample_data/question.csv') as data_file:
        for line in data_file:
            line = line.replace('\n', '')
            list_of_dicts.append(ast.literal_eval(line))
    return list_of_dicts


def delete_question_from_file(question_id):
    all_questions = read_all_questions_from_file()
    questions_to_keep = []
    for question in all_questions:
        if question['id']==question_id:
            pass
        else:
            questions_to_keep.append(question)


def update_id_in_questions(questions_to_keep):
    id = 1
    for question in questions_to_keep:
        question['id'] = id
        id += 1