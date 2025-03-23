from tensorflow.keras.utils import image_dataset_from_directory


def load(path: str, batch_size=32):
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
    print(f"Loaded df_train:{df_train.element_spec} - {len(df_train)} elements.")
    print(f"Loaded df_val:{df_val.element_spec} - {len(df_val)} elements.")
    return df_train, df_val