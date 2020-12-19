import random

statements = ["Хорошо, держи меня в курсе событий!", "Ого!", "Вот это да!", "Забавно!"]
questions = ["Да, да?", "Что, что?", "А?", "Что говоришь?", "Что такое?", "А ну повтори!"]

def get_response(input):
    ret_statement = input
    if (random.randint(0, 5) != 0):
        if (ret_statement.text.endswith("?")):
            ret_statement.text = random.choice(questions)
        else:
            ret_statement.text = random.choice(statements)

    return ret_statement
