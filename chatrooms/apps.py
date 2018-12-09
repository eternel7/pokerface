from chatterbot import ChatBot
from chatterbot.ext.django_chatterbot import settings
from chatterbot.trainers import ListTrainer
import os
import threading

PokerFaceBot = ChatBot(**settings.CHATTERBOT)


def get_chatBot():
    return PokerFaceBot


def train_with_file(path):
    print("Training with ", path)
    diags = open(path, 'r', encoding='utf-8').readlines()
    PokerFaceBot.train(diags)
    print("Done training with ", path)


def init_chatbot():
    print("Starting initialization of chatBot")
    
    # Train according to setting
    if settings.CHATTERBOT.get('training_data'):
        print("Training according to setting with trainer", settings.CHATTERBOT.get('trainer'))
        for trainingset in settings.CHATTERBOT.get('training_data'):
            print("Training with ", trainingset)
            PokerFaceBot.train(trainingset)
            print("Done training with ", trainingset)
        
        print("Done training according to setting")
    
    # complete train with local files
    PokerFaceBot.set_trainer(ListTrainer)
    
    for _file in os.listdir('datasets'):
        t = threading.Thread(target=train_with_file, args=('datasets/' + _file,))
        t.start()
    
    print("ChatBot initialization launched")
