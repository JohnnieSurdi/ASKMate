import csv
import server


def write_new_answer_to_file(new_answer):
    with open(server.answer_path(), 'a', newline='') as csvfile:
        fieldnames = ['id','submission_time','vote_number','question_id','message','image']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'id': new_answer['id'], 'submission_time': new_answer['submission_time'], 'vote_number': new_answer['vote_number'], 'question_id': new_answer['question_id'], 'message': new_answer['message'], 'image': new_answer['image']})



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
    if max_id == 0:
        new_id = 1
    return new_id


def add_question_to_file(title,question,submission_time):
    file = server.question_path()
    id = create_new_id(file)
    view_number = 0
    vote_number = 0
    image = -1
    with open(server.question_path(), 'a', newline='') as csvfile:
        fieldnames = ['id', 'submission_time','view_number','vote_number','title','message','image']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'id': id, 'submission_time': submission_time, 'view_number': view_number, 'vote_number': vote_number, 'title': title, 'message': question, 'image': image})


def read_all_questions_from_file():
    list_of_dicts = []
    with open(server.question_path()) as data_file:
        for line in data_file:
            line = line.replace('\n', '')
            line = line.split(',')
            print(line)
            dict = {}
            dict['id']=line[0]
            dict['submission_time']=line[1]
            dict['view_number']=line[2]
            dict['vote_number']=line[3]
            dict['title']=line[4]
            dict['message']=line[5]
            dict['image']=line[6]
            list_of_dicts.append(dict)
    return list_of_dicts[1:]


def delete_question_from_file(question_id):
    list = read_file(server.question_path())
    list_updated = []
    for item in list:
        if item['id'] == question_id:
            continue
        else:
            list_updated.append(item)
    with open(server.question_path(), 'w', newline='') as csvfile:
        fieldnames = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        counter = 1
        for item in list_updated:
            writer.writerow(
                {'id': counter, 'submission_time': item['submission_time'], 'view_number': item['view_number'],
                 'vote_number': item['vote_number'], 'title': item['title'], 'message': item['message'],
                 'image': item['image']})
            counter += 1




'''def update_id_in_questions(questions_to_keep):
=======
def delete_from_file(data_id, file):
    list_of_lines = []
    with open(file) as data_file:
        for line in data_file:
            line = line.replace('\n', '')
            line = line.split(',')
            if line[0] == data_id:
                if len(line) == 6:
                    question_id = line[3]
                continue
            else:
                list_of_lines.append(line)
    counter = 1
    for item in list_of_lines:
        if item[0] != 'id':
            item[0] = counter
            counter += 1
    with open(file, 'w') as f:
        for item in list_of_lines:
            if len(item) == 6:
                f.write(f'{item[0]},{item[1]},{item[2]},{item[3]},{item[4]},{item[5]}\n')
            elif len(item) == 7:
                f.write(f'{item[0]},{item[1]},{item[2]},{item[3]},{item[4]},{item[5]},{item[6]}\n')
    if len(list_of_lines[0]) == 6:
        return question_id



def update_id_in_questions(questions_to_keep):
>>>>>>> b80340767e16978989c23fc3a890fa335846d3c7
    id = 1
    for question in questions_to_keep:
        question['id'] = id
        id += 1'''

def read_file(filename):
    with open(filename, mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        return list(csv_reader)


def get_question_to_edit(question_id):
    list = read_file(server.question_path())
    for item in list:
        if item['id'] == question_id:
            return item

def edit_question_in_file(question_id,edited_title,edited_question,new_submission_time):
    list = read_file(server.question_path())
    for item in list:
        if item['id']==question_id:
            item['submission_time']=new_submission_time
            item['title']=edited_title
            item['message']=edited_question
    with open(server.question_path(), 'w', newline='') as csvfile:
        fieldnames = ['id', 'submission_time','view_number','vote_number','title','message','image']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in list:
            writer.writerow({'id': item['id'], 'submission_time': item['submission_time'], 'view_number': item['view_number'], 'vote_number': item['vote_number'], 'title': item['title'], 'message': item['message'], 'image': item['image']})

