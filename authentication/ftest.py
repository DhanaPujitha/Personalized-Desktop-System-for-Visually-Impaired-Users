import os
import cv2
import numpy as np
import pickle
import time

def extract_face_features(image):
    """
    Extract features from the face image.
    - Converts the image to grayscale
    - Resizes it to a fixed size (100x100)
    - Flattens it into a 1D vector
    """
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    image = cv2.resize(image, (100, 100))  # Resize to a fixed size (100x100)
    return image.flatten()  # Flatten the image to a 1D vector

def recognize_face(image_path):
    """
    Recognizes the face from a given image file path.
    - Loads the trained PCA and GMM models
    - Processes the given image and performs face recognition
    """
    model_path = 'authentication/face/face_model.pkl'
    
    if not os.path.exists(model_path):
        print(f"Error: Model file not found at {model_path}.")
        return 0

    try:
        with open(model_path, 'rb') as model_file:
            model_data = pickle.load(model_file)
            pca = model_data['pca']
            gmm = model_data['gmm']
            labels = model_data['labels']
    except Exception as e:
        print(f"Error loading model: {e}")
        return 0

    # Load the image from the provided path
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not read the image from {image_path}.")
        return 0

    # Extract features from the image
    face_features = extract_face_features(image)

    # Transform the features using the PCA model
    face_features_pca = pca.transform([face_features])

    try:
        # Predict the label using the Gaussian Mixture Model
        probabilities = gmm.predict_proba(face_features_pca)[0]
        predicted_index = np.argmax(probabilities)
        predicted_label = labels[predicted_index]

        # If the prediction probability is above a threshold, consider the face recognized
        threshold = 0.5
        if probabilities[predicted_index] >= threshold:
            print(f"Face recognized: {predicted_label}")
            return 1  # Successful recognition
        else:
            print("Face not recognized.")
            return 0  # Unsuccessful recognition
    except Exception as e:
        print(f"Error during prediction: {e}")
        return 0  # Return 0 in case of an error
