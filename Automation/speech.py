import sys
from win32com.client import Dispatch   

def print_animated_message(message: str):
    sys.stdout.write(message)
    sys.stdout.flush()

def prntdisp(text):
    speak = Dispatch("SAPI.Spvoice")
    speak.Speak(text)
    print_animated_message(f"Assistant: {text}")

