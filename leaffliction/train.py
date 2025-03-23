import os
import sys
import cv2
import numpy as np
import pandas as pd

from utils import load

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.utils import image_dataset_from_directory


def create_model(nb_outputs, nb_filters=64, dropout=0.5):
    model = model.Sequential()
    model.add(layers.Rescaling(1.0 / 255))
    model.add(layers.BatchNormalization())
    model.add(layers.Conv2D(nb_filters, (3, 3), activation="ReLU"))
    model.add(layers.MaxPooling2D(2, 2))
    model.add(layers.BatchNormalization())
    model.add(layers.Conv2D(nb_filters, (3, 3), activation="ReLU"))
    model.add(layers.MaxPooling2D(2, 2))
    model.add(layers.BatchNormalization())
    model.add(layers.Conv2D(32, (1, 1), activation="ReLU"))
    model.add(layers.MaxPooling2D(2, 2))
    model.add(layers.Flatten())
    model.add(layers.Dense(512, activation="ReLU"))
    model.add(layers.Dropout(dropout))
    model.add(layers.Dense(256, activation="ReLU"))
    model.add(layers.Dense(nb_outputs, activation="Softmax"))
    model.compile(
        optimizer="ADAM",
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=["accuracy"],
    )
    return model


def train(df, df_val, nb_filters=64, dropout=0.5, epochs=100):
    print(f"Starting model's training with Settings :\n{epochs} epochs\n\
          Convolution filters: {nb_filters}\nDropout: {dropout}")
    model = create_model(len(df.class_names), nb_filters, dropout)
    model.fit(df, epochs=epochs, validation_data=df_val)

    loss, accu = model.evaluate(df_val)
    print(f"Model trained.\nLoss: {loss}\nAccuracy: {round(accu * 100, 5)}%")

    # Save the model etc, zip etc...

def main():
    # Replace with argparse
    df_train_path = "./data/Apple_scab"
    df_val_path = "./data/Apple_scab"
    
    # Add nb epochs, nb filters, dropout and other
    # training settings with argparse
    
    try:
        df_train = load(df_train_path)
        df_val = load(df_val_path)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        exit()
    
    train(df_train, df_val, 64, 0.5, 100)


if __name__ == "__main__":
    main()
