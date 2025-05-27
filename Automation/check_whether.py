import requests
from Automation.speech import prntdisp

def get_weather(location):
    api_key = 'b2cd0e05d3834eac99b61210250102'  # Replace with your WeatherAPI key
    base_url = 'http://api.weatherapi.com/v1/current.json'
    params = {
        'key': api_key,
        'q': location
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        weather = data['current']['condition']['text']
        temperature = data['current']['temp_c']
        prntdisp(f"Weather in {location}: {weather}")
        prntdisp(f"Temperature: {temperature}°C")
    else:
        print("Failed to get the weather data.")
  
