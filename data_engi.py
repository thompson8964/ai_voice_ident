import librosa
import numpy as np
import scipy
import pandas as pd


def extract_audio_features(file_path):
    """
    Extracts audio features from an audio file.

    Args:
    file_path (str): Path to the audio file.

    Returns:
    dict: A dictionary containing the extracted features.
    """
    # Load audio file
    y, sr = librosa.load(file_path, sr=None)

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

    # MFCCs (Mel-frequency cepstral coefficients)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20).mean(axis=1)

    for i, value in enumerate(mfccs):
        features[f"mfccs_{i}"] = value
    return features


if __name__ == "__main__":
    dict_1 = extract_audio_features(r"warrenCloned.mp3")
    print(f'{dict_1=}')
    df = pd.DataFrame([dict_1, dict_2, dict_3])
    df['is_fake'] = False
    print(df)