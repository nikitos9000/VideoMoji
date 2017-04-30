import numpy as np
import pyaudio

CHANNELS = 1
RATE = 44100
FRAMES_PER_BUFFER = 16 * 1024
FORMAT = pyaudio.paInt16


def _init_capture():
    audio = pyaudio.PyAudio()
    return audio, audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,
                             frames_per_buffer=FRAMES_PER_BUFFER)

audio, stream = _init_capture()


def capture(duration):
    samples = []
    for _ in xrange(0, int(RATE / FRAMES_PER_BUFFER * duration)):
        data = stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)
        samples.append(np.fromstring(data, dtype=np.int16))

    return dict(samples=samples, sample_rate=RATE, channels=CHANNELS, sample_size=audio.get_sample_size(FORMAT))
