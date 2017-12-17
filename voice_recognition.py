#!/home/vinay/AIY-voice-kit-python/env/bin/python
# -*- coding: utf-8 -*-

"""
Google Cloud Speech based Voice Recognition Test


2017-12-10
Vinay Keerthi
"""

import os
import sys
sys.path.append("/home/vinay/AIY-voice-kit-python/src/")
import aiy.audio
import aiy.voicehat
import aiy.assistant.grpc

def say(text=None):
    from google_speech import Speech

    if text is None:
        say_fortune()
    elif text.lower() == "flipkart":
        say_fk_fortune()
    else:
        lang="en"
        speech = Speech(text, lang)
    speech.play()


def say_fk_fortune():
    import random
    with open("quotes.txt", "r") as f:
        quotes = f.readlines()

    say(random.choice(quotes))

def say_fortune():
    import subprocess
    fortune = subprocess.check_output(["fortune"]).decode("utf-8").replace("\n","")
    for character in [".","?",";", ":","-"]:
        fortune = fortune.replace(character,character+"\n")
    for line in fortune.split("\n"):
        if line.strip() != "":
            say(line.strip())

def main_cloud():
    """Main function. Duh."""
    import aiy.cloudspeech
    recognizer = aiy.cloudspeech.get_recognizer()
    recognizer.expect_phrase("Yabadabado")

    button = aiy.voicehat.get_button()
    led = aiy.voicehat.get_led()
    aiy.audio.get_recorder().start()
    led.set_state(aiy.voicehat.LED.BLINK)
    while True:
        try:
            say("Press the button")
            button.wait_for_press()
            led.set_state(aiy.voicehat.LED.ON)
            say("Say something!")
            text = recognizer.recognize()
            if text is None:
                say("I thought I told you to say something.")
            else:
                say('You said: {}'.format( text))
            led.set_state(aiy.voicehat.LED.OFF)
        except KeyboardInterrupt:
            led.set_state(aiy.voicehat.LED.OFF)
            led.set_state(aiy.voicehat.LED.BLINK)
            led.set_state(aiy.voicehat.LED.BLINK)
            break

    say("buh bye!")

def main_grpc():
    import aiy.assistant.grpc
    import time
    status_ui = aiy.voicehat.get_status_ui()
    status_ui.status("starting")
    assistant = aiy.assistant.grpc.get_assistant()
    button = aiy.voicehat.get_button()
    led = aiy.voicehat.get_led()
    led.set_state(aiy.voicehat.LED.BLINK)
    time.sleep(1)
    led.set_state(aiy.voicehat.LED.OFF)
    say("Press the button and speak.")
    with aiy.audio.get_recorder():
        while True:
            try:
                status_ui.status("ready")
                button.wait_for_press()
                status_ui.status("listening")
                say("Listening...")
                text, audio = assistant.recognize()
                if text is not None:
                    if text == "goodbye":
                        status_ui.status("stopping")
                        say("Bye!")
                        break
                    elif "fortune" in text.lower():
                        say()
                    elif "flipkart" in text.lower():
                        say("flipkart")
                    else:
                        say("You said: {}. I need to ask Google to help me with that.".format(text))
                        if audio is None:
                            say("I did not get any response from Google.")
                        else:
                            try:
                                aiy.audio.play_audio(audio)
                            except:
                                say("There was some problem trying to say what Google wants me to say.")
                else:
                    say("I did not catch that boss.")
            except KeyboardInterrupt:
                led.set_state(aiy.voicehat.LED.OFF)
                say("I am done, boss!")
                break


if __name__ == "__main__":
    main_grpc()

