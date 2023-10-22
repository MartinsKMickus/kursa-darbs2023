import threading
from time import sleep
from matplotlib import pyplot as plt
import numpy as np
from scipy.io import wavfile
import sounddevice as sd

sample_rate = 44100  # Sample rate (samples per second)

# Set parameters
play_frequency = 19000.0  # Frequency of the sine wave in Hz
rec_duration = 1.0
wait_rec = 0
play_duration = 0.5  # Duration of the audio signal in seconds

output_filename = "sine_wave.wav"  # Name of the output audio file

current_number = 0
# Generate signal
def gen_signal(frequency, duration):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    signal = np.sin(2 * np.pi * frequency * t)
    # plt.plot(signal)
    # plt.show()
    return signal

# Play signal
def play_signal(signal, sr = sample_rate):
    sd.play(signal, sr)
    sd.wait()

def rec_signal(duration):
    signal = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=1)
    sd.wait()
    return signal

# Play and record at the same time
def playrec_signal(signal):
    signal = sd.playrec(signal, sample_rate, channels=2)
    sd.wait()
    return signal

def save_audio(signal, name="recorded_audio.wav"):
    output_filename = name
    wavfile.write(output_filename, sample_rate, signal)

def load_file(filename):
    return wavfile.read(filename)

def play_file(filename):
    sr, audio_data = load_file(filename=filename) 
    play_signal(signal=audio_data, sr=sr)

# For threadin. Recoder
def threading_recorder():
    print("Starting recording")
    save_audio(rec_signal(rec_duration), name=f"recorded_audio{current_number}.wav")

for i in range(1, 10):
    current_number = i
    recording_thread = threading.Thread(target=threading_recorder)
    recording_thread.start()
    sleep(wait_rec)
    play_signal(gen_signal(frequency=play_frequency, duration=play_duration))
    recording_thread.join()
    sleep(1)
    # sr, recorded = load_file(filename="recorded_audio.wav")

# play_signal(signal=recorded, sr=sr)

# # original = gen_signal(frequency=play_frequency, duration=play_duration)
# # recorded = playrec_signal(signal=original)
# # play_signal(recorded)
# plt.plot(gen_signal(frequency=play_frequency, duration=play_duration))
# plt.plot(recorded)
# plt.show()
# sleep(0.1)