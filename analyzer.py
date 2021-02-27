import re
import datetime

def chat_reader(file_name):
    for row in open(file_name, "r", encoding="utf8"):
        yield row

name_to_msg_dic = {}
date_to_msg_dic = {}
date_to_name_dic = {}

def append_to_diclist(key, value, dic):
    if key not in dic:
        dic[key] = []

    dic[key].append(value)

def count_word_said_by_name(word, name):
    counter = 0
    for msgs in name_to_msg_dic[name]:
        if word in msgs:
            counter += 1
    return counter


def process_chat_rows(rows):
    for row in rows:
        regex = r"^(?P<date>\d+\/\d+\/\d+\,\s\d+\:\d+)\s\-\s(?P<message>.*)"
        matches = re.search(regex, row)
        if matches:
            date_str = matches.group('date')
            message = matches.group('message')
            regex = r"^(?P<name>\w+)\:\s+(?P<message>.*)"
            matches = re.search(regex, message)
            if matches == None:
                name, msg = ["whatsapp", message]
            else:
                name, msg = [matches.group('name'), matches.group('message')]

            date = datetime.datetime.strptime(date_str, '%m/%d/%y, %H:%M')

            append_to_diclist(name, msg, name_to_msg_dic)
            append_to_diclist(date, msg, date_to_msg_dic)
            append_to_diclist(date, name, date_to_name_dic)

        else: # in case of multiline message
            message += row






file_rows = chat_reader("WhatsAppChatFreeHate.txt")
process_chat_rows(file_rows)
word = "זין"
name = "יואב"
content = ""
content += (f"{name} said {word} {count_word_said_by_name(word, name)} times\n")

name = "עמית"
content += (f"{name} said {word} {count_word_said_by_name(word, name)} times\n")

name = "תומר"
content += (f"{name} said {word} {count_word_said_by_name(word, name)} times\n")

with open("end", "w", encoding="utf-8") as f:
    f.write(content)
