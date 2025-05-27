import sys
from Automation.speech import prntdisp
sys.path.append(r'c:\Users\Dhana pujitha\OneDrive\Documents\New folder1\New folder')
import wmi
def get_brightness_windows():
    try:
        w = wmi.WMI(namespace='wmi')
        brightness_methods = w.WmiMonitorBrightness()
        brightness_percentage = brightness_methods[0].CurrentBrightness
        return brightness_percentage
    except Exception as e:
        return f"Error: {e}"

def check_br_persentage():
    brightness = get_brightness_windows()
    prntdisp(f"Current Brightness: {brightness}%")

