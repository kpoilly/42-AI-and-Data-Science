#!./leaf_venv/bin/python3

from utils import Argument, StaticValidators
from transformation import transformation
import sys
import os
import matplotlib

matplotlib.use('TkAgg')


def arguments_logic():
    cls = Argument(
        "Create images with different transformation \
from an image/dir passed as parameters")
    cls.add_argument(
        "-src",
        type=str,
        help="Path to the img file",
    )
    cls.add_argument(
        "-dst",
        type=str,
        help="Path to the directory to save the images",
        default="output/"
    )
    cls.add_argument(
        "--mask",
        action="store_true",
        help="Do the mask transformation",
    )
    cls.add_argument(
        "--analyze",
        action="store_true",
        help="Do the analyze transformation",
    )
    cls.add_argument(
        "--no_bg",
        action="store_true",
        help="Do the no_bg transformation",
    )
    args = cls.get_args()
    cls.add_validator(StaticValidators.validate_path, args.src)
    cls.validate()
    transformations = set()
    if args.mask:
        transformations.add("mask")
    if args.analyze:
        transformations.add("analyze")
    if args.no_bg:
        transformations.add("no_bg")
    return args, transformations


def transformation_dir(path, output_dir, transformations):
    """
    This function creates a list of images from a directory.
    """
    count = 0
    allowed_extensions = (".jpg", ".JPG", ".jpeg")
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(allowed_extensions):
                img_path = os.path.join(root, file)
                relative_path = os.path.commonpath([path, root])
                new_path = os.path.relpath(root, relative_path)
                output_subdir = os.path.join(
                    output_dir, new_path) if new_path != "." else output_dir
                if not os.path.exists(output_subdir):
                    os.makedirs(output_subdir)
                output_file_basename = os.path.join(
                    output_subdir, file[:-4])
                transformation(img_path, output_file_basename,
                               "print", transformations)

                count += 1
                print(f"{count} {count / 16}%", end="\r")


def main():
    args, transformations = arguments_logic()

    if os.path.isdir(args.src):
        if not os.path.exists(args.dst):
            os.makedirs(args.dst)
        transformation_dir(args.src, args.dst, transformations)
    else:
        transformation(
            args.src, args.dst, "plot", transformations)


if __name__ == "__main__":
    try:
        main()
        exit(0)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        exit(1)
