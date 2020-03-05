import numpy as np
import struct
import pyaudio

class Microphone(object):
    def __init__(self):
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 2205*8

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            output=False,
            frames_per_buffer=self.CHUNK,
        )

        for x in range(0, self.p.get_device_count()):
            info = self.p.get_device_info_by_index(x)
            if info["name"] == "pulse":
                chosen_device_index = info["index"]

    def get_mic_data(self, chunk=2205*8):
        data = self.stream.read(chunk)
        data_int16 = struct.unpack(str(chunk) + 'h', data)
        return data_int16

    def close():
        self.stream.close()
