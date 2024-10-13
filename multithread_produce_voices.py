from elevenlabs import play, save
from elevenlabs.client import ElevenLabs
import toml
import numpy as np
import random
import datetime
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import glob

#def getaiaudio(savePath, filePath, length)
url = "https://api.elevenlabs.io/v1/voices"


# response = requests.request("GET", url)
# print(response.text)
# response = json.loads(response.text)
#
# print(type(response))
# voicesList = []
#
# for voice in response["voices"]:
#     voicesList.append(voice["voice_id"])
#
# word_url = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
# response = urllib.request.urlopen(word_url)
# long_txt = response.read().decode()
# words = long_txt.splitlines()
# print(words)

config = toml.load("keys.toml")
api_key = config['key']

client = ElevenLabs(
    api_key=api_key,  # Defaults to ELEVEN_API_KEY
)

response = client.voices.get_all()
voicesList = response.voices
# Access the API key
def single_ai_audio(text, saveDir):
    """

    :param text:
    :param saveDir: folder where mp3 is saved
    :return: file path of mp3
    """





    voice = voicesList[random.randint(0, len(voicesList)-1)]
    print(voice)

    filePath = os.path.join(saveDir, f"{voice}_{str(hash(text))}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}.mp3")



    client = ElevenLabs(
      api_key=api_key,
    )

    audio = client.generate(
      text=text,
      voice=voice,
      model="eleven_multilingual_v2"
    )

    save(audio, filePath)
    return filePath


def multithread(
        num_audio_generate: int = 20,
        input_dir=r"E:\aclImdb\test\neg",
        output_dir: str = "fake",
        max_workers: int = 10,
        language: str="en",
) -> int:
    fileLists = glob.glob(os.path.join(input_dir, "*.txt"))
    print(f'files found: {len(fileLists)}')

    paths = np.random.choice(fileLists, num_audio_generate, replace=True)



    futures = []
    total_count = 0


    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for filePath in paths:
            with open(filePath) as f:
                text = f.read()
                # if language != "en":
                #
                #     text = translator.translate(text, dest=language)
                futures.append(
                    executor.submit(
                        single_ai_audio,
                        text=text,
                        saveDir=output_dir,
                    )
                )


        for future in as_completed(futures):
            result = future.result
            total_count += result
    return total_count



if __name__ == "__main__":
    # single_ai_audio("Similar to Harley's answer, but use the str() function for a quick-n-dirty, slightly more human readable format:", r"fake")
    multithread(
        num_audio_generate = 20,
        input_dir = r"E:\aclImdb\test\neg",
        output_dir = "fake",
        max_workers = 10,
        language= "en",

    )
