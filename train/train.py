from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

trainer = ListTrainer(ChatBot("Trainer", database_uri='sqlite:///../db.sqlite3'))

with open("source.txt", "r", encoding="utf-8") as f:
    for dialogue in f.read().split("\n\n"):
        dial_list = []
        for line in dialogue.split("\n"):
            dial_list.append(line.replace("-", ""))
        trainer.train(dial_list)
