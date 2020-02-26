import numpy as np

class Modulation:
    def __init__(self):
        pass

    def binary_signal(self, bit_stream, fs, Bd):
        k = len(bit_stream)
        n = round(fs/Bd) * k
        samples = round(n/k)
        X = np.zeros(n)
        for i in range(0, k):
            X[i*samples:(i+1)*samples] = np.ones(samples) * int(bit_stream[i])
        return X

    def encode_ascii(self, msg):
        stream = ''.join(f'{ord(i):08b}' for i in msg)
        stream = stream[::-1]
        return stream

    def bfsk(self, bit_stream, fs=44100, Bd=1200):
        bin_wave = self.binary_signal(bit_stream, fs, Bd)
        t = np.linspace(0, len(bit_stream)/Bd, len(bin_wave))
        fc = (bin_wave + 1) * Bd
        return np.cos(2*np.pi*fc*t)


if __name__ == '__main__':
    module = Modulation()
    Bd = 1200
    fs = 44100
    s = module.bfsk(module.encode_ascii('hello'), fs, Bd)
