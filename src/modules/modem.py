import sys
import numpy as np
import fsk
import sounddevice as sd

class Transmitter:
    def __init__(self):
        self.BAUD = 50
        self.RATE = 44100
        self.CARRIER = 1200

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
            sd.play(tone, fs)
            status = sd.wait()

class Receiver:
    def __init__(self):
        self.BAUD = 50
        self.RATE = 44100
        self.CARRIER = 1200
        self.FILTER_SIZE = 300
        self.BANDWIDTH = 1000

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

    def tune(self, Bd, fa=None, bandwidth=None, N=None):
        self.set_baud(Bd)
        if fa is not None:
            self.set_frequency_sampling(fa)
        if bandwidth is not None:
            self.set_bandwidth(bandwidth)
        if N is not None:
            self.set_filter_size(N)

    def listen(self, Bd=self.BAUD, fa=self.RATE, device=None, nparray=None, file=None):
        if device is not None:
            pass
        elif nparray is not None:
            C, encoded_msg = fsk.demodulate(s, fc, Bd, carrier, 20, bandwidth, N)

    def decoded_message(self):
        pass

if __name__ == '__main__':
    modem = Transmitter()
    modem.send_text_message('Hello world!')
