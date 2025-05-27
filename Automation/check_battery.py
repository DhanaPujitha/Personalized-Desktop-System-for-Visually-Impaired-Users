import psutil
import time
from Automation.speech import prntdisp

def check_battery_status():
    battery = psutil.sensors_battery()  # Get battery information
    if battery:
        percent = battery.percent  # Battery percentage
        plugged = battery.power_plugged  # Whether the device is plugged in or not

        # Print battery status
        prntdisp(f"\nBattery: {percent}%")
        if(plugged):
            prntdisp("\nCharger is plugged in.")

        # Check if battery level is at or below 15% and alert to charge
        if percent <= 15 and not plugged:
            prntdisp("\nWarning: Battery is low! Please charge your device.")
        
        # If the battery is charging and the level is above 95%, remind to unplug
        if plugged and percent >= 95:
            prntdisp("\nBattery is fully charged. Please unplug the device to avoid overcharging.")

        elif plugged:
            prntdisp("Device is plugged in, charging...")

        # Alert when the battery is low
        elif percent <= 15:
            prntdisp("Warning: Battery is low! Please plug in your charger.")
