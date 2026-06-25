import numpy as np
from scipy.io import wavfile
from io import BytesIO

def extract_waveform(file_bytes: bytes, num_samples: int = 1000) -> dict:
    """
    Extract downsampled waveform amplitude data from WAV file bytes.
    Returns a dict with sample rate, duration, and amplitude arrays.
    
    num_samples: number of data points to return (for frontend rendering)
    """
    try:
        sample_rate, data = wavfile.read(BytesIO(file_bytes))
    except Exception as e:
        raise ValueError(f"Failed to read WAV file: {e}")
    
    # convert to float32 and normalize to [-1.0, 1.0]
    if data.dtype == np.int16:
        data = data.astype(np.float32) / 32768.0
    elif data.dtype == np.int32:
        data = data.astype(np.float32) / 2147483648.0
    elif data.dtype == np.uint8:
        data = (data.astype(np.float32) - 128.0) / 128.0
    else:
        data = data.astype(np.float32)

    # if stereo, mix down to mono by averaging channels
    if data.ndim == 2:
        data = np.mean(data, axis=1)
    
    duration = len(data) / sample_rate

    # Downsample by chunking and taking min/max per chunk
    # This preserves peaks better than simple decimation
    chunk_size = max(1, len(data) // num_samples)
    num_chunks = len(data) // chunk_size

    mins = []
    maxs = []

    for i in range(num_chunks):
        chunk = data[i * chunk_size:(i + 1) * chunk_size]
        mins.append(float(chunk.min()))
        maxs.append(float(chunk.max()))

    return {
        "sample_rate": int(sample_rate),
        "duration": round(duration, 4),
        "min_samples": mins,
        "max_samples": maxs,
    }