import numpy as np

from Vokaturi import Vokaturi

Vokaturi.load("data/voice_emotions/Vokaturi/Vokaturi_mac.so")


def extract_emotions(samples, sample_rate):
    if not samples:
        return {}

    samples = np.concatenate(samples)
    print "Allocating Vokaturi sample array..."
    buffer_length = len(samples)
    print "   %d samples, %d channels" % (buffer_length, samples.ndim)
    c_buffer = Vokaturi.SampleArrayC(buffer_length)
    c_buffer[:] = samples[:] / 32768.0

    print "Creating VokaturiVoice..."
    voice = Vokaturi.Voice(sample_rate, buffer_length)

    print "Filling VokaturiVoice with samples..."
    voice.fill(buffer_length, c_buffer)

    print "Extracting emotions from VokaturiVoice..."
    quality = Vokaturi.Quality()
    emotion_probabilities = Vokaturi.EmotionProbabilities()
    voice.extract(quality, emotion_probabilities)
    voice.destroy()

    if not quality.valid:
        return {}

    return dict(neutral=emotion_probabilities.neutrality, happy=emotion_probabilities.happiness,
                sad=emotion_probabilities.sadness, angry=emotion_probabilities.anger,
                fear=emotion_probabilities.fear)
