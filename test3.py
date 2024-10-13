from elevenlabs import Voice, VoiceSettings, play
from elevenlabs.client import ElevenLabs
import toml
from elevenlabs import save

config = toml.load("keys.toml")
api_key = config['key']
client = ElevenLabs(
  api_key=api_key, # Defaults to ELEVEN_API_KEY
)

audio = client.generate(
    text="Hello! My name is Bella.",
    voice=Voice(
        voice_id='S2KyfwxJ5VIsvOJ1XtQX',
        settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.1, use_speaker_boost=True)
    )
)

save(audio, "./test123.mp3")