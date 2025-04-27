#!./leaf_venv/bin/python3

from utils import Argument, StaticValidators
from distribution import distribution, plot_distribution
import sys
import matplotlib

matplotlib.use('TkAgg')


def arguments_logic():
    cls = Argument("Display the distribution of the dataset")
    cls.add_argument(
        "directory",
        str,
        "Path to the directory containing the dataset",
        default="data/"
    )
    args = cls.get_args()
    cls.add_validator(StaticValidators.validate_path_dir, args.directory)
    cls.validate()
    return args


if __name__ == "__main__":
    try:
        args = arguments_logic()
        dist = distribution(args.directory)
        plot_distribution(dist)
        exit(0)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        exit(1)
