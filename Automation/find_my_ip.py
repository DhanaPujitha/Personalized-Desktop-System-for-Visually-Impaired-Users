import requests

def find_my_ip():
    try:
        # Make the request to the ipify API
        response = requests.get('https://api64.ipify.org?format=json')
        response.raise_for_status()  # Check if the request was successful
        
        # Parse the JSON response
        ip_address = response.json()
        return ip_address["ip"]
    
    except requests.exceptions.RequestException as e:
        # Handle request errors (e.g., network issues)
        print(f"Error retrieving IP address: {e}")
        return None

def checkip():
    public_ip = find_my_ip()
    if public_ip:
        print(f"Your device Public IP Address: {public_ip}")
    else:
        print("Failed to retrieve the IP address.")
