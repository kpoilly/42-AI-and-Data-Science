import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('gtk3agg')


def ft_invert(array) -> np.array:
    """
    Inverts the color of the image received.
    """
    # = + - *
    img = np.invert(array)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(img)
    plt.savefig("invert.png")


def ft_red(array) -> np.array:
    """
    Converts the color of the image received to shades of red.
    """
    # = *
    img = array[:, :, 1]
    img_rgb = np.stack([img, np.zeros_like(img), np.zeros_like(img)], axis=-1)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(img_rgb)
    plt.savefig("red.png")


def ft_green(array) -> np.array:
    """
    Converts the color of the image received to shades of green.
    """
    # = -
    img = array[:, :, 1]
    img_rgb = np.stack([np.zeros_like(img), img, np.zeros_like(img)], axis=-1)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(img_rgb)
    plt.savefig("green.png")


def ft_blue(array) -> np.array:
    """
    Converts the color of the image received to shades of blue.
    """
    # =
    img = array[:, :, 0]
    img_rgb = np.stack([np.zeros_like(img), np.zeros_like(img), img], axis=-1)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(img_rgb)
    plt.savefig("blue.png")


def ft_grey(array) -> np.array:
    """
    Converts the color of the image received to shades of grey.
    """
    # = /
    img = array[:, :, 0]
    img = np.stack([np.zeros_like(img), np.zeros_like(img),
                    np.zeros_like(img)], axis=-1)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(img)
    plt.savefig("grey.png")
