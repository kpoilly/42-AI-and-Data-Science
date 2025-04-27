#!./leaf_venv/bin/python3

import os
import sys
from predict import predict
from utils import Argument, StaticValidators

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def arguments_logic():
    cls = Argument(
        "Create images with different transformation \
from an image passed as parameters")
    cls.add_argument(
        "file",
        str,
        "Path to the img file",
    )
    args = cls.get_args()
    cls.add_validator(StaticValidators.validate_path, args.file)
    cls.validate()
    return args


def main(args):
    image_path = args.file

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"image file '{image_path}' not found.")
    models_name = ["original", "mask", "no_bg"]
    predict(image_path, models_name)


if __name__ == "__main__":
    try:
        args = arguments_logic()
        main(args)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        exit(1)
