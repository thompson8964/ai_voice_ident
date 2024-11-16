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

config = toml.load("keys.toml")
api_key = config['key']

client = ElevenLabs(
    api_key=api_key,  # Defaults to ELEVEN_API_KEY
)

print(client.voices.get_all())