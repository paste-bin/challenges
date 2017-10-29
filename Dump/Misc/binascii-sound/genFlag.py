from __future__ import division #Avoid division problems in Python 2
import wave
import random
import math
import pyaudio
import sys

PyAudio = pyaudio.PyAudio
RATE = 16000
#WAVE = 1000
CRUELTY = True
#CRUELTY = False

C4 = 261.626
G4 = 391.995
CS4 = 277.183

DS4 = 311.127
E4 = 329.629

def get_zero(cruel):
    if cruel:
        # generate a random number between x and y
        return random.randint(310,320)
    else:
        return C4


def get_one(cruel):
    if cruel:
        # generate a randum number between x and y
        return random.randint(425,435)
    else:
        return G4


binflag = "011001100110110001100001011001110111101101100100001100000101111101111001001100000111010101110010010111110110010100110100011100100111001101011111010010000111010101010010011101000101111101111001001100110111010001111101"

def gen_wave(WAVE):
    data = ''.join([chr(int(math.sin(x/((RATE/WAVE)/math.pi))*127+128)) for x in xrange(RATE)])
    return data

def gen_stream(binstream):
    data = []
    for char in binstream:
        if char == "0":
            data.append(gen_wave(get_zero(CRUELTY)))
        elif char == "1":
            data.append(gen_wave(get_one(CRUELTY)))
    return data

def silence():
    return chr(128)*int(RATE/4)

def play_locally(data):
    # to hear it locally:
    stream = p.open(format =
                    p.get_format_from_width(1),
                    channels = 1,
                    rate = RATE,
                    output = True)
    for DISCARD in xrange(5):
        for thing in data:
            stream.write(silence())
            stream.write(thing)

    stream.stop_stream()
    stream.close()
    p.terminate()

def generate_file(data):
    output = []

    for asdf in xrange(5):
        for thing in data:
            output.append(silence())
            output.append(thing)

    waveFile = wave.open("flag.wav", "wb")
    waveFile.setnchannels(1)
    waveFile.setsampwidth(p.get_sample_size(p.get_format_from_width(1)))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(output))
    waveFile.close()

p = PyAudio()
data = gen_stream(binflag)

#play_locally(data)
generate_file(data)


