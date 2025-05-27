import threading
import pyttsx3
import speech_recognition as sr
import sys
import os
import datetime
# Add the path to the Automation folder
sys.path.append(r'c:\Users\Dhana pujitha\OneDrive\Documents\New folder1\New folder\Automation')

# Import your custom modules
from Automation.open_App import open_App
from Automation.web_app import openweb
from Automation.check_battery import check_battery_status
from Automation.br_percentage import check_br_persentage
from Automation.find_my_ip import checkip
from Automation.play_Music import play_music_on_youtube
from Automation.tab_automation import perform_browser_action
from Automation.data import tell_me_about
from Automation.news import NewsFromBBC
from Automation.check_whether import get_weather
from Automation.speech import prntdisp
from Automation.voice_email import send_email,read_unread_emails

def execute_command(command):
    output_text = ""
    # Check and execute the command related to apps
    if "send email" in command:
        send_email()
    
    elif "read email" in command:
        read_unread_emails()
         
    elif "open" in command:
        if "website" in command or "web" in command:
            web_name = command.replace("open", "").replace("open web", "").replace("website", "").strip()
            openweb(web_name)
            output_text = f"Opening {web_name} website."
        else:
            app_name = command.replace("open", "").strip()
            open_App(app_name)
            output_text = f"Opening {app_name}"


    elif 'the time' in command:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            prntdisp(f"The Time is {strTime}")

    # Play music on YouTube
    elif "play music" in command:
        song_name = command.replace("play music", "").strip()
        play_music_on_youtube(song_name)
        output_text = f"Playing {song_name} on YouTube."

    # Check battery status
    elif "check battery" in command:
        check_battery_status()
        output_text = "Battery status checked."

    elif "fetch news" in command:
        NewsFromBBC()
        output_text="News fetching completed"

    elif "restart the system" in command:
            os.system("shutdown /r /t 5")
# SLEEP
    elif "sleep" in command:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    # Check screen brightness
    elif "check brightness" in command:
        check_br_persentage()
        output_text = "Brightness status checked."

    # Check public IP address
    elif "ip address" in command:
        checkip()
        output_text = "Fetching your public IP address."

    elif "shut down the system" in command:
            os.system("shutdown /s /t 5")

    elif "tell me about" in command:
        ipt=command.replace("tell me about", "").strip()
        tell_me_about(ipt)
        output_text = "Fetching data completed."

    elif "check weather" in command:
        ipt=command.replace("check weather in","").strip()
        get_weather(ipt)
        output_text="Fetched weather completed"

    # Perform browser tab actions
    elif "browser action" in command:
        perform_browser_action(command)
        output_text = "Performing browser action."

    else:
        output_text = "Sorry, I did not recognize that command."

    prntdisp(output_text)