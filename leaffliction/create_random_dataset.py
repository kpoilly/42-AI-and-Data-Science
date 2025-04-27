#!./leaf_venv/bin/python3

import os
import sys
import random
import shutil
from utils import Argument, StaticValidators


def create_random_dataset(source_dir, output_dir, images_per_class=10):
    """
    Create a new dataset by randomly selecting images from each class folder.

    Args:
        source_dir: Path to the source directory containing class folders
        output_dir: Path to the output directory
                    where random images will be copied
        images_per_class: Number of random images to select from each class
    """
    os.makedirs(output_dir, exist_ok=True)

    class_folders = [f for f in os.listdir(source_dir)
                     if os.path.isdir(os.path.join(source_dir, f))]

    print(f"Found {len(class_folders)} class folders: {class_folders}")

    total_copied = 0

    # Process each class folder
    for class_folder in class_folders:
        class_path = os.path.join(source_dir, class_folder)

        # Get all image files in the class folder
        image_files = [f for f in os.listdir(class_path)
                       if f.lower().endswith(('.jpg',
                                              '.jpeg', '.png', '.JPG'))]

        num_to_select = min(len(image_files), images_per_class)

        if num_to_select == 0:
            print(f"No images found in {class_folder}, skipping")
            continue

        print(f"Selecting {num_to_select} random images from {class_folder}")

        # Randomly select images
        selected_images = random.sample(image_files, num_to_select)

        # Copy and rename each selected image
        for i, image_file in enumerate(selected_images):
            source_path = os.path.join(class_path, image_file)

            # Get file extension from original file
            _, ext = os.path.splitext(image_file)
            if not ext:
                ext = ".JPG"  # Default extension if none is found

            # Create new filename with the pattern folderName_number.JPG
            new_filename = f"{class_folder}_{i+1}{ext}"
            dest_path = os.path.join(output_dir, new_filename)

            # Copy the file
            shutil.copy2(source_path, dest_path)
            print(f"  Copied: {image_file} → {new_filename}")
            total_copied += 1

    print(f"\nSummary: Copied {total_copied} images to {output_dir}")


def arguments_logic():
    cls = Argument("Create a random dataset from class folders")
    cls.add_argument("--src", type=str, default="data/images",
                     help="Source directory containing class folders")
    cls.add_argument("--dst", type=str, default="data/random_dataset",
                     help="Output directory for the random dataset")
    cls.add_argument("--count", type=int, default=10,
                     help="Number of random images to select from each class")
    args = cls.get_args()
    cls.add_validator(StaticValidators.validate_path_dir, args.src)
    cls.add_validator(StaticValidators.validate_number, (args.count, 1, 200))
    cls.validate()
    return args


if __name__ == "__main__":
    try:
        args = arguments_logic()
        create_random_dataset(
            args.src, args.dst, args.count)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        exit(1)
