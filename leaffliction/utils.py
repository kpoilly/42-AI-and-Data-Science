from tensorflow.keras.utils import image_dataset_from_directory


def load(path: str):
    """
    Loads a csv file and returns it as a panda DataFrame
    """
    try:
        dataset = image_dataset_from_directory(path, image_size(128, 128))
    except FileNotFoundError:
        raise AssertionError(f"file {path} not found.")
    print("Loading dataset of dimensions", dataset.shape)
    return dataset