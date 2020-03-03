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

    def send_generic_message(self, msg, debug=False):
        fs = self.RATE
        carrier = self.CARRIER
        Bd = self.BAUD
        bmsg = '11010001' + fsk.encode_ascii(msg)
        if debug: print(bmsg)
        sys.stdout.write('### BAUD {} CARRIER {}Hz ###\n'.format(str(Bd), str(carrier)))
        sys.stdout.flush()

        s = fsk.generate_tones(bmsg, fs, Bd, carrier)
        s = fsk.sanduiche_encoding(s, Bd)
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
        self.FILTER_SIZE = 500
        self.BANDWIDTH = 1000
        self.THRESHOLD = 6
        self.MESSAGE = None
        self.ENCODED_SIGNAL = None
        self.vetor = None

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

    def tune(self, Bd, fa=None, carrier=None, bandwidth=None, threshold=None, N=None):
        self.set_baud(Bd)
        if fa is not None:
            self.set_frequency_sampling(fa)
        if carrier is not None:
            self.set_carrier(carrier)
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
            chunk = round(fs/Bd)
            try:
                S = np.array([])
                while True:
                    print('Procurando sinal... ', end='\r', flush=True)
                    data = np.array(mic.get_mic_data(chunk=chunk))
                    tone = data * (2**15 - 1) / np.max(np.abs(data))
                    tone = tone.astype(np.int16)
                    if fsk.sintonizado(tone, fs, 3400, 20, 200, 80):
                        print(f'### BAUD {Bd} @ CARRIER {carrier} Hz')
                        break
                while True:
                    print('Recebendo mensagem... ', end='\r', flush=True)
                    data = np.array(mic.get_mic_data(chunk=chunk))
                    tone = data * (2**15 - 1) / np.max(np.abs(data))
                    tone = tone.astype(np.int16)
                    if fsk.sintonizado(tone, fs, 3800, 20, 500, 80):
                        C, encoded_msg = fsk.demodulate(S, fs, Bd, carrier, threshold, bandwidth, N)
                        msg = fsk.decode_sanduiche(encoded_msg)
                        msg = fsk.decode_ascii(msg)
                        self.MESSAGE = msg
                        print(f"Mensagem recebida: {msg}")
                        print("Fim da transmissão")
                        break
                    else:
                        S = np.append(S, tone)
            except KeyboardInterrupt:
                print('Transmissão encerrada')
            self.ENCODED_SIGNAL = S
        if nparray is not None:
            C, encoded_msg = fsk.demodulate(nparray, fs, Bd, carrier, threshold, bandwidth, N)
            self.MESSAGE = fsk.decode_ascii(encoded_msg)
            self.ENCODED_SIGNAL = C
            print(self.MESSAGE, flush=True, end='')

    def get_received_encoded_signal(self):
        return self.ENCODED_SIGNAL

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    modem = Transmitter()
    modem.config(Bd=100, carrier=1200)
    modem.send_generic_message('In order to use this binary to ascii text converter tool, type a binary value, i.e. 011110010110111101110101, to get "you" and push the convert button. You can convert up to 1024 binary characters to ascii text. Decode binary to ascii text readable format.')
    s = modem.get_transmitting_signal()
    from scipy.io import wavfile
    wavfile.write('../../resources/audios/encoded_msgbd100ascii.wav', 44100, s)

    # receiver = Receiver()
    # receiver.tune(Bd=100, threshold=6)
    # receiver.listen()
