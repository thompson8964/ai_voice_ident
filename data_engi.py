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
import argparse


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
            features[f"chroma_stft_{i}"] = note #shape error caused by 2 audio channels; solve by converting to mono channel audio


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


def extra_audio_features_multiple(folder_path, is_fake, csv_path_test, csv_path_train):
    df_existing_test = None
    df_existing_train = None
    if os.path.exists(csv_path_test):
        df_existing_test = pd.read_csv(csv_path_test)
    if os.path.exists(csv_path_train):
        df_existing_train = pd.read_csv(csv_path_train)

    df_combined = None
    list_dict_test = []
    list_dict_train = []
    for index, filepath in enumerate(tqdm(glob.glob(os.path.join(folder_path, "*.mp3")))):

        try:
            list_of_d = extract_audio_features(filepath, is_fake)
        except Exception as e:
            print("Error occurred during audio feature: " + filepath)
            print(e)
            continue
        if index % 5 == 0:
            if df_existing_test is not None and "file_path" in df_existing_test.columns and filepath in df_existing_test["file_path"]:
                continue
            list_dict_test += list_of_d

            df_combined_test = pd.concat([df_existing_test, pd.DataFrame(list_dict_test)], axis=0)
            df_existing_test = df_combined_test
            list_dict_test = []

            df_combined_test.to_csv(csv_path_test, index=False)
        else:
            if df_existing_train is not None and "file_path" in df_existing_train.columns and filepath in df_existing_train["file_path"]:
                continue
            list_dict_train += list_of_d

            df_combined_train = pd.concat([df_existing_train, pd.DataFrame(list_dict_train)], axis=0)
            df_existing_train = df_combined_train
            list_dict_train = []

            df_combined_train.to_csv(csv_path_train, index=False)

    return pd.concat([df_combined_train, df_combined_test])


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--folder_path", "-f", required=True, help="Process audio files in this folder")
    arg_parser.add_argument("--is_real", required=True, help="If the audio is AI generated", type=int, default=0)
    arg_parser.add_argument("--test_path", required=True, help="csv path for testing audio")
    arg_parser.add_argument("--train_path", required=True, help="csv path for training audio")
    args = arg_parser.parse_args()

    # extra_audio_features_multiple("real_mpeg", False, "audio_real_test.csv", "audio_real_train.csv")
    extra_audio_features_multiple(
        folder_path=args.folder_path,
        is_fake=bool(not args.is_real),
        csv_path_test=args.test_path,
        csv_path_train=args.train_path,
    )
