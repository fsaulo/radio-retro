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

    def config(self, Bd=None, fs=None, carrier=None):
        if Bd is not None:
            self.BAUD = Bd
        if fs is not None:
            self.RATE = fs
        if carrier is not None:
            self.CARRIER = carrier

    def get_transmitting_signal(self):
        return self.SIGNAL

    def send_text_message(self, msg):
        bmsg = '11010001' + fsk.encode_ascii(msg)
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

        sys.stdout.write('### BAUD {} @ CARRIER {}Hz ###\n'.format(str(Bd), str(carrier)))
        sys.stdout.flush()
        s = fsk.set_frequency_header(np.zeros(0),Bd)
        sd.play(s, fs)
        status = sd.wait()

        for byte in bytearray:
            s = fsk.generate_tones(byte, fs, Bd, carrier)
            tone = s * (2**15 - 1) / np.max(np.abs(s))
            tone = tone.astype(np.int16)
            self.SIGNAL = tone
            sd.play(tone, fs)
            status = sd.wait()

        s = fsk.set_frequency_trailer(np.zeros(0),Bd)
        sd.play(s, fs)
        status = sd.wait()

    def send_generic_message(self, msg, debug=False):
        fs = self.RATE
        carrier = self.CARRIER
        Bd = self.BAUD
        bmsg = '11010001' + fsk.encode_ascii(msg)
        if debug: print(bmsg)
        sys.stdout.write(f'### BAUD {Bd} @ CARRIER {carrier}Hz ###\n')
        sys.stdout.flush()

        s = fsk.generate_tones(bmsg, fs, Bd, carrier)
        s = fsk.sanduiche_encoding(s, Bd)
        tone = s * (2**15 - 1) / np.max(np.abs(s))
        tone = tone.astype(np.int16)

        self.SIGNAL = tone
        sd.play(tone, fs)
        status = sd.wait()

    def message_to_wav(self, msg):
        fs = self.RATE
        carrier = self.CARRIER
        Bd = self.BAUD
        bmsg = '11010001' + fsk.encode_ascii(msg)
        sys.stdout.write(f'### BAUD {Bd} @ CARRIER {carrier}Hz ###\n')
        sys.stdout.flush()

        s = fsk.generate_tones(bmsg, fs, Bd, carrier)
        s = fsk.sanduiche_encoding(s, Bd)
        tone = s * (2**15 - 1) / np.max(np.abs(s))
        tone = tone.astype(np.int16)
        self.SIGNAL = tone

class Receiver():
    def __init__(self):
        self.BAUD = 50
        self.RATE = 44100
        self.CARRIER = 1200
        self.FILTER_SIZE = 500
        self.BANDWIDTH = 10
        self.THRESHOLD = 8
        self.MESSAGE = None
        self.ENCODED_SIGNAL = None
        self.vetor = None
        self.SINTONIA = 150

    def tune(self, Bd=None, fa=None, carrier=None, bandwidth=None, threshold=None, N=None, sintonia=None):
        if Bd is not None:
            self.BAUD = Bd
        if fa is not None:
            self.RATE = fa
        if carrier is not None:
            self.CARRIER = carrier
        if bandwidth is not None:
            self.BANDWIDTH = bandwidth
        if threshold is not None:
            self.THRESHOLD = threshold
        if N is not None:
            self.FILTER_SIZE = N
        if sintonia is not None:
            self.SINTONIA = sintonia

    def listen(self, device='mic', nparray=None, file=None):
        import matplotlib.pyplot as plt
        Bd=self.BAUD
        fs=self.RATE
        carrier=self.CARRIER
        threshold=self.THRESHOLD
        bandwidth=self.BANDWIDTH
        N=self.FILTER_SIZE
        sintonia=self.SINTONIA

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
                    if fsk.sintonizado(tone, fs, 3400, 20, N, sintonia):
                        print(f'### BAUD {Bd} @ CARRIER {carrier} Hz')
                        break
                while True:
                    print('Recebendo mensagem... ', end='\r', flush=True)
                    data = np.array(mic.get_mic_data(chunk=chunk))
                    tone = data * (2**15 - 1) / np.max(np.abs(data))
                    tone = tone.astype(np.int16)
                    if fsk.sintonizado(tone, fs, 3800, 20, N, sintonia):
                        S = np.append(S, tone)
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
                mic.close()
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
    modem.send_generic_message('Hello world')
    s = modem.get_transmitting_signal()
    from scipy.io import wavfile
    wavfile.write('../../resources/audios/encoded_msgbd100ascii.wav', 44100, s)

    # receiver = Receiver()
    # receiver.tune(Bd=100, threshold=5)
    # receiver.listen()
