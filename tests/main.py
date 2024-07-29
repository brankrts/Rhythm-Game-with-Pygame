import numpy as np
import pydub
from scipy.fft import fft
import matplotlib.pyplot as plt

def load_mp3(mp3_path):
    audio = pydub.AudioSegment.from_mp3(mp3_path)
    audio = audio.set_channels(1)
    audio = audio.set_frame_rate(44100)  
    audio_data = np.array(audio.get_array_of_samples())
    return audio.frame_rate, audio_data

def perform_fft_per_second(audio_data, sampling_rate, window_size=1024):
    fft_window = np.hanning(window_size)
    
    segment_length = sampling_rate  
    num_segments = len(audio_data) // segment_length
    
    freqs = np.fft.fftfreq(window_size, 1 / sampling_rate)[:window_size // 2]
    
    time_stamps = []
    fft_results = []
    
    for i in range(num_segments):
        start_idx = i * segment_length
        end_idx = start_idx + window_size
        if end_idx > len(audio_data):
            break
        
        segment = audio_data[start_idx:end_idx] * fft_window
        fft_result = np.abs(fft(segment))[:window_size // 2]
        
        time_stamps.append(i)
        fft_results.append(fft_result)
    
    return time_stamps, freqs, fft_results

def plot_fft_per_second(time_stamps, freqs, fft_results):
    for i, fft_result in enumerate(fft_results):
        plt.figure(figsize=(14, 7))
        plt.plot(freqs, fft_result)
        plt.xlabel('Frekans (Hz)')
        plt.ylabel('Genlik')
        plt.title(f'FFT Analizi - Saniye {time_stamps[i]}')
        plt.grid(True)
        plt.show()

mp3_path = '../musics/beat_dun.mp3'


sampling_rate, audio_data = load_mp3(mp3_path)


time_stamps, freqs, fft_results = perform_fft_per_second(audio_data, sampling_rate)

plot_fft_per_second(time_stamps, freqs, fft_results)
