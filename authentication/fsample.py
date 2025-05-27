import cv2
import os

def capture_face_samples(user_name, sample_count=10):
    # Create the user's directory
    save_dir = f'authentication/face/{user_name}'
    os.makedirs(save_dir, exist_ok=True)

    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    count = 0
    while count < sample_count:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image.")
            break

        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = frame[y:y+h, x:x+w]
            file_path = os.path.join(save_dir, f'{user_name}.{count+1}.jpg')
            cv2.imwrite(file_path, face)
            count += 1
            print(f"Captured {count}/{sample_count} face samples for {user_name}")
        
        # Show the frame
        cv2.imshow('Face Capture', frame)

        # Press 'q' to quit capturing
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Example usage
if __name__ == "__main__":
    user_name = input("Enter your name: ")
    capture_face_samples(user_name)
