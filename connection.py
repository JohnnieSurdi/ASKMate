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


