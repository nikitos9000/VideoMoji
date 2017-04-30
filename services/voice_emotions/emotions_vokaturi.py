import sys
import numpy as np

from Vokaturi import Vokaturi

Vokaturi_platform = dict(linux='linux64', linux2='linux64', darwin='mac')[sys.platform]
Vokaturi.load("data/voice_emotions/Vokaturi/Vokaturi_%s.so" % Vokaturi_platform)


def extract_emotions(samples, sample_rate):
    if not samples:
        return {}

    samples = np.concatenate(samples)
    buffer_length = len(samples)
    print "   %d samples, %d channels" % (buffer_length, samples.ndim)
    c_buffer = Vokaturi.SampleArrayC(buffer_length)
    c_buffer[:] = samples[:] / 32768.0

    voice = Vokaturi.Voice(sample_rate, buffer_length)
    voice.fill(buffer_length, c_buffer)
    quality = Vokaturi.Quality()
    emotion_probabilities = Vokaturi.EmotionProbabilities()
    voice.extract(quality, emotion_probabilities)
    voice.destroy()

    if not quality.valid:
        return {}

    emotions = dict(neutral=emotion_probabilities.neutrality, happy=emotion_probabilities.happiness,
                    sad=emotion_probabilities.sadness, angry=emotion_probabilities.anger,
                    fear=emotion_probabilities.fear)

    return dict(emotions=emotions)
