import pyaudio
import speech_recognition as sr
import sys
sys.path.append(r'c:\Users\Dhana pujitha\OneDrive\Documents\New folder1\New folder')
from commands import execute_command
from Automation.speech import prntdisp, print_animated_message

def listen():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        prntdisp("Calibrating for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

    recognizer.energy_threshold = 4000  # Adjust this value based on the environment

    while True:
        try:
            with mic as source:
                print_animated_message("Say something!")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
                try:
                    # Recognize speech using Google Web Speech API
                    text = recognizer.recognize_google(audio, show_all=False)
                    print_animated_message(f"You Said: {text}")
                    execute_command(text)  # Execute the recognized command
                except sr.UnknownValueError:
                    prntdisp("")
                except sr.RequestError:
                    prntdisp("")
        except sr.WaitTimeoutError:
            prntdisp("Listening timed out, please try again.")