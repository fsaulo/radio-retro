import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 2205 * 8
DEVICE_INDEX = -1

mic = pyaudio.PyAudio()

stream = mic.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
    )

# data = stream.read(CHUNK)
# print(data)

# for x in range(0, mic.get_device_count()):
#     info = mic.get_device_info_by_index(x)
#     if info["name"] == "pulse":
#         chosen_device_index = info["index"]
#         # print("Chosen index: {}".format(chosen_device_index))


plt.ion()
fig, ax = plt.subplots()

x = np.arange(0, CHUNK)
data = stream.read(CHUNK)
data_int16 = np.array(struct.unpack(str(CHUNK) + 'h', data))/2**15
line, = ax.plot(x, data_int16)
ax.set_ylim([1.5,-1.5])

try:
    while True:
        data = np.array(struct.unpack(str(CHUNK) + 'h', stream.read(CHUNK)))/2**15
        line.set_ydata(data)
        fig.canvas.draw()
        fig.canvas.flush_events()
except KeyboardInterrupt:
    pass
