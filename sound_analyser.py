import numpy as np
import pydub
from scipy.fft import fft

class SoundAnalyzer:
    def __init__(self, mp3_path, threshold, sampling_rate=44100, window_size=1024, step_size_ms=10):
        self.mp3_path = mp3_path
        self.threshold = threshold
        self.sampling_rate = sampling_rate
        self.window_size = window_size
        self.step_size_ms = step_size_ms
        self.audio_data = None
        self.time_stamps = None
        self.fft_results = None
        
        self.load_mp3()
        self.perform_fft_with_millisecond_resolution()
    
    def load_mp3(self):
        audio = pydub.AudioSegment.from_mp3(self.mp3_path)
        audio = audio.set_channels(1)
        audio = audio.set_frame_rate(self.sampling_rate)
        self.audio_data = np.array(audio.get_array_of_samples())
    
    def perform_fft_with_millisecond_resolution(self):
        fft_window = np.hanning(self.window_size)
        step_length = int(self.sampling_rate * (self.step_size_ms / 1000.0))
        
        num_segments = (len(self.audio_data) - self.window_size) // step_length
        
        self.time_stamps = []
        self.fft_results = []
        
        for i in range(num_segments):
            start_idx = i * step_length
            end_idx = start_idx + self.window_size
            if end_idx > len(self.audio_data):
                break
            
            segment = self.audio_data[start_idx:end_idx] * fft_window
            fft_result = np.abs(fft(segment))[:self.window_size // 2]
            
            self.time_stamps.append(start_idx / self.sampling_rate * 1000)  
            self.fft_results.append(fft_result)
    
    def find_peaks(self):
        print(self.threshold , self.step_size_ms)

        peak_times = []
        
        for i, fft_result in enumerate(self.fft_results):
            if np.max(fft_result) > self.threshold:
                peak_times.append(self.time_stamps[i])
        
        return peak_times

