#!/bin/bash --rcfile
# -** coding: utf-8 -*-

source /etc/bash.bashrc
source ~/.bashrc
cat /etc/aiyprojects.info
source /home/vinay/AIY-voice-kit-python/env/bin/activate

cd -

python voice_recognition.py
deactivate

