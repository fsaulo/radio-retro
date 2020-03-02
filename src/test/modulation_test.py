import sys
sys.path.append('../modules/')

import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import time
import fsk
import microphone

from sinais import specgram, bandpass

fc = 44100
Bd = 1200
carrier = 1200
N = 500
bandwidth = carrier/2 + carrier*0.1
print('### BAUD {} CARRIER {}Hz ###'.format(str(Bd), str(carrier)))

msg = 'Hello world'

bmsg = fsk.encode_ascii(msg)
X = fsk.binary_signal(bmsg, fc, Bd)
print('Bitstream da mensagem original \n{}\n'.format(bmsg))

# byte = ''
# bytearray = []
#
# for k, bit in enumerate(bmsg, start=1):
#     if k % 8 == 0:
#         byte += bit
#         bytearray.append(byte)
#         byte = ''
#     else:
#         byte += bit
#
# for byte in bytearray:
#     s = fsk.generate_tones(byte, fc, Bd, carrier)
#     tone = s * (2**15 - 1) / np.max(np.abs(s))
#     tone = tone.astype(np.int16)
#     sd.play(tone, fc)
#     status = sd.wait()
#     C, encoded_msg = fsk.demodulate(s, fc, Bd, carrier, 20, bandwidth, N)
#     print(fsk.decode_ascii(encoded_msg), end='', flush=True)


# s = fsk.generate_tones(bmsg, fc, Bd, carrier)
# white_noise = np.random.normal(0, 0.5, size=len(s))*0
# s = s + white_noise
mic = microphone.Microphone()
s = np.array(mic.get_mic_data())
C, encoded_msg = fsk.demodulate(s, fc, Bd, carrier, 500, bandwidth, N)

# self.MESSAGE = fsk.decode_ascii(encoded_msg)
# print(self.MESSAGE, flush=True, end='')

# C, encoded_msg = fsk.demodulate(s, fc, Bd, carrier, 5, bandwidth, N)
string = ''.join([chr(int(encoded_msg[i:i+8],2)) for i in range(0,len(encoded_msg),8)])

# print('Mensagem original:     {}\n'.format(msg))
print('Mensagem decodificada: {}\n'.format(string))

print('Tamanho do sinal transmitido: {}Mb'.format(str(s.nbytes/1e6)))
plt.plot(C)
plt.show()
