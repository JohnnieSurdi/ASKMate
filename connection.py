def create_new_answer_for_file(new_answer):
    new_answer_list = []
    for index, value in enumerate(new_answer.values()):
        if index == 4:
            value = "\"" + value + "\""
        new_answer_list.append(str(value))
    file_answer_message = ", ".join(new_answer_list)
    file_answer_message += "\n"
    return file_answer_message


def write_new_answer_to_file(new_answer):
    file_answer_message = create_new_answer_for_file(new_answer)
    print(file_answer_message)
    with open('sample_data/answer.csv', 'a+') as answers:
        answers.write(file_answer_message)


# new_answer = {'id': 6, 'w}evw': 3, 'erqnbeqr': 2, 'qrbqrb': 0, 'message': 'kjbrqeirub', 'fqb': ''}
# write_new_answer_to_file(new_answer)

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
        id_number = 0
        for element in row:
            if element.isdigit():
                id_number += int(element)
            else:
                if id_number > max_id:
                    max_id = id_number
                break
    new_id = max_id + 1
    return new_id


# create_new_id('sample_data/answer.csv')
