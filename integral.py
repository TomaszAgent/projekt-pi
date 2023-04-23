import numpy as np


def integral(a, b, f):
    try:
        a, b = int(a), int(b)
        dx = ((b - a) / 10000)
        X = np.arange(a, b, dx).tolist()
        Y = []
        for element in X:
            Y.append(eval(f, {}, {'x': element}))
        s = dx * np.sum(Y)
        return s
    except:
        return 'ERROR OCCURRED\r\n\r\n'
