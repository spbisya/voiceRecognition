import urllib2
import sys
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import json

def startRecognition(bot, update, file_path):
    os.system("curl -o voice.oga "+file_path+" && ffmpeg -y -i voice.oga voice.flac")
    key = "AIzaSyAqk7vE0vQDR3JItUPgFp6bcPqgJz8h8tI"
    url = "https://www.google.com/speech-api/v2/recognize?output=json&lang=ru-ru&key="+key

    audio = open("voice.flac",'rb').read()

    headers={'Content-Type': 'audio/x-flac; rate=44100'}

    request = urllib2.Request(url, data=audio, headers=headers)
    response = urllib2.urlopen(request)
    data = response.read()
    new_data = str(data).replace("{\"result\":[]}","")
    try:
        maps = json.loads(new_data)
        print maps["result"][0]["alternative"][0]
        update.message.reply_text("With confidence "+str(maps["result"][0]["alternative"][0]["confidence"])+" text is \n"+maps["result"][0]["alternative"][0]["transcript"])
    except Exception as e:
        update.message.reply_text("Can't recognize text!") 


def start(bot, update):
    update.message.reply_text('Hi!')

def help(bot, update):
    update.message.reply_text('Help!')

def echo(bot, update):
    logging.warning(update.message)
    file_id = bot.getFile(update.message.voice.file_id)
    logging.warning(file_id.file_path)
    startRecognition(bot, update, file_id.file_path)

def error(bot, update, error):
    logging.warning('Update "%s" caused error "%s"' % (update, error))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

updater = Updater(token='288744063:AAGQrAS7exlDXWl583KaYNGdTb6u9_x38DU')
dispatcher = updater.dispatcher
# on different commands - answer in Telegram
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help))
dispatcher.add_handler(MessageHandler([Filters.voice], echo))
dispatcher.add_error_handler(error)
updater.start_polling()
