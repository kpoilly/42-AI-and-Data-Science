from PIL import Image, ImageFile
from PIL import ImageFilter
from PIL import ImageEnhance
import random
import os
import numpy as np


class ImgTransformation():
    @staticmethod
    def rotate(image: ImageFile, angle=None):
        """
        Rotate the image by a given angle.
        """
        if angle is None:
            angle = random.choice(
                [random.randint(15, 45), random.randint(-45, -15)])
        return image.rotate(angle)

    @staticmethod
    def flip(image: ImageFile):
        """
        Flip the image horizontally.
        """
        return image.transpose(Image.FLIP_LEFT_RIGHT)

    @staticmethod
    def crop(image: ImageFile, crop_fraction=0.8):
        """
        Crop the image to the given box.
        """
        width, height = image.size
        new_width = int(width * crop_fraction)
        new_height = int(height * crop_fraction)
        left = (width - new_width) // 2
        top = (height - new_height) // 2
        return image.crop((left, top, left + new_width, top + new_height))

    @staticmethod
    def blur(image: ImageFile, blur_radius=2):
        """
        Blur the image by a given radius.
        """
        return image.filter(ImageFilter.GaussianBlur(blur_radius))

    @staticmethod
    def contrast(image: ImageFile, contrast_factor=2):
        """
        Adjust the contrast of the image.
        """
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(contrast_factor)

    @staticmethod
    def shear(image: ImageFile, shear_factor=0.25):
        """
        Shear the image by a given angle while maintaining the original width.
        """
        w, h = image.size
        # Source coordinates (original image corners)
        src = np.float32([
            [0, 0],
            [w, 0],
            [w, h],
            [0, h]
        ])

        # Destination coordinates - randomly generated
        # to create a shearing effect
        # Adjust these values for more/less perspective

        dst = np.float32([
            [random.randint(0, int(w * shear_factor)),
             random.randint(0, int(h * shear_factor))],
            [w - random.randint(0, int(w * shear_factor)),
             random.randint(0, int(h * shear_factor))],
            [w - random.randint(0, int(w * shear_factor)), h -
             random.randint(0, int(h * shear_factor))],
            [random.randint(0, int(w * shear_factor)), h -
             random.randint(0, int(h * shear_factor))],
        ])

        def find_coeffs(pa, pb):
            matrix = []
            for p1, p2 in zip(pa, pb):
                matrix.append([p1[0], p1[1], 1, 0, 0, 0, -
                              p2[0]*p1[0], -p2[0]*p1[1]])
                matrix.append([0, 0, 0, p1[0], p1[1], 1, -
                              p2[1]*p1[0], -p2[1]*p1[1]])

            A = np.matrix(matrix)
            B = np.array(pb).reshape(8)

            res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
            return np.array(res).reshape(8)

        matrix = find_coeffs(dst, src)

        # Apply perspective transformation
        img = image.transform(
            (w, h),
            Image.PERSPECTIVE,
            matrix,
            resample=Image.BICUBIC
        )

        return img


def save_images(images):
    """
    Save the images to the given path with the given name.
    """
    for path, image in images:
        image.save(path)
        print(f"Saved images to {path}")


def augmentation(path, save_in_local_folder=False, skip={}):
    """_summary_
    Augment images in the given path using OpenCV.
    This function applies various transformations to the images
    such as rotate, flip, skew, sher, crop and distortion.

    Args:
        path (_type_): img file path
        to be augmented
    """

    img = Image.open(path)
    names = [
        "rotate",
        "flip",
        "crop",
        "blur",
        "contrast",
        "shear"
    ]
    transformations = [
        ImgTransformation.rotate,
        ImgTransformation.flip,
        ImgTransformation.crop,
        ImgTransformation.blur,
        ImgTransformation.contrast,
        ImgTransformation.shear
    ]
    if skip.get("crop", None) is True:
        names.remove("crop")
        transformations.remove(ImgTransformation.crop)
    if skip.get("shear", None) is True:
        names.remove("shear")
        transformations.remove(ImgTransformation.shear)
    if skip.get("blur", None) is True:
        names.remove("blur")
        transformations.remove(ImgTransformation.blur)
    if skip.get("flip", None) is True:
        names.remove("flip")
        transformations.remove(ImgTransformation.flip)
    images = []
    for transformation, name in zip(transformations, names):
        new_img = transformation(img)
        output_path = "{0}_{1}.JPG".format(path[:-4] if save_in_local_folder
                                           else os.path.basename(path)[:-4],
                                           name)
        images.append((output_path, new_img))

    return images


def augmentation_from_img(img):
    """_summary_
    Augment images in the given path using OpenCV.
    This function applies various transformations to the images
    such as rotate, flip, skew, sher, crop and distortion.

    Args:
        path (_type_): img file path
        to be augmented
    """

    names = [
        "rotate",
        "flip",
        "crop",
        "blur",
        "contrast",
        "shear"
    ]
    transformations = [
        ImgTransformation.rotate,
        ImgTransformation.flip,
        ImgTransformation.crop,
        ImgTransformation.blur,
        ImgTransformation.contrast,
        ImgTransformation.shear
    ]
    images = []
    for transformation, name in zip(transformations, names):
        new_img = transformation(img)
        images.append((name, new_img))
    return images
