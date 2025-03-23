import os
import sys
import cv2
import numpy as np
import pandas as pd

from utils import load

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.utils import image_dataset_from_directory
from tensorflow.keras.callbacks import EarlyStopping


def create_model(nb_outputs, nb_filters=64, dropout=0.5):
    model = models.Sequential()
    model.add(layers.Rescaling(1.0 / 255))
    model.add(layers.BatchNormalization())
    model.add(layers.Conv2D(nb_filters, (3, 3), activation="relu"))
    model.add(layers.MaxPooling2D(2, 2))
    model.add(layers.BatchNormalization())
    model.add(layers.Conv2D(nb_filters, (3, 3), activation="relu"))
    model.add(layers.MaxPooling2D(2, 2))
    model.add(layers.BatchNormalization())
    model.add(layers.Conv2D(32, (1, 1), activation="relu"))
    model.add(layers.MaxPooling2D(2, 2))
    model.add(layers.Flatten())
    model.add(layers.Dense(512, activation="relu"))
    model.add(layers.Dropout(dropout))
    model.add(layers.Dense(256, activation="relu"))
    model.add(layers.Dense(nb_outputs, activation="softmax"))
    model.compile(
        optimizer="adam",
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=["accuracy"],
    )
    return model


def train(df, df_val, nb_filters=64, dropout=0.5, epochs=10, patience=3):
    print(f"Starting model's training with settings:\n{epochs} epochs\n\
Convolution filters: {nb_filters}\nDropout: {dropout}")
    model = create_model(len(df.class_names), nb_filters, dropout)
    
    early_stop = EarlyStopping(
        monitor='val_loss',
        patience=patience,
        verbose=1,
        mode='min',
        restore_best_weights=True
    )
    
    history = model.fit(df,
                        epochs=epochs,
                        validation_data=df_val
                        callbacks=[early_stop])

    loss, accu = model.evaluate(df_val)
    print(f"Model trained.\nLoss: {loss}\nAccuracy: {round(accu * 100, 4)}%")

    # Save the model etc, zip etc...

def main():
    # Replace with argparse
    data_path = "data"
    
    # Add batch_size, nb epochs, nb filters, dropout and other
    # training settings with argparse
    
    try:
        df_train, df_val = load(data_path, 32)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        exit()
    
    train(df_train, df_val, 64, 0.5, 3)


if __name__ == "__main__":
    main()
