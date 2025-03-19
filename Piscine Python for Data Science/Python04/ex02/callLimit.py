import sys


def callLimit(limit: int):
    """
    Mean to be used as a decorator
    blocks the execution of a function above a limit
    """
    count = 0

    def callLimiter(function):

        def limit_function(*args, **kwds):
            try:
                nonlocal count
                count += 1
                if count <= limit:
                    return function(*args, **kwds)
                else:
                    raise AssertionError(f"{function} called too many times.")
            except AssertionError as e:
                print("AssertionError:", e, file=sys.stderr)
        return limit_function
    return callLimiter
