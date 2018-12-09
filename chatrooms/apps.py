from chatterbot import ChatBot
from chatterbot.ext.django_chatterbot import settings
from chatterbot.trainers import ListTrainer
import os
import threading

PokerFaceBot = ChatBot(**settings.CHATTERBOT)


def get_chatBot():
    return PokerFaceBot


def train_with_file(path):
    exclude_path_in_dev = ['datasets/movies_dialogues.txt']
    if path not in exclude_path_in_dev:
        print("Training with ", path)
        filename, file_extension = os.path.splitext(path)
        print("Training set extension", file_extension)
        
        if file_extension == '.txt':
            print("Training with ListTrainer")
            PokerFaceBot.set_trainer(ListTrainer)
            diags = open(path, 'r', encoding='utf-8').readlines()
            PokerFaceBot.train(diags)
            print("Done training with ", path)
        else:
            print("Don't know which trainer to apply for", filename, "of type", file_extension)


def train_according_setting():
    if settings.CHATTERBOT.get('training_data'):
        print("Training according to setting with trainer", settings.CHATTERBOT.get('trainer'))
        for trainingset in settings.CHATTERBOT.get('training_data'):
            print("Training with ", trainingset)
            PokerFaceBot.train(trainingset)
            print("Done training with ", trainingset)
        
        print("Done training according to setting")


def init_chatbot():
    print("Starting initialization of chatBot")
    # purging database
    print("Starting purge of chatBot database")
    PokerFaceBot.storage.drop()
    print("Purging chatBot Done")
    
    # Train according to setting
    t = threading.Thread(target=train_according_setting)
    t.start()
    
    for _file in os.listdir('datasets'):
        t = threading.Thread(target=train_with_file, args=('datasets/' + _file,))
        t.start()
    
    print("ChatBot initialization launched")
