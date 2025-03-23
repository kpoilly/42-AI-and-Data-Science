from tensorflow.keras.utils import image_dataset_from_directory


def load(path: str):
    """
    Loads an image and returns it as a tf.Dataset
    """
    try:
        dataset = image_dataset_from_directory(path, image_size=(128, 128), shuffle=True)
    except FileNotFoundError:
        raise AssertionError(f"file {path} not found.")
    print("Loading dataset of dimensions", dataset.element_spec)
    return dataset