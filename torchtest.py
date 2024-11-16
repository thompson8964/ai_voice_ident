import torch
import torchaudio
import torchaudio.transforms as T

waveform, sample_rate = torchaudio.load("WarrenP.mp3")
pitch_shift = T.PitchShift(sample_rate=sample_rate, n_steps=40)
shifted_waveform = pitch_shift(waveform)
torchaudio.save("torchtest1.mp3", shifted_waveform.detach(), sample_rate)