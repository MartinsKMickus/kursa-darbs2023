import threading
from time import sleep
from matplotlib import pyplot as plt
import numpy as np
from scipy.io import wavfile
import sounddevice as sd
import scipy.signal
import scipy.io.wavfile as wav
from scipy import signal

sample_rate = 44100  # Sample rate (samples per second)

# Set parameters
play_frequency = 17000.0  # Frequency of the sine wave in Hz
rec_duration = 3
wait_rec = 1
play_duration = 3.0  # Duration of the audio signal in seconds

output_filename = "sine_wave.wav"  # Name of the output audio file

current_number = 0

# Generate signal
def gen_signal(frequency = play_frequency, duration = play_duration):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    signal = np.sin(2 * np.pi * frequency * t)
    signal = np.concatenate([signal,np.zeros(int(sample_rate*0.4))])
    # plt.plot(signal)
    # plt.show()
    return signal

generated_signal = gen_signal(frequency=play_frequency, duration=play_duration)

# Play signal
def play_signal(signal = generated_signal, sr = sample_rate):
    sd.play(signal, sr)
    sd.wait()

def rec_signal(duration):
    signal = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=1)
    sd.wait()
    return signal

# Play and record at the same time
def playrec_signal(signal = generated_signal):
    signal = sd.playrec(signal, sample_rate, channels=1)
    sd.wait()
    return signal

def save_audio(signal, name="recorded_audio.wav"):
    output_filename = name
    signal = signal[int(-sample_rate*0.4):]
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

def apply_high_pass_filter(input_file, output_file, cutoff_frequency, sampling_rate):
    sos = signal.butter(4, cutoff_frequency / (sampling_rate/2), 'high', output='sos', analog=True)
    # w, h = signal.freqs(b, a)
    data = np.asarray(load_file(filename=input_file))
    filtered = signal.sosfilt(sos, data)
    save_audio(signal=filtered, name=output_file)


sleep(4)
for i in range(1, 5):
    sleep(1) # Lai atskaņošanas un ieraksta ierīces iegūst miera stāvokli
    print(f"Recording: {i}")
    current_number = i
    recording = playrec_signal()
    save_audio(recording, name=f"recorded_audio{current_number}.wav")
    # sr, recorded = load_file(filename="recorded_audio.wav")


# for i in range(1, 10):
#     current_number = i
#     playback_thread = threading.Thread(target=play_signal)
#     playback_thread.start()
#     sleep(wait_rec)
#     save_audio(rec_signal(rec_duration), name=f"recorded_audio{current_number}.wav")
#     sleep(1)

# for i in range(1, 10):
#     apply_high_pass_filter(input_file=f"recorded_audio{i}.wav", output_file=f"recorded_audio{i}.wav", cutoff_frequency=11000, sampling_rate=sample_rate)
# playback_thread.join()
# play_signal(signal=recorded, sr=sr)

# # original = gen_signal(frequency=play_frequency, duration=play_duration)
# # recorded = playrec_signal(signal=original)
# # play_signal(recorded)
# plt.plot(gen_signal(frequency=play_frequency, duration=play_duration))
# plt.plot(recorded)
# plt.show()
# sleep(0.1)