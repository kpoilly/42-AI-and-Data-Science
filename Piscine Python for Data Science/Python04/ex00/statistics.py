def ft_mean(vec):
    """
Calculate the mean of a vector
    """
    mean = 0
    for elem in vec:
        mean += elem
    return mean / len(vec)


def ft_median(vec):
    """
Calculate the median of a vector
    """
    vec.sort()
    if len(vec) % 2 != 0:
        return vec[int((len(vec) - 1) / 2)]
    else:
        return (vec[int(len(vec) / 2)] +
                vec[int((len(vec) / 2) - 1)]) / 2


def ft_quartile(vec):
    """
Calculate the q1 and q3 of a vector
    """
    vec.sort()
    pos_q1 = len(vec) // 4
    pos_q3 = pos_q1 * 3

    if len(vec) % 4 == 0:
        q1 = float(vec[int(pos_q1) - 1]) + float(vec[int(pos_q1)]) / 2
        q3 = float(vec[int(pos_q3) - 1]) + float(vec[int(pos_q3)]) / 2
    else:
        q1 = float(vec[int(pos_q1)])
        q3 = float(vec[int(pos_q3)])
    return [q1, q3]


def ft_std(vec):
    """
Calculate the standard deviation of a vector
    """
    return ft_var(vec) ** 0.5


def ft_var(vec):
    """
Calculate the variance of a vector
    """
    mean = ft_mean(vec)
    res = sum((i - mean) ** 2 for i in vec) / len(vec)
    return res


def ft_statistics(*args, **kwargs) -> None:
    """
ft_statistics

print the result of given operations on given numbers.

Possible operations:
    mean
    median
    quartile
    std
    var
    """
    vec = []
    ops = {"mean": ft_mean,
           "median": ft_median,
           "quartile": ft_quartile,
           "std": ft_std,
           "var": ft_var}

    for elem in range(len(args)):
        vec.append(args[elem])
    for val in kwargs.values():
        if len(vec) == 0:
            print("ERROR")
        elif val in ops:
            print(val, ":", ops[val](vec))
