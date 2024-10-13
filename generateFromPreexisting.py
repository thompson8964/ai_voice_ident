from voiceCloning import text_to_speech_file
import random

from elevenlabs.client import ElevenLabs
from elevenlabs import play
import toml
from elevenlabs import save
import os
import glob
from pathlib import Path
import shutil
from elevenlabs import VoiceSettings
import uuid
import re
import json
import requests

config = toml.load("keys.toml")
api_key = config['key']

client = ElevenLabs(
    api_key=api_key,  # Defaults to ELEVEN_API_KEY
)
response = client.voices.get_all()
voicesList = response.voices
print(voicesList)


#print(response.text)
#
#
filePaths = glob.glob(r"E:\aclImdb\test\**\*.txt")
for voice in voicesList:
    if voice.category == "cloned":

        for i in range(10):
            filePath = random.choice(filePaths)
            with open(filePath, encoding="UTF-8") as f:
                text = f.read()
                text = text.replace("\n", ". ")
                text_to_speech_file(text, voice.voice_id, r"E:\aclImdb\voices_audio")