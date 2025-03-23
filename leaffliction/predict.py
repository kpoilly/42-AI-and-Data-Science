import tensorflow as tf
from tensorflow.keras import models



def predict(image_path, model):
    # Load image
    # Transform image
    # make prediction for each image
    # argmax is our pred
    pass


def main():
    # A recup en argparse
    to_predict_path = ""
    model_path = "models/model.keras"
    model = models.load_model(model_path)
    
    print(f"Model @{model_path} loaded.")
    print(model.summary())
    

if __name__ == "__main__":
    main()