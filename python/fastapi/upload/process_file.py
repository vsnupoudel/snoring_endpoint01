from scipy.io import wavfile
from scipy.signal import resample
import numpy as np

# Ensure sample rate
def ensure_sample_rate(original_sample_rate, waveform, desired_sample_rate=16000):
    if original_sample_rate != desired_sample_rate:
        desired_length = int(  len(waveform) *  (desired_sample_rate/original_sample_rate ) )
        waveform = resample(waveform, desired_length)
    return  waveform

# Read and normalize audio
def read_and_normalise(file):
    try:
        sample_rate, wav_data = wavfile.read(file)
        wav_data = wav_data.mean(axis=1)  # Convert to mono
        wav_data = ensure_sample_rate(sample_rate, wav_data)
        waveform = wav_data / wav_data.max()
        return waveform
    except Exception as e:
        raise RuntimeError(f"Error reading and normalizing audio: {str(e)}")

def split_generator(waveform, chunk_size=16000):
    """
    Splits the waveform into chunks of specified size. chunk_size*2
    """
    start_index = chunk_size
    end_index = len(waveform) - 1 
    while start_index+chunk_size < end_index:
        if waveform[start_index] > 0.0:
            yield waveform[start_index-chunk_size:start_index + chunk_size]
        start_index += chunk_size