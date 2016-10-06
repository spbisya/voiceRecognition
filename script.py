import urllib2
import sys
import os

key = "AIzaSyAqk7vE0vQDR3JItUPgFp6bcPqgJz8h8tI"
url = "https://www.google.com/speech-api/v2/recognize?output=json&lang=ru-ru&key="+key

audio = open("voice.flac",'rb').read()

headers={'Content-Type': 'audio/x-flac; rate=44100'}

request = urllib2.Request(url, data=audio, headers=headers)
response = urllib2.urlopen(request)
print response.read()
