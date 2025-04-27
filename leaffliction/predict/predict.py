import os
from typing import List
import numpy as np
import cv2
from keras.api.models import load_model
from keras import Model
from transformation import transformation


def get_image(img_path: str, models_name: List[str]) -> tuple:
    transformations = {name for name in models_name}
    transformations = transformation(
        img_path, "", None, transformations)

    def get_array_imgage(image):
        img_array = cv2.resize(image, (128, 128))
        img_array = np.array(cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB))
        img_array = np.expand_dims(img_array, axis=0)
        return img_array

    return [(name, get_array_imgage(transformations[name]))
            for name in models_name]


def predict_images(img_tuple: any, models: dict[str, Model]):
    class_names = ["Apple_Black_rot",
                   "Apple_healthy",
                   "Apple_rust",
                   "Apple_scab",
                   "Grape_Black_rot",
                   "Grape_Esca",
                   "Grape_healthy",
                   "Grape_spot"]

    images, filename = img_tuple

    print(f"\nPredicting {filename}...")

    def get_prediction(image):
        name, img_array = image
        model = models[name]
        prediction = model.predict(img_array)
        predicted_class = class_names[np.argmax(prediction[0])].lower()
        isValid = predicted_class in filename.lower()
        return name, predicted_class, isValid, prediction,

    predictions_results = dict()
    result_by_model = [get_prediction(image)
                       for image in images]
    for name, predicted_class, isValid, _ in result_by_model:
        predictions_results[name] = isValid, predicted_class

    predictions = [result[-1] for result in result_by_model]
    predictions = np.sum(predictions, axis=0)
    prediction = np.argmax(predictions[0])
    predicted_class = class_names[prediction].lower()
    isValid = predicted_class in filename.lower()

    predictions_results["final"] = isValid, predicted_class
    if isValid:
        print(f"\033[92mPredicted class: {predicted_class}\033[0m")
    else:
        print(f"\033[91mPredicted class: {predicted_class}\033[0m")
    return predictions_results


def load_models(models_name: List[str] = None) -> dict[str, Model]:
    try:
        models = dict()
        for name in models_name:
            models[name] = load_model(os.path.join(
                "model", f"model_{name}.keras"))
        print("Models loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        return None
    return models


def predict_from_file(file, filename='filename',
                      models_name: List[str] = None):
    models = load_models(models_name)
    if models is None:
        return None

    try:
        predictions = []
        images = get_image(file, models_name)
        predictions.append(predict_images(
            (images, filename), models))
        accuracy = print_accuracy_report(predictions)
        return predictions, accuracy
    except Exception as e:
        print(f"Error processing image: {e}")
        return None


def predict(path: str, models_name: List[str] = None) -> List[bool]:
    models = load_models(models_name)
    if models is None:
        return None

    try:
        predictions = []
        if not os.path.exists(path):
            raise FileNotFoundError(f"Image file '{path}' not found.")

        if os.path.isdir(path):
            for filename in os.listdir(path):
                if filename.endswith(('.JPG', '.jpeg', '.png')):
                    images = get_image(os.path.join(
                        path, filename), models_name)
                    predictions.append(predict_images(
                        (images, filename), models))
        elif os.path.isfile(path):
            images = get_image(path, models_name)
            predictions.append(predict_images(
                (images, os.path.basename(path)), models))
        else:
            raise ValueError("Invalid path. Must be a file or directory.")
        accuracy = print_accuracy_report(predictions)
        return predictions, accuracy
    except Exception as e:
        print(f"Error processing image: {e}")
        return None


def calculate_model_accuracy(predictions_list):
    """
    Calculate accuracy for each model from a list of prediction results.

    Args:
        predictions_list: List of dictionaries
          containing model predictions as (bool, class) tuples

    Returns:
        Dictionary of model names with their accuracy scores
    """
    if not predictions_list:
        return {}

    # Initialize counters
    model_counts = {}
    model_correct = {}

    # Process each prediction
    for pred_dict in predictions_list:
        for model_name, (is_correct, _) in pred_dict.items():
            # Initialize counters for new models
            if model_name not in model_counts:
                model_counts[model_name] = 0
                model_correct[model_name] = 0

            # Update counters
            model_counts[model_name] += 1
            if is_correct:
                model_correct[model_name] += 1

    # Calculate accuracy percentages
    model_accuracy = {}
    for model_name in model_counts:
        accuracy = model_correct[model_name] / model_counts[model_name]
        model_accuracy[model_name] = (accuracy,
                                      model_correct[model_name],
                                      model_counts[model_name])

    return model_accuracy


def print_accuracy_report(predictions_list):
    """Print a formatted accuracy report for all models"""
    accuracy = calculate_model_accuracy(predictions_list)
    if not accuracy:
        print("No predictions to evaluate.")
        return
    print("\nAccuracy Results:")
    result = "-" * 30
    for model, value in accuracy.items():
        acc, correct, total = value
        result += f"\n{model.ljust(10)}: {acc:.2%} ({correct}/{total})"

    # Find best model
    best_model = max(accuracy.items(), key=lambda x: x[1][0])
    result += f"\n\nBest model: {best_model[0]} with \
{best_model[1][0]:.2%} accuracy"
    print(result)
    return result
