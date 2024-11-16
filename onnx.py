import tensorflow as tf
import json
import sys
import os
import time
import numpy as np
import cv2
import onnx
import onnxruntime
import logging
import PIL
from PIL import Image, ImageOps
import librosa

# import spleeter

path = r"C:\Users\Thomas Song\Downloads\2024-10-27 19-00-38.mp3"

# def makePrediction:
if not os.path.exists(path):
    raise FileNotFoundError(f"Audio file not found: {path}")


def save_random_crop(imgArray: np.ndarray, crop_width: int, outputPath: str, file_counter: int,
                     cropCounter: int) -> bool:
    start_index = np.random.randint(0, imgArray.shape[1] - crop_width)
    crop_imgArray = imgArray[:, start_index: crop_width + start_index]
    # print(crop_imgArray.mean())

    if crop_imgArray.mean() > 5:

        crop_img = Image.fromarray(crop_imgArray)
        crop_img = crop_img.resize((128, 128), resample=Image.BICUBIC)

        save_path = f"{outputPath}image{file_counter}_{cropCounter}.png"
        crop_img.save(save_path)
        logging.debug(f"saved crop to {save_path}")

        return True
    else:
        logging.debug(f"Crop is too dark to be saved! Mean brightness {crop_imgArray.mean()}")
        return False


def multithread(imgArray: np.ndarray, crop_width: int, outputPath: str, counter: int) -> int:
    save_random_crop(
        imgArray=imgArray,
        crop_width=crop_width,
        outputPath=outputPath,
        file_counter=counter,
        cropCounter=0)


def makeImgArray(path, batchSize: int = 1):
    # CMD = f"spleeter separate -o audio_output \"{path}\""
    # print(f"CMD: {CMD}")
    # os.system(CMD)

    vocalsPath = path  # f"/content/audio_output{path[8:len(path)-4]}/vocals.wav"

    result = []
    amps = {}
    window_legnth_sec = 3
    contrastFactor = 1  # high val = high contrast
    amp, sr = librosa.load(vocalsPath)
    for i in range(batchSize):
        D = librosa.feature.melspectrogram(y=amp, sr=sr, n_fft=2048, hop_length=512, n_mels=2000)
        D = 255 * 2 * (1 / (1 + np.exp(-D * contrastFactor)) - 0.5)

        imgArray = D[:int(D.shape[0] * 0.1), :][::-1, :].astype(np.uint8)

        duration = len(amp) / sr
        crop_percentage = window_legnth_sec / duration
        crop_width = int(imgArray.shape[1] * crop_percentage)
        if imgArray.shape[1] <= crop_width:
            print(imgArray)
        #   logging.info(f"Audio is too short!")
        multithread(
            imgArray=imgArray,
            crop_width=crop_width,
            outputPath="content/New Recording 19",
            counter=0)
        imgPath = r"content/New Recording 19image0_0.png"
        img = Image.open(imgPath).convert("L")
        result.append(np.array(img).reshape(1, 128, 128, 1) / 255)
    if len(result) == 1:
        return result[0]

    return result


img = makeImgArray(path)  # path is an audio file

data = json.dumps({'data': img.tolist()})
data = np.array(json.loads(data)['data']).astype('float32')

onnx_model_path = "voice_cnn.onnx"
session = onnxruntime.InferenceSession(onnx_model_path, None)
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name
print(input_name)
print(output_name)

result = session.run([output_name], {input_name: data})
prob = np.array(result).squeeze()
print(f"Probabilities: {prob}")
if prob < 0.5:  # np.argmax(prob, axis=0) is for multi-class classification where the NN has multiple neurons (with softmax activation) in the output layer
    print(f"Final predicted class: fake")
else:
    print(f"Final predicted class: real " + str(prob))
