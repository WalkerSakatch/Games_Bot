from firebase import firebase
import random, re
firebase = firebase.FirebaseApplication('https://game-bot-28c09-default-rtdb.firebaseio.com/', None)
fortune_num = 3

def submit(string):
    fortunes = firebase.get('/fortunes', None)

    if(fortunes is None or string not in fortunes.values()):
        firebase.post('/fortunes', string)
        return("Got it!")
    elif(string in fortunes.values()):
        return("I've already got that one, babe")

def fortune(update, context):
    global fortune_num
    msg_ID = update.message.message_id
    fortunes = firebase.get('/fortunes', None)
    if(fortunes is None):
        return("Sorry I'm all out of fortunes, come back later.")
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text="Sorry I'm all out of fortunes, come back later.")
    else:
        fortune = fortunes.values()
        fortune = list(fortune)
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=fortune[fortune_num])
        fortune_num += random.randint(1, 2)
        if(fortune_num >= len(fortune) - 1):
            fortune_num = random.randint(1, 4)
        #context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text="New fortune num: {}".format(fortune_num))

def kill(string):
    firebase.delete('/fortunes', string)
    return("Bye Bye!")