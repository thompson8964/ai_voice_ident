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
def text_to_speech_file(text: str, voiceId: str, saveFolder: str = "") -> str:
    # Calling the text_to_speech conversion API with detailed parameters
    response = client.text_to_speech.convert(
        voice_id= voiceId, # Adam pre-made voice
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_multilingual_v2",
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
        ),
    )

    # uncomment the line below to play the audio back
    # play(response)

    # Generating a unique file name for the output MP3 file
    if not os.path.isdir(saveFolder):
        os.makedirs(saveFolder)

    save_file_path = os.path.join(saveFolder, f"{uuid.uuid4()}.mp3")

    # Writing the audio to a file
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!")

    # Return the path of the saved audio file
    return save_file_path


if __name__ == "__main__":

    config = toml.load("keys.toml")
    api_key = config['key']

    client = ElevenLabs(
        api_key=api_key,  # Defaults to ELEVEN_API_KEY
    )
    sourceAudioPaths = sorted(list(glob.glob("./sourcesForCloning/*")))

    filePath = glob.glob(r"E:\aclImdb\test\**\*.txt")

    for path in sourceAudioPaths:

        voice = client.clone(
            name=(filename:=Path(path).name),
            description="",
            files=[path],
        )
        if voice.voice_id:
            print("Successful clone!")


            try:
                shutil.move(path, f"./clonedSources/{filename}")
            except WindowsError:
                pass


            for i in range(10):
                filePath = random.choice(filePath)
                with open(filePath) as f:
                    text = f.read()
                    text = text.replace("\n", ". ")
                    text_to_speech_file(text, voice.voice_id, r"E:\aclImdb\voices_audio")




        # audio = client.generate(text="Hi! I'm a cloned voice!", voice=voice)
        # save(audio, "./warrenCloned.mp3")
    #play(audio)