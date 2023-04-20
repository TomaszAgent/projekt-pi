import numpy as np


def integral(a, b, f):
    dx = ((b-a) / 1000)
    X = np.arange(a, b, dx).tolist()
    try:
        Y = []
        for element in X:
            Y.append(eval(f, {}, {'x': element}))
        s = dx * np.sum(Y)
        return s
    except:
        return 'ERROR OCCURRED\r\n\r\n'
