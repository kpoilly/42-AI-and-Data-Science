import argparse
import os


class StaticValidators:
    @staticmethod
    def validate_path(path_str):
        """
        This function checks if the given path is a valid path.
        If it is not, it raises an AssertionError with a message.
        """
        if not os.path.exists(path_str):
            raise AssertionError(f"Path {path_str} does not exist.")

    @staticmethod
    def validate_path_dir(path_str):
        """
        This function checks if the given path is a directory.
        If it is not, it raises an AssertionError with a message.
        """
        if not os.path.isdir(path_str):
            raise AssertionError(f"Path {path_str} is not a directory.")

    @staticmethod
    def validate_imgFile(
        path_str, allowed_extensions=[".jpg", ".jpeg", ".JPG", ".png"]
    ):
        """
        This function checks if the given path is a file.
        If it is not, it raises an AssertionError with a message.
        """
        if not os.path.isfile(path_str):
            raise AssertionError(f"{path_str} is not a file.")

        if not any(path_str.endswith(ext) for ext in allowed_extensions):
            raise AssertionError(f"File {path_str} is not a valid image file.")

    @staticmethod
    def validate_number(args):
        """
        This function checks if the given path is a directory.
        If it is not, it raises an AssertionError with a message.
        """
        value, min_value, max_value = args
        if not isinstance(value, (int)):
            raise AssertionError(f"Value {value} is not a number.")
        if min_value is not None and value < min_value:
            raise AssertionError(
                f"Value {value} is less than minimum {min_value}.")
        if max_value is not None and value > max_value:
            raise AssertionError(
                f"Value {value} is greater than maximum {max_value}.")


class ArgumentValidator():
    def __init__(self):
        self.validators = []

    def validate(self):
        """
        This function validates the arguments using the provided validator.
        """
        try:
            for validator, args in self.validators:
                validator(args)
        except AssertionError as e:
            print(f"Validation error: {e}")
            raise

    def add_validator(self, validator, args):
        """
        This function adds a validator to the list of validators.
        """
        self.validators.append((validator, args))


class Argument(ArgumentValidator):
    def __init__(self, description=""):
        self.parser = argparse.ArgumentParser(description=description)
        super().__init__()

    def add_argument(self, arg_name, type=None, help="",
                     default=None, action=None, nargs=None):
        """
        This function adds an argument to the parser.
        """
        kwargs = {
            'help': help,
        }
        if nargs is not None:
            kwargs['nargs'] = nargs

        if action == 'store_true':
            kwargs['action'] = 'store_true'
        else:
            kwargs['type'] = type
            kwargs['default'] = default

        self.parser.add_argument(arg_name, **kwargs)

    def add_validator(self, validator, args):
        return super().add_validator(validator, args)

    def get_args(self):
        args = self.parser.parse_args()
        return args

    def validate_path_dir(self, path_str):
        """
        This function checks if the given path is a directory.
        If it is not, it raises an AssertionError with a message.
        """
        if not os.path.isdir(path_str):
            raise AssertionError(f"Path {path_str} is not a directory.")
