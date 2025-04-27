import os
import tensorflow as tf
import matplotlib.pyplot as plt
from keras import layers, models
from keras.api.callbacks import EarlyStopping
from keras.api.utils import image_dataset_from_directory
import matplotlib
matplotlib.use('TkAgg')


def load_split_dataset(path: str, batch_size=128):
    """
    Loads directory of images and split it into 2 tf.Datasets
    (train and validation)
    """
    try:
        df_train, df_val = image_dataset_from_directory(path,
                                                        image_size=(128, 128),
                                                        batch_size=batch_size,
                                                        validation_split=0.2,
                                                        subset='both',
                                                        shuffle=True,
                                                        seed=42
                                                        )
    except FileNotFoundError:
        raise AssertionError(f"file {path} not found.")
    print(
        f"Loaded df_train: {df_train.element_spec} \
- {len(df_train)} elements.")
    print(f"Loaded df_val: {df_val.element_spec} - {len(df_val)} elements.")
    return df_train, df_val


# Add this new class to track batch-level metrics
class BatchHistory(tf.keras.callbacks.Callback):
    def __init__(self):
        super().__init__()
        self.batch_losses = []
        self.batch_accuracies = []
        self.batch_nums = []
        self.current_batch = 0
        # Keep track of epoch boundaries for plotting
        self.epoch_boundaries = [0]

    def on_train_batch_end(self, batch, logs=None):
        self.batch_losses.append(logs.get('loss'))
        self.batch_accuracies.append(logs.get('accuracy'))
        self.batch_nums.append(self.current_batch)
        self.current_batch += 1

    def on_epoch_end(self, epoch, logs=None):
        # Mark the boundary between epochs
        self.epoch_boundaries.append(self.current_batch)


def draw_training(history, batch_history, name):
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs_range = range(len(acc))

    # Create a figure with 4 subplots (2 rows, 2 columns)
    plt.figure(figsize=(15, 10))

    # 1. Epoch-level accuracy
    plt.subplot(2, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Epoch-level Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')

    # 2. Epoch-level loss
    plt.subplot(2, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Epoch-level Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')

    # 3. Batch-level accuracy
    plt.subplot(2, 2, 3)
    plt.plot(batch_history.batch_nums,
             batch_history.batch_accuracies, label='Batch Accuracy')
    # Add vertical lines to indicate epoch boundaries
    for boundary in batch_history.epoch_boundaries[1:-1]:
        plt.axvline(x=boundary, color='r', linestyle='--', alpha=0.3)
    plt.legend(loc='lower right')
    plt.title('Batch-level Accuracy')
    plt.xlabel('Batch')
    plt.ylabel('Accuracy')

    # 4. Batch-level loss
    plt.subplot(2, 2, 4)
    plt.plot(batch_history.batch_nums,
             batch_history.batch_losses, label='Batch Loss')
    # Add vertical lines to indicate epoch boundaries
    for boundary in batch_history.epoch_boundaries[1:-1]:
        plt.axvline(x=boundary, color='r', linestyle='--', alpha=0.3)
    plt.legend(loc='upper right')
    plt.title('Batch-level Loss')
    plt.xlabel('Batch')
    plt.ylabel('Loss')

    plt.tight_layout()
    os.makedirs('metrics', exist_ok=True)
    plot_path = os.path.join("metrics", f"training_history_{name}.png")
    plt.savefig(plot_path)
    print(f"Training history plot saved to '{plot_path}'")


def create_model(nb_outputs, nb_filters=64, dropout=0.5):
    model = models.Sequential([
        layers.Rescaling(1.0 / 255),
        layers.BatchNormalization(),
        layers.SeparableConv2D(nb_filters, (3, 3), activation="relu"),
        layers.MaxPooling2D(2, 2),
        layers.BatchNormalization(),
        layers.SeparableConv2D(nb_filters, (3, 3), activation="relu"),
        layers.MaxPooling2D(2, 2),
        layers.BatchNormalization(),
        layers.SeparableConv2D(nb_filters // 2, (1, 1), activation="relu"),
        layers.MaxPooling2D(2, 2),
        layers.Flatten(),
        layers.Dense(256, activation="relu"),
        layers.Dropout(dropout),
        layers.Dense(128, activation="relu"),
        layers.Dense(nb_outputs, activation="softmax")
    ])
    model.compile(
        optimizer="adam",
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
        metrics=["accuracy"],
    )
    return model


def train(df, df_val, name, nb_filters=48, dropout=0.3, epochs=10, patience=3):
    print(f"{name} | Starting model's training with settings:\
\n{epochs} epochs\
\nConvolution filters: {nb_filters}\
\nDropout: {dropout}")

    model = create_model(len(df.class_names), nb_filters, dropout)
    early_stop = EarlyStopping(
        monitor='val_loss',
        patience=patience,
        verbose=1,
        mode='min',
        restore_best_weights=True
    )
    batch_history = BatchHistory()
    history = model.fit(df,
                        epochs=epochs,
                        validation_data=df_val,
                        callbacks=[early_stop, batch_history])

    loss, accuracy = model.evaluate(df_val)
    print(f"Val Loss: {loss:.4f}")
    print(f"Val Accuracy: {accuracy:.4f}")

    draw_training(history, batch_history, name)
    print(model.summary())

    return model
