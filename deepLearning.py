import pandas as pd
import matplotlib.pyplot as plt
import os, os.path
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten, Dense, Conv2D, Input, MaxPooling2D, Dropout

train_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.25,
        )
test_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.25,
)
train_generator = train_datagen.flow_from_directory(
        r"C:\Users\Thomas Song\PycharmProjects\elevenlabs\data",
        target_size=(128,128),
        color_mode = "grayscale",
        batch_size=32,
        class_mode='binary',
        seed=42,
        subset="training",
)
train_generator.class_indices = {'fake_spects': 0, 'real_spects': 1}
validation_generator = test_datagen.flow_from_directory(
        r"C:\Users\Thomas Song\PycharmProjects\elevenlabs\data",
        target_size=(128,128),
        color_mode = "grayscale",
        batch_size=32,
        class_mode='binary',
        seed=42,
        subset="validation",
)
validation_generator.class_indices = {'fake_spects': 0, 'real_spects': 1}


model = Sequential(
    [
        Conv2D(32, kernel_size=(3, 3), padding="same", activation="relu", input_shape=(128,128, 1)),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(64, kernel_size=(3, 3), padding="same", activation="relu"),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(128, kernel_size=(3, 3), padding="same", activation="relu"),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(256, kernel_size=(3, 3), padding="same", activation="relu"),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(512, kernel_size=(3, 3), padding="same", activation="relu"),
        Flatten(),
        Dropout(0.4),
        Dense(256, activation="relu"),
        Dense(64, activation="relu"),
        Dense(1, activation="sigmoid"),
    ]
)
model.summary()


from tensorflow.keras.optimizers import Adam
model.compile(
    optimizer=Adam(learning_rate=1E-4),
    loss="binary_crossentropy",
    metrics=["accuracy"],
)

checkpoint_filepath = 'checkpoint.keras'
# !rm "$checkpoint_filepath"/ -r
# os.makedirs(checkpoint_filepath, exist_ok=True)
model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_filepath,
    save_weights_only=False,
    monitor='val_accuracy',
    mode='max',
    save_best_only=True)

early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_accuracy', patience=10, restore_best_weights=True)

history = model.fit(
    train_generator,
    epochs=50,
    batch_size=256,
    validation_data=validation_generator,
    callbacks=[model_checkpoint_callback, early_stopping],
)

df_history = pd.DataFrame(history.history)
df_history["epoch"] = history.epoch
df_history

# if validation score is higher than training score, it could mean high bias: https://stackoverflow.com/a/45854380
with plt.style.context("fivethirtyeight"):
  ax = df_history.plot(x="epoch", y=["accuracy", "val_accuracy"], figsize=(15,10), title="Learning curve");
  ax.set_ylabel("score")
  plt.show()
