import pyaudio
import wave
import os

def capture_voice_samples(user_name, sample_count=10):
    # Define the directory to save voice samples
    save_dir = f'authentication/voice/{user_name}'
    os.makedirs(save_dir, exist_ok=True)
    
    # Set parameters for audio recording
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 44100  # Record at 44100 samples per second
    
    p = pyaudio.PyAudio()

    for i in range(sample_count):
        print(f'Recording sample {i+1}/{sample_count}...')
        
        stream = p.open(format=sample_format, channels=channels,
                        rate=fs, frames_per_buffer=chunk, input=True)
        frames = []
        
        for _ in range(0, int(fs / chunk * 3)):  # Record for 3 seconds
            data = stream.read(chunk)
            frames.append(data)
        
        # Stop and close the stream
        stream.stop_stream()
        stream.close()

        # Save the recorded audio as a WAV file
        sample_path = os.path.join(save_dir, f'{user_name}.{i+1}.wav')
        wf = wave.open(sample_path, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()

    p.terminate()
    print(f'Samples captured and saved in {save_dir}')

# Example usage
if __name__ == "__main__":
    user_name = input("Enter your name: ")
    capture_voice_samples(user_name)
