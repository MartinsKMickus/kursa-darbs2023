import sys
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
cut_off = 12000

# Set parameters
play_frequency = 17000.0  # Frequency of the sine wave in Hz
# NETIEK IZMANTOTS
rec_duration = 3
wait_rec = 1
# Skaņas signālam ar 2 sekundēm pietiks, lai izplatītos vienmērīgi telpā.
play_duration = 2.0  # Duration of the audio signal in seconds

output_filename = "sine_wave.wav"  # Name of the output audio file

current_number = 0

# Generate signal
def gen_signal(frequency = play_frequency, duration = play_duration):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    signal = np.sin(2 * np.pi * frequency * t)
    # Beigās signālam vajag klusumu 0.4s. Tas dod ~190ms atbalsi
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
    # Atbalsij esot aptuveni 190ms. Lai neiekļautu oriģinālo signālu var ņemt 180ms
    signal = signal[int(-sample_rate*0.180):]
    # current_peak = np.max(np.abs(signal))
    # signal = (signal / current_peak)
    # Saglabā signālu, jo problēmas ja nesaglabā
    wavfile.write(output_filename, sample_rate, signal)
    # Noņemt zemās frekvences
    sample_rate1, data = scipy.io.wavfile.read(output_filename)
    filtered = highpass(data, cut_off, sample_rate1)
    # Normalizē
    current_peak = np.max(np.abs(filtered))
    filtered = (filtered / current_peak)
    wavfile.write(output_filename, sample_rate1, filtered)


def load_file(filename):
    return wavfile.read(filename)

def play_file(filename):
    sr, audio_data = load_file(filename=filename) 
    play_signal(signal=audio_data, sr=sr)

# For threadin. Recoder
def threading_recorder():
    print("Starting recording")
    save_audio(rec_signal(rec_duration), name=f"recorded_audio{current_number}.wav")

def highpass(data: np.ndarray, cutoff: float = 12000, sample_rate: float = sample_rate, poles: int = 5):
    sos = scipy.signal.butter(poles, cutoff, 'highpass', fs=sample_rate, output='sos')
    filtered_data = scipy.signal.sosfiltfilt(sos, data)
    return filtered_data

print(sys.argv[1])
sleep(4)
for i in range(1, 9):
    sleep(1) # Lai atskaņošanas un ieraksta ierīces iegūst miera stāvokli
    print(f"Recording: {i}")
    current_number = i
    recording = playrec_signal()
    save_audio(recording, name=f"recorded_{sys.argv[1]}{current_number}.wav")
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