import librosa
import numpy as np
import scipy
import pandas as pd
import csv
import glob
import os
from tqdm import tqdm
import csv
import random
def getSlice(array, duration, sr):
  length = len(array) / sr
  start = random.uniform(0, length - duration)
  amp_slice = array[int(start * sr) : int((start + duration) * sr)]

  return amp_slice

def isQuiet(np_slice, threshold=0.1, percent=0.9):
  #give percent as decimal
  #returns true if fraction below threshould is higher than percent given, false otherwise
  numUnderThresh = (np.abs(np_slice) < threshold).sum()
  # np_size = np.prod(amp.shape)
  # print(numUnderThresh, np_size)
  return (numUnderThresh / len(np_slice) ) > percent
def extract_audio_features(file_path, is_fake):
    """
    Extracts audio features from an audio file.

    Args:
    file_path (str): Path to the audio file.

    Returns:
    dict: A dictionary containing the extracted features.
    """
    # Load audio file
    full_audio_array, sr = librosa.load(file_path, sr=None)
    duration = librosa.get_duration(y=full_audio_array, sr=sr)

    list_features = []
    for i in range(int(duration / 10)):
        y = getSlice(full_audio_array, 10, sr)
        if isQuiet((y)):
            continue

        features = {}

        # Chroma STFT (Chromagram) it's an average value for the 12 music notes, with a shape of (12, )
        chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr).mean(axis=1)
        for i, note in enumerate(chroma_stft):
            features[f"chroma_stft_{i}"] = note


        # RMS (Root Mean Square)
        features['rms'] = librosa.feature.rms(y=y).mean()

        # Spectral Centroid
        features['spectral_centroid'] = librosa.feature.spectral_centroid(y=y, sr=sr).mean()

        # Spectral Bandwidth
        features['spectral_bandwidth'] = librosa.feature.spectral_bandwidth(y=y, sr=sr).mean()

        # Spectral Roll-off
        features['spectral_rolloff'] = librosa.feature.spectral_rolloff(y=y, sr=sr, roll_percent=0.85).mean()

        # Zero Crossing Rate
        features['zero_crossing_rate'] = librosa.feature.zero_crossing_rate(y=y).mean()

        features["is_fake"] = is_fake

        features["file_path"] = file_path

        # MFCCs (Mel-frequency cepstral coefficients)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20).mean(axis=1)

        for i, value in enumerate(mfccs):
            features[f"mfccs_{i}"] = value
        list_features.append(features)

    return list_features


def extra_audio_features_multiple(folder_path, is_fake, csv_path):
    df_existing = None
    if os.path.exists(csv_path):
        df_existing = pd.read_csv("audio.csv")

    df_combined = None
    list_dict = []
    for filepath in tqdm(glob.glob(os.path.join(folder_path, "*.mp3"))):
        if df_existing is not None and "file_path" in df_existing.columns and filepath in df_existing["file_path"]:
            continue

        try:
            list_of_d = extract_audio_features(filepath, is_fake)
        except:
            print("Error occurred during audio feature: " + filepath)
            continue
        list_dict += list_of_d

        df_new = pd.DataFrame(list_dict)
        df_combined = pd.concat([df_existing, df_new], axis=0)
        df_existing = df_combined
        list_dict = []
        df_combined.to_csv(csv_path, index=False)
    return df_combined


if __name__ == "__main__":
    extra_audio_features_multiple("real_mpeg", False, "audio_real.csv")
    # dict_1 = extract_audio_features(r"warrenCloned.mp3", False)
   # print(f'{dict_1}')
  #  df = pd.DataFrame([dict_1, dict_2, dict_3])
  #  df['is_fake'] = False
   # print(df)