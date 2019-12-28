#!/usr/bin/env python

# patches issue that path when using cron didn't have access to needed libs
import sys
dependencies = ['/usr/lib/python2.7', '/usr/lib/python2.7/plat-arm-linux-gnueabihf', '/usr/lib/python2.7/lib-tk', '/usr/lib/python2.7/lib-old', '/usr/lib/python2.7/lib-dynload', '/home/pi/.local/lib/python2.7/site-packages', '/usr/local/lib/python2.7/dist-packages', '/usr/lib/python2.7/dist-packages', '/usr/lib/python2.7/dist-packages/gtk-2.0']
for dependency in dependencies:
    if (sys.path.__contains__(dependency) is not True):
        sys.path.append(dependency)

from os import walk
from pydub import AudioSegment
from pydub.playback import play
from random import randint
import RPi.GPIO as GPIO

# initialization
input_pin = 17
key = 0
values = {}
soundbite = {}
GPIO.setmode(GPIO.BCM)
GPIO.setup(input_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# this is expensive, we only want to do it once
for root, dirs, files in walk("/home/pi/Music"):
    for filename in files:
        values[key] = filename
        soundbite[key] = AudioSegment.from_wav('/home/pi/Music/' + filename)
        key += 1

# infinite loop starts here
door_open = False
already_open = False

while True:
    door_open = (GPIO.input(input_pin) >= 1) # (i//50000 >= 1)
    if (door_open and not already_open):
        soundbite_selector = randint(0, key-1)
        play(soundbite[soundbite_selector])
    if door_open:
        already_open = True
    else:
        already_open = False
