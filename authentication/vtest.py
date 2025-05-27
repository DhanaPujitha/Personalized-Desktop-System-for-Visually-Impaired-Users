import pyaudio
import wave
import numpy as np
import librosa
import pickle

def record_voice_sample(filename="temp.wav", seconds=5):
    """
    Record a voice sample and save it as a WAV file.
    """
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 44100  # Record at 44100 samples per second
    p = pyaudio.PyAudio()

    print("Recording...")

    stream = p.open(format=sample_format, channels=channels,rate=fs, frames_per_buffer=chunk, input=True)
    frames = []

    for _ in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    print("Recording complete.")

def extract_features(audio_path):
    """
    Extract MFCC features from an audio file.
    """
    audio, sample_rate = librosa.load(audio_path, res_type='kaiser_fast')
    mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
    return np.mean(mfccs.T, axis=0)

def recognize_voice():
    """
    Recognize the user's voice by comparing the recorded voice sample to the trained GMM model.
    Return 1 for a successful match, 0 for a failure.
    """
    # Record the voice sample
    record_voice_sample()

    # Load the trained model
    model_path = 'authentication/voice/voice_model.pkl'  # Ensure this is the correct path
    with open(model_path, 'rb') as model_file:
        gmm = pickle.load(model_file)

    # Extract features from the recorded sample
    features = extract_features('temp.wav')

    try:
        # Predict the label for the recorded sample
        predicted_label = gmm.predict([features])[0]
        print(predicted_label)
        # Known user labels from your training data
        known_users = [0]  # Update this with actual labels

        if predicted_label in known_users:
            print(f"Recognized user: {predicted_label}")
            return 1  # Return 1 for successful recognition
        else:
            print("Voice not recognized.")
            return 0  # Return 0 for unsuccessful recognition
    except Exception as e:
        print(f"Error during voice recognition: {e}")
        return 0  # Return 0 in case of any error
