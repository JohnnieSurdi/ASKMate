
def create_new_answer_for_file(new_answer):
    new_answer_list = []
    for value in new_answer.values():
        new_answer_list.append(str(value))
    file_answer_message = ", ".join(new_answer_list)
    file_answer_message += "\n"
    return file_answer_message


def write_new_answer_to_file(new_answer):
    file_answer_message = create_new_answer_for_file(new_answer)
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
        for element in row:
            if element != ",":
                id_number += element
            else:
                if int(id_number) > max_id:
                    max_id = int(id_number)
                break
    new_id = max_id + 1
    return new_id

# create_new_id('sample_data/answer.csv')

def add_question_to_file(title,question,submission_time):
    file = 'C:/Users/kamci/projects/ask-mate-1-python-MichalProsniak/sample_data/question.csv'
    id = create_new_id(file)
    view_number = 0
    vote_number = 0
    image = ''
    with open(file, "a") as f:
        f.write(f'{id},{submission_time},{view_number},{vote_number},{title},{question},{image}\n')
    return id


def read_all_questions_from_file():
    list_of_dicts = []
    with open('C:/Users/kamci/projects/ask-mate-1-python-MichalProsniak/sample_data/question.csv') as data_file:
        for line in data_file:
            line = line.replace('\n', '')
            line = line.split(',')
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
    list = []
    with open('C:/Users/kamci/projects/ask-mate-1-python-MichalProsniak/sample_data/question.csv') as data_file:
        for line in data_file:
            raw_line = line
            line = line.replace('\n', '')
            line = line.split(',')
            if line[0]==question_id:
                continue
            else:
                list.append(line)
    counter = 1
    for item in list:
        if item[0] != 'id':
            item[0]=counter
            counter+=1
    with open('C:/Users/kamci/projects/ask-mate-1-python-MichalProsniak/sample_data/question.csv','w') as f:
        for item in list:
            print(item)
            f.write(f'{item[0]},{item[1]},{item[2]},{item[3]},{item[4]},{item[5]}\n')






def update_id_in_questions(questions_to_keep):
    id = 1
    for question in questions_to_keep:
        question['id'] = id
        id += 1