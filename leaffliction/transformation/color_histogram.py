
import matplotlib.pyplot as plt
from plantcv import plantcv as pcv


def plot_stat_hist(key, val):
    scl, color = val
    # outputs observation of the last pcv
    y = pcv.outputs.observations['default_1'][f"{key}_frequencies"]['value']
    x = [
        i * scl
        for i in pcv.outputs.observations['default_1'][
            f"{key}_frequencies"
        ]['label']
    ]
    # normalize the hue from 0 - 360 to 0 - 180
    if key == "hue":
        x = x[:127]
        y = y[:127]

    # recenter the blue-yellow and green-magenta on the 0-255 scale
    # CIELAB a* and b* are unsigned integers
    if (
        key == "blue-yellow" or
        key == "green-magenta"
    ):
        x = [x + 128 for x in x]

    return (x, y, color)


def plot_histogram(image, mask, display_func=None):

    # Create a dictionary to store the labels and their corresponding scale
    # some labels are on % so they are multiplied by 2.55
    dict_label = {
        "blue": [1, 'blue'],
        "green": [1, 'green'],
        "green-magenta": [1, (1, 0, 1)],
        "blue-yellow": [1, (1, 1, 0)],
        "red": [1, 'red'],
        "hue": [1, (0, 1, 1)],
        "lightness": [2.55, 'orange'],
        "saturation": [2.55, 'grey'],
        "value": [2.55, 'purple'],
    }

    pcv.analyze.color(
        image,
        mask,
        colorspaces="all",
        label="default"
    )

    fig, ax = plt.subplots(figsize=(16, 9))
    for key, val in dict_label.items():
        x, y, color = plot_stat_hist(key, val)
        plt.plot(
            x,
            y,
            color=color,
            label=key,
            linewidth=2,
        )

    plt.legend(dict_label.keys(), loc="upper right")

    plt.title("Color histogram")
    plt.xlabel("Pixel intensity")
    plt.xticks(range(0, 256, 25))
    plt.ylabel("Proportion of pixels (%)")
    plt.grid(
        visible=True,
        which='major',
        axis='both',
        linestyle='--',
    )
    if display_func is not None:
        display_func(fig)
    else:
        plt.show()
        plt.close()
