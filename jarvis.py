import threading
from Automation.speech import prntdisp
from Automation.greeting import greet_user
from Automation.check_battery import check_battery_status
from Automation.listen import listen

def main():
    # Function to speak text and wait for it to finish
    def speak_and_wait(text):
        prntdisp(text)
        while threading.active_count() > 1:  # Wait for the speak thread to finish
            pass
    
    # Start speaking "Loading Please Wait"
    speak_and_wait("Loading Please Wait")

    # Start speaking the greeting
    greet_user()  # Assuming `greet_user` already has `speak` integrated
    speak_and_wait("Greeting Complete.")
    
    # Start speaking battery status
    check_battery_status()  # Assuming `check_battery_status` also calls `speak` for its message
    speak_and_wait("Battery check complete.")
    
    # Start the listening thread for user commands
    listen_thread = threading.Thread(target=listen)
    listen_thread.daemon = True  # Allow the program to exit even if this thread is running
    listen_thread.start()

    # Main thread continues to run indefinitely, ensuring the program stays active
    while True:
        pass

if __name__ == "__main__":
    main()
    
