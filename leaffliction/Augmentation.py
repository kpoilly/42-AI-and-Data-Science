#!./leaf_venv/bin/python3

from utils import Argument, StaticValidators
from augmentation import augmentation, save_images
import sys
import os
import matplotlib

matplotlib.use('TkAgg')


def arguments_logic():
    cls = Argument(
        "Create images with different transformation \
from an image passed as parameters")
    cls.add_argument(
        "file",
        str,
        "Path to the img file",
    )
    cls.add_argument("--max",
                     help="Max the number of images saved",
                     type=int, nargs="?")
    cls.add_argument("--skip-crop",
                     help="Skip the crop augmentation",
                     action="store_true")
    cls.add_argument("--skip-shear",
                     help="Skip the shear augmentation",
                     action="store_true")
    cls.add_argument("--skip-blur",
                     help="Skip the blur augmentation",
                     action="store_true")
    cls.add_argument("--skip-flip",
                     help="Skip the flip augmentation",
                     action="store_true")
    args = cls.get_args()
    cls.add_validator(StaticValidators.validate_path, args.file)
    cls.validate()
    return args


def augmentation_dir(path, skip):
    """
    This function creates a list of images from a directory.
    """
    allowed_extensions = (".jpg", ".JPG", ".jpeg")
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(allowed_extensions):
                img_path = os.path.join(root, file)
                images = augmentation(img_path, True, skip)
                count += len(images)
                save_images(images)
                if skip.get("max", None) is not None and count >= skip["max"]:
                    print(f"Max number of images reached: {count}")
                    break


if __name__ == "__main__":
    try:
        args = arguments_logic()
        if os.path.isdir(args.file):
            augmentation_dir(args.file, skip={
                "crop": args.skip_crop,
                "shear": args.skip_shear,
                "blur": args.skip_blur,
                "flip": args.skip_flip,
                "max": args.max
            })
        else:
            images = augmentation(args.file, skip={
                "crop": args.skip_crop,
                "shear": args.skip_shear,
                "blur": args.skip_blur,
                "flip": args.skip_flip
            })
            save_images(images)
        exit(0)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        exit(1)
