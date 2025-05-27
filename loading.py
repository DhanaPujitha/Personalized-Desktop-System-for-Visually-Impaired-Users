import sys
import cv2
import pyttsx3  # Import pyttsx3 for text-to-speech
import subprocess  # Import subprocess to run external scripts
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QGraphicsDropShadowEffect
from PyQt5.QtGui import QImage, QPixmap, QMovie
from authentication import ftest  # Correct import for ftest
from authentication import vtest  # Correct import for vtest


class RecognitionThread(QThread):
    # Create a custom signal to send recognition status
    recognition_status_signal = pyqtSignal(int)

    def run(self):
        # Run the face recognition and emit the result
        recognition_status = ftest.recognize_face()  # Call the function from ftest.py
        self.recognition_status_signal.emit(recognition_status)  # Emit the result


class VoiceRecognitionThread(QThread):
    # Create a custom signal to send voice recognition result
    voice_recognition_status_signal = pyqtSignal(int)

    def run(self):
        # Run the voice recognition and emit the result
        voice_recognition_status = vtest.recognize_voice()  # Call the function from vtest.py
        self.voice_recognition_status_signal.emit(voice_recognition_status)  # Emit the result


class SplashScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Splash Screen')
        self.setGeometry(100, 100, 600, 400)  # Adjust size as needed
        self.setStyleSheet("background-color: #2b2b2b;")  # Dark background color

        # Create label for showing GIF animation
        self.background_label = QLabel(self)
        self.add_gif_to_label(self.background_label, "page1.gif", size=(600, 300), alignment=Qt.AlignCenter)
        
        # Add a message below the GIF (e.g., Loading...)
        self.message_label = QLabel("Loading, please wait...", self)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        
        # Create a layout and add both the GIF and the message
        layout = QVBoxLayout()
        layout.addWidget(self.background_label)
        layout.addWidget(self.message_label)
        self.setLayout(layout)

        # Set window to stay on top and hide the borders
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        # Speak the "Loading, please wait..." message
        self.speak_loading_message()

        # Set a timer to close the GIF and start the camera feed after 3 seconds
        QTimer.singleShot(3000, self.close_gif_and_start_camera)

    def add_gif_to_label(self, label, gif_path, size=None, alignment=None):
        """Helper method to add a GIF to a label"""
        movie = QMovie(gif_path)
        label.setMovie(movie)
        movie.start()

        if size:
            label.setFixedSize(*size)

        if alignment:
            label.setAlignment(alignment)

        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        label.setGraphicsEffect(shadow)

    def close_gif_and_start_camera(self):
        """Stop displaying the GIF and start the camera feed"""
        self.background_label.clear()  # Clear the GIF
        self.start_camera_feed()  # Start showing the camera feed

    def start_camera_feed(self):
        """Start the camera feed"""
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Capture frames every 30ms (approx 30fps)
        self.message_label.setText("Waiting for face recognition...")

        # After a few seconds, send the captured image to ftest.py for face recognition
        QTimer.singleShot(3000, self.send_image_to_ftest)

    def update_frame(self):
        """Update the frame shown in the label to display the camera feed"""
        ret, frame = self.cap.read()
        if ret:
            # Convert the frame to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            p = QPixmap.fromImage(convert_to_Qt_format)
            self.background_label.setPixmap(p)

    def send_image_to_ftest(self):
        """Capture the current frame and send it to ftest.py for face recognition"""
        ret, frame = self.cap.read()
        if ret:
            # Save the current frame as an image
            cv2.imwrite("captured_face.jpg", frame)
            
            # Now, send the image to ftest for face recognition
            recognition_status = ftest.recognize_face("captured_face.jpg")  # Pass the image path to ftest
            self.update_recognition_status(recognition_status)
        else:
            print("Failed to capture the frame.")
            self.update_recognition_status(0)

    def update_recognition_status(self, recognition_status):
        """Update the splash screen with recognition status"""
        if recognition_status == 1:
            result_message = "Face recognition successful"
            self.speak_result(result_message)
            self.stop_camera_feed()  # Stop the camera feed once face recognition is successful
            self.show_voice_recognition_gif()  # Show the voice recognition GIF after face recognition
            self.start_voice_recognition()  # Start voice recognition if face is recognized
        else:
            result_message = "Face not recognized"
            self.speak_result(result_message)
            self.close_splash_screen()  # Close splash screen after result

    def stop_camera_feed(self):
        """Stop the camera feed"""
        self.cap.release()  # Release the camera
        self.timer.stop()  # Stop the timer for updating frames

    def show_voice_recognition_gif(self):
        """Display a new GIF for voice recognition"""
        self.add_gif_to_label(self.background_label, "page3.gif", size=(600, 300), alignment=Qt.AlignCenter)
        self.message_label.setText("Waiting for voice recognition...")
        self.message_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        
        # Speak the message for voice recognition
        self.speak_result("Please speak now for voice recognition...")

    def start_voice_recognition(self):
        """Start voice recognition in a background thread"""
        self.voice_recognition_thread = VoiceRecognitionThread()
        self.voice_recognition_thread.voice_recognition_status_signal.connect(self.update_voice_recognition_status)
        self.voice_recognition_thread.start()  # Start the voice recognition thread

    def update_voice_recognition_status(self, voice_recognition_status):
        """Update the splash screen with voice recognition result"""
        if voice_recognition_status == 1:
            result_message = "Voice recognition successful"
            self.speak_result(result_message)
            # Display final success message
            final_message = "Both face and voice recognition successful"
            self.speak_result(final_message)  # Speak out the success message
            self.message_label.setText(final_message)  # Update label with final message
            self.message_label.setStyleSheet("color: green; font-size: 20px; font-weight: bold;")  # Green text for success
            self.close()
            subprocess.run(['python', 'ui.py'], check=True)

        else:
            result_message = "Voice not recognized"
            self.speak_result(result_message)

        # Close splash screen after a short delay
        QTimer.singleShot(2000, self.close_splash_screen)  # Close splash screen after 2 seconds

    def speak_loading_message(self):
        """Speak the loading message using pyttsx3"""
        engine = pyttsx3.init()  # Initialize the TTS engine
        engine.setProperty('rate', 150)  # Set the speed of speech
        engine.setProperty('volume', 1)  # Set the volume (0.0 to 1.0)
        engine.say("Loading, please wait...")  # Say the loading message
        engine.runAndWait()  # Wait until speaking is done

    def speak_result(self, message):
        """Function to speak the result using pyttsx3"""
        engine = pyttsx3.init()  # Initialize the TTS engine
        engine.setProperty('rate', 150)  # Set the speed of speech
        engine.setProperty('volume', 1)  # Set the volume (0.0 to 1.0)
        engine.say(message)  # Say the message
        engine.runAndWait()  # Wait until speaking is done

def main():
    app = QApplication(sys.argv)

    # Create and show the splash screen first
    splash_screen = SplashScreen()
    splash_screen.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
