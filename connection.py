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
