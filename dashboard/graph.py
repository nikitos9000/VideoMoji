import time
import plotly
import matplotlib.pyplot as plt
from collections import defaultdict

plt.figure(figsize=(14, 7))
plt.ion()
plt.show()

history = defaultdict(list)


def plot(points):
    timestamp = time.time()

    for idx, (key, value) in enumerate(points.iteritems()):
        history[key].append(value)
        avg = history[key][-5:]
        avg_value = sum(avg) / len(avg)
        plt.subplot(2, 3, idx + 1)
        plt.title(key)
        plt.plot(timestamp, avg_value, 'ro')
        plt.grid(True)
        plt.axis([timestamp - 30, timestamp, 0, 1.0])

    plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25, wspace=0.35)

    plt.draw()
    plt.pause(0.001)
