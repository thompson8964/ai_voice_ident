import librosa
import os
from tqdm import tqdm
import numpy as np
import random
import PIL
import cv2
from PIL import Image, ImageOps
import glob
from pathlib import Path

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

sourcePath = r"fake/"
savePath = r"fake_spects/"
counter = 0

for filepath in tqdm(glob.glob(sourcePath + "*.mp3")[41:]):
  filename = Path(filepath).name
  print("loading: " + filename)
  amp, sr = librosa.load(sourcePath + filename)
  # amps[str(filename)] = [amp, sr]
  #
  #
  # amp = amps[str(filename)][0]
  # sr = amps[str(filename)][1]
  for i in range(100):
    amp_slice = getSlice(amp, 3, sr)
    if isQuiet((amp_slice)):
      amp_slice = getSlice(amp, 3, sr)

    D = librosa.amplitude_to_db(librosa.stft(amp_slice), ref=np.max)
    A = D
    D = (255/80) * (D + 80)
    imgArray = A.astype(np.uint8)
    imgArray = imgArray[: int(imgArray.shape[0]*0.1), :]
    flipImgArray = cv2.flip(imgArray, 0)
    img = Image.fromarray(flipImgArray)
    img = img.resize((128,128), resample=PIL.Image.BICUBIC)
    img.save(savePath + filename+ "_" + str(counter) + ".png")
    counter += 1
    #todo add counter for skipped files
