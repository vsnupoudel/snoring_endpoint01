from scipy.io import wavfile
from scipy.signal import resample
import numpy as np
import requests, json

# Ensure sample rate
def ensure_sample_rate(original_sample_rate, waveform, desired_sample_rate=16000):
    if original_sample_rate != desired_sample_rate:
        desired_length = int(  len(waveform) *  (desired_sample_rate/original_sample_rate ) )
        waveform = resample(waveform, desired_length)
    return  waveform

# Read and normalize audio
def read_and_normalise(file):
    try:
        sample_rate, wav_data = wavfile.read(file, 'rb')
        wav_data = wav_data.mean(axis=1)  # Convert to mono
        wav_data = ensure_sample_rate(sample_rate, wav_data)
        waveform = wav_data / wav_data.max()
        return waveform
    except Exception as e:
        raise RuntimeError(f"Error reading and normalizing audio: {str(e)}")

def split_generator(waveform, chunk_size=16000):
    """
    Splits the waveform into chunks of specified size.
    """
    start_index = chunk_size
    end_index = len(waveform) - 1 
    # while start_index+chunk_size < end_index:
    #     if waveform[start_index] > 0.0:
    #         yield waveform[start_index-chunk_size:start_index + chunk_size].tolist()
    #     start_index += chunk_size

    return ( 
    waveform[index-chunk_size:index + chunk_size].tolist() for index in range(start_index, end_index, chunk_size)
    if waveform[index] > 0.0 
    )
    
    # return [
    #     waveform[index-chunk_size:index + chunk_size].tolist() for index in range(start_index, end_index, chunk_size)
    #     if waveform[index] > 0.0 
    #     ]


def req_mp(wave: list):
    url = 'http://snoring:8501/v1/models/snoring_or_not:predict'
    payload = {"instances": wave}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json().get('predictions', {})  #json.loads(response.text)['predictions']
    except Exception as e:
        return {"error": str(e)}    

    return result
    
if __name__ == "__main__":
    import sys, time
    import multiprocessing  as mp
    if len(sys.argv) > 1:
        file = sys.argv[1]
    waveform = read_and_normalise(file)
    waveform = split_generator(waveform)
    
    t0 = time.time()
    with mp.Pool(processes= mp.cpu_count() ) as pool:
        results = pool.map(req_mp, [next(waveform) for i in range(30)]  )
 
    # results = [ req_mp(wave) for wave in waveform]
    
    t1 = time.time()
    print(f"\n\n {len(results)} , {results[-2:]} \n\n")
    print(f"Time taken: {t1-t0} seconds")
