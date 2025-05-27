import os
import numpy as np
import librosa
from sklearn.mixture import GaussianMixture
import pickle

def extract_features(audio_path):
    audio, sample_rate = librosa.load(audio_path, res_type='kaiser_fast')
    mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
    return np.mean(mfccs.T, axis=0)

def train_voice_model():
    voice_samples_dir = 'authentication/voice'  # Update the path to the voice folder
    features = []
    labels = []

    for user_name in os.listdir(voice_samples_dir):
        user_dir = os.path.join(voice_samples_dir, user_name)
        
        if os.path.isdir(user_dir):  # Ensure this is a directory
            for file_name in os.listdir(user_dir):
                file_path = os.path.join(user_dir, file_name)
                
                if os.path.isfile(file_path) and file_path.endswith('.wav'):
                    try:
                        mfccs = extract_features(file_path)
                        features.append(mfccs)
                        labels.append(user_name)
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")
        else:
            print(f"Skipping {user_dir}, as it is not a directory.")

    features = np.array(features)
    labels = np.array(labels)

    # Train a Gaussian Mixture Model
    gmm = GaussianMixture(n_components=len(np.unique(labels)), covariance_type='diag', n_init=3)
    gmm.fit(features, labels)

    # Save the trained model
    model_path = 'authentication/voice/voice_model.pkl'  # Update the path to save the model
    with open(model_path, 'wb') as model_file:
        pickle.dump(gmm, model_file)

    print(f"Model trained and saved as {model_path}")

# Example usage
if __name__ == "__main__":
    train_voice_model()
