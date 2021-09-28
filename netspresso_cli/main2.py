from __future__ import print_function, unicode_literals
import sys
import os
import json
from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint


sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from netspresso_cli.onprem import auth


style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

def get_user_id():
    question_user_id = [
        {
            'type': 'input',
            'message': 'user_id: ',
            'name': 'user_id',
        }
    ]
    answers = prompt(question_user_id, style=style)
    return answers["user_id"]


def get_user_pw():
    question_user_pw = [
        {
            'type': 'input',
            'message': 'user_pw: ',
            'name': 'user_pw',
        }
    ]
    answers = prompt(question_user_pw, style=style)
    return answers["user_pw"]

def select_main_task():
    question_task = [
        {
            'type': 'list',
            'message': 'Select a tasks',
            'name': 'task',
            'choices': [
                Separator('= what do you want to do? (please login first) ='),
                {
                    'name': 'Login'
                },
                {
                    'name': "Logout"
                },
                {
                    'name': 'Create a compression'
                },
                {
                    'name': 'Exit'
                }
            ],
            'validate': lambda answer: 'You must choose at least one task.' \
                if len(answer) == 0 else True
        }
    ]
    answers = prompt(question_task, style=style)
    return answers

def save_userinfo(user_info):
    with open("user_info.json", "wt") as f:
        json.dump(user_info, f)

def load_userinfo():
    try:
        with open("user_info.json", "rt") as f:
            d = json.load(f)
        return d
    except:
        raise Exception("loading userinfo failed!!")

def delete_userinfo():
    try:
        os.remove("user_info.json")
    except:
        pass

if __name__ == "__main__":
    answers = select_main_task()
    print(answers)
    if answers["task"] == "Login":
        user_id = get_user_id()
        user_pw = get_user_pw()
        user_info = auth.login(user_id, user_pw)
        save_userinfo(user_info)
    if answers["task"] == "Logout":
        delete_userinfo()
    elif answers["task"] == "Create a compression":
        print("compression")
    elif answers["task"] == "Exit":
        print("exit")
    else:
        print("invalid selection")