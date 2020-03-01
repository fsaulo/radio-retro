import numpy as np
import sounddevice as sd
import sys
import fsk
import time
import microphone

class Transmitter:
    def __init__(self):
        self.BAUD = 50
        self.RATE = 44100
        self.CARRIER = 1200
        self.TSIGNAL = None

    def set_baud(self, Bd=50):
        self.BAUD = Bd

    def set_frequency_sampling(self, fa):
        self.RATE = fa

    def set_carrier(self, carrier):
        self.CARRIER = carrier

    def config(self, Bd=None, fs=None, carrier=None):
        if Bd is not None:
            self.set_baud(Bd)
        if fs is not None:
            self.set_frequency_sampling(fs)
        if carrier is not None:
            self.set_carrier(carrier)

    def get_transmitting_signal(self):
        return self.SIGNAL

    def send_text_message(self, msg):
        bmsg = fsk.encode_ascii(msg)
        byte = ''
        bytearray = []
        fs = self.RATE
        carrier = self.CARRIER
        Bd = self.BAUD

        for k, bit in enumerate(bmsg, start=1):
            if k % 8 == 0:
                byte += bit
                bytearray.append(byte)
                byte = ''
            else:
                byte += bit

        sys.stdout.write('### BAUD {} CARRIER {}Hz ###\n'.format(str(Bd), str(carrier)))
        sys.stdout.flush()

        for byte in bytearray:
            s = fsk.generate_tones(byte, fs, Bd, carrier)
            tone = s * (2**15 - 1) / np.max(np.abs(s))
            tone = tone.astype(np.int16)
            self.SIGNAL = tone
            sd.play(tone, fs)
            status = sd.wait()

    def send_generic_message(self, msg):
        fs = self.RATE
        carrier = self.CARRIER
        Bd = self.BAUD
        bmsg = '11010001' + fsk.encode_ascii(msg)
        print(bmsg)
        sys.stdout.write('### BAUD {} CARRIER {}Hz ###\n'.format(str(Bd), str(carrier)))
        sys.stdout.flush()

        s = fsk.generate_tones(bmsg, fs, Bd, carrier)
        tone = s * (2**15 - 1) / np.max(np.abs(s))
        tone = tone.astype(np.int16)
        self.SIGNAL = tone
        sd.play(tone, fs)
        status = sd.wait()

class Receiver():
    def __init__(self):
        self.BAUD = 50
        self.RATE = 44100
        self.CARRIER = 1200
        self.FILTER_SIZE = 300
        self.BANDWIDTH = 1000
        self.THRESHOLD = 6
        self.MESSAGE = None

    def set_baud(self, Bd=50):
        self.BAUD = Bd

    def set_frequency_sampling(self, fa):
        self.RATE = fa

    def set_carrier(self, carrier):
        self.CARRIER = carrier

    def set_bandwidth(self, bandwidth):
        self.BANDWIDTH = bandwidth

    def set_filter_size(self, N):
        self.FILTER_SIZE = N

    def set_threshold(self, th):
        self.THRESHOLD = th

    def tune(self, Bd, fa=None, bandwidth=None, threshold=None, N=None):
        self.set_baud(Bd)
        if fa is not None:
            self.set_frequency_sampling(fa)
        if bandwidth is not None:
            self.set_bandwidth(bandwidth)
        if threshold is not None:
            self.set_threshold(threshold)
        if N is not None:
            self.set_filter_size(N)

    def listen(self, device='mic', nparray=None, file=None):
        import matplotlib.pyplot as plt
        Bd=self.BAUD
        fs=self.RATE
        carrier=self.CARRIER
        threshold=self.THRESHOLD
        bandwidth=self.BANDWIDTH
        N=self.FILTER_SIZE

        if nparray or file is None:
            mic = microphone.Microphone()
            chunk = round(fs/Bd)*8
            # data = np.array(mic.get_mic_data())/2**15
            # C, encoded_msg = fsk.demodulate(data, fs, Bd, carrier, threshold, bandwidth, N)
            # plt.plot(C)
            # plt.show()
            # self.MESSAGE = fsk.decode_ascii(encoded_msg)
            # print(self.MESSAGE, flush=True, end='')
            try:
                while True:
                    data = np.array(mic.get_mic_data(chunk=chunk))/2**15
                    C, encoded_msg = fsk.demodulate(data, fs, Bd, carrier, threshold, bandwidth, N)
                    print(f'Tentando sincronizar... {encoded_msg}', end='\r', flush=True)
                    if encoded_msg == '11010001':
                        break
                while True:
                    data = np.array(mic.get_mic_data(chunk=chunk))/2**15
                    C, encoded_msg = fsk.demodulate(data, fs, Bd, carrier, threshold, bandwidth, N)
                    byte = fsk.decode_ascii(encoded_msg)
                    if encoded_msg == '§':
                        break
                    else:
                        print(byte, flush=True, end='')
            except KeyboardInterrupt:
                print('Fim da transmissão')

        if nparray is not None:
            C, encoded_msg = fsk.demodulate(nparray, fs, Bd, carrier, threshold, bandwidth, N)
            self.MESSAGE = fsk.decode_ascii(encoded_msg)
            print(self.MESSAGE, flush=True, end='')

if __name__ == '__main__':
    # modem = Transmitter()
    # modem.config(Bd=500)
    # modem.send_generic_message('Enviando uma mensagem muito mais longa mas lentamente§')
    # s = modem.get_transmitting_signal()
    # from scipy.io import wavfile
    # wavfile.write('../../resources/audios/encoded_msgbd500ascii.wav', 44100, s)
    #
    receiver = Receiver()
    receiver.tune(500)
    receiver.listen()
