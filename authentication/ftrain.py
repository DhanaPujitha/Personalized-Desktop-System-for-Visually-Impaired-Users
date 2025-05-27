import os
import cv2
import numpy as np
from sklearn.decomposition import PCA
from sklearn.mixture import GaussianMixture
import pickle

def extract_face_features(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Convert to grayscale
    image = cv2.resize(image, (100, 100))  # Resize to a fixed size (e.g., 100x100)
    return image.flatten()  # Flatten the image to a 1D vector

def train_face_model():
    face_samples_dir = 'authentication/face'
    features = []
    labels = []

    for user_name in os.listdir(face_samples_dir):
        user_dir = os.path.join(face_samples_dir, user_name)
        
        if os.path.isdir(user_dir):
            for file_name in os.listdir(user_dir):
                file_path = os.path.join(user_dir, file_name)
                
                if os.path.isfile(file_path) and file_path.endswith('.jpg'):
                    try:
                        face_features = extract_face_features(file_path)
                        features.append(face_features)
                        labels.append(user_name)
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")
        else:
            print(f"Skipping {user_dir}, as it is not a directory.")

    features = np.array(features)
    labels = np.array(labels)

    # Use PCA to reduce dimensionality of the face images
    pca = PCA(n_components=10, whiten=True)
    features_pca = pca.fit_transform(features)

    # Train a Gaussian Mixture Model for face recognition
    gmm = GaussianMixture(n_components=len(np.unique(labels)), covariance_type='diag', n_init=3)
    gmm.fit(features_pca)

    # Save the PCA and GMM models
    model_path = 'authentication/face/face_model.pkl'
    with open(model_path, 'wb') as model_file:
        pickle.dump({'pca': pca, 'gmm': gmm, 'labels': labels}, model_file)

    print(f"Face model trained and saved as {model_path}")

# Example usage
if __name__ == "__main__":
    train_face_model()
