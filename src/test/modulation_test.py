import matplotlib.pyplot as plt
import numpy as np
import sounddevice
import sys

if __name__ == '__main__':
    sys.path.append('../modules/')
    import fsk
    module = fsk.Modulation()
    msg = module.encode_ascii('hello world')
    s = module.bfsk(msg, 44100, 1200)
    plt.plot(s)
    plt.show()
