import sys
import os
import subprocess
from PyQt5.QtCore import Qt, QProcess, QTimer, pyqtSignal, QSize
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QGraphicsDropShadowEffect, QLabel
from PyQt5.QtGui import QMovie
from Automation.speech import prntdisp

class JarvisUI(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Jarvis UI')
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: black;")  # Set background color to black

        # Create the layout
        layout = QVBoxLayout()

        # Create label for showing background animation (GIF or video)
        self.background_label = QLabel(self)
        self.add_gif_to_label(self.background_label, "page4.gif", size=(600, 400), alignment=Qt.AlignCenter)
        layout.addWidget(self.background_label)

        # Create QTextEdit for displaying commands and Jarvis output
        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet("color: white; font-size: 14px;")
        self.output_text.setPlaceholderText("Jarvis will display commands here...")
        layout.addWidget(self.output_text)

        # Set layout
        self.setLayout(layout)

        # Create QProcess to handle external scripts (e.g., Jarvis.py)
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)

        # Start Jarvis
        self.start_jarvis()

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

    def start_jarvis(self):
        """Run the Jarvis main.py script (voice recognition will be handled here)"""

        # Specify the path to main.py
        path_to_jarvis = "C:/Users/Dhana pujitha/OneDrive/Documents/New folder1/New folder/jarvis.py"  # Change path accordingly
        self.process.start("python", [path_to_jarvis])

    def handle_stdout(self):
        """Handle the standard output from Jarvis"""
        output = bytes(self.process.readAllStandardOutput()).decode("utf-8", errors="ignore")  # Ignore invalid characters
        # Remove extra newlines and ensure text is displayed in a clean format
        cleaned_output = " ".join(output.splitlines()).strip()
        # Display output in the QTextEdit widget
        self.display_output(cleaned_output)

    def handle_stderr(self):
        """Handle the standard error from Jarvis"""
        error_output = bytes(self.process.readAllStandardError()).decode("utf-8")
        self.display_output(f"ERROR: {error_output}")

    def display_output(self, text):
        """Display the output text in the QTextEdit widget"""
        if text:
            # Clean up text by replacing multiple newlines with one
            cleaned_text = text.replace("\n", " ").strip()

            if cleaned_text:
                # Avoid adding multiple newlines when not needed
                current_text = self.output_text.toPlainText()
                if current_text and not current_text.endswith("\n"):
                    self.output_text.append("")  # Add a newline before appending if needed
                
                # Append cleaned text
                self.output_text.append(cleaned_text)

    # Ensure the QTextEdit scrolls to the latest output
        self.output_text.ensureCursorVisible()


def main():
    app = QApplication(sys.argv)
    
    # Create and show the Jarvis UI window
    jarvis_ui = JarvisUI()
    jarvis_ui.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
