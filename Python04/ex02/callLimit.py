def callLimit(limit: int):
    count = 0
    def callLimiter(function):
        def limit_function(*args, **kwds):
        #your code here