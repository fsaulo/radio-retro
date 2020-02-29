import sys
sys.path.append('../modules/')

import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import time
import fsk

from sinais import specgram, bandpass

fc = 44100
Bd = 50
carrier = 1200
N = 300
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


s = fsk.generate_tones(bmsg, fc, Bd, carrier)
white_noise = np.random.normal(0, 0.5, size=len(s))*0
s = s + white_noise

C, encoded_msg = fsk.demodulate(s, fc, Bd, carrier, 5, bandwidth, N)
# encoded_msg = encoded_msg[::-1]
string = ''.join([chr(int(encoded_msg[i:i+8],2)) for i in range(0,len(encoded_msg),8)])

print('Mensagem original:     {}\n'.format(msg))
print('Mensagem decodificada: {}\n'.format(string))

print('Tamanho do sinal transmitido: {}Mb'.format(str(s.nbytes/1e6)))
