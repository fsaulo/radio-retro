import sinais as sn
import numpy as np
import matplotlib.pyplot as plt
def binary_signal(bit_stream, fs, Bd):
    k = len(bit_stream)
    n = round(fs/Bd) * k
    samples = round(n/k)
    X = np.zeros(n)
    for i in range(0, k):
        X[i*samples:(i+1)*samples] = np.ones(samples) * int(bit_stream[i])
    return X
def set_frequency_header(sig):
    fx = 3400
    fa = 44100
    t = np.arange(0,0.2,1/fa)
    y = np.cos(np.pi*2*fx*t)
    d = np.zeros(len(sig)+len(y))
    d[0:len(y)] = y
    d[len(y):len(d)] = sig
    return d
def set_frequency_trailer(sig):
    fx = 3800
    fa = 44100
    t = np.arange(0,0.2,1/fa)
    y = np.cos(np.pi*2*fx*t)
    d = np.zeros(len(sig)+len(y))
    d[0:len(sig)] = sig
    d[len(sig):len(d)] = y
    return d

def encode_ascii(msg, reverse=False):
    stream = ''.join(f'{ord(i):08b}' for i in msg)
    return stream if not reverse else stream[::-1]

def decode_ascii(bit_stream):
    string = ''.join([chr(int(bit_stream[i:i+8],2)) for i in range(0,len(bit_stream),8)])
    return string

def generate_tones(bit_stream, fs=44100, Bd=1200, carrier=1200):
    bin_wave = binary_signal(bit_stream, fs, Bd)
    t = np.linspace(0, len(bit_stream)/Bd, len(bin_wave))
    fc = (bin_wave + 1) * carrier
    return np.cos(2*np.pi*fc*t)
def sintonizado(s, fa, carrier, bandwidth, N, threshold):
    x1 = sn.bandpass(s,fa,carrier, bandwidth, N)
    energia = sn.rms(x1**2)
    #print(energia)
    if energia > threshold:
        return True
    else:
        return False
def demodulate(s, fa, Bd, carrier, threshold=4, bandwidth=500, N=300):
    x0 = sn.bandpass(s, fa, carrier, bandwidth, N)
    x1 = sn.bandpass(s, fa, 2*carrier, bandwidth, N)
    m = 0
    C = np.zeros(len(x1))
    encoded_msg = ''
    samples_per_symbol = round(fa/Bd)
    for k in range(0, round(len(x1)/samples_per_symbol)):
        chunk = k*samples_per_symbol
        rms_0 = sn.rms(x1[chunk:chunk+samples_per_symbol]**2)
        rms_1 = sn.rms(x0[chunk:chunk+samples_per_symbol]**2)
        if rms_0 > threshold or rms_1 > threshold:
            if rms_1 > rms_0:
                C[chunk:chunk+samples_per_symbol] = np.ones(samples_per_symbol)
                encoded_msg += '0'
            else:
                C[chunk:chunk+samples_per_symbol] = np.ones(samples_per_symbol) * (-1)
                encoded_msg += '1'
        m += samples_per_symbol
    return C, encoded_msg

if __name__ == '__main__':
    # import matplotlib.pyplot as plt
    # Bd = 1200
    # fs = 44100
    # s = generate_tones(encode_ascii('hello'), fs, Bd, 1200)
    # plt.plot(s)
    # plt.show()
    #from scipy.io import wavfile
    #[fa, s] = wavfile.read('../../resources/audios/encoded_msg_bd1200ascii.wav')
    #C, encoded_msg = demodulate(s, fa, 1200, 1200, threshold=20, bandwidth=1000, N=300)
    #print(decode_ascii(encoded_msg[::-1]))
    t = np.linspace(0,0.05,44100)
    sig = np.cos(2*np.pi*200*t)

    s2 = set_frequency_trailer(set_frequency_header(sig))
    if sintonizado(s2, 44100, 3800, 200, 500,687.841606187618):
        print("sintonizado")

    else:
        print("não sintonizado")
