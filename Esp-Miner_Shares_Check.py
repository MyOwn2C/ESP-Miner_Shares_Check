# Version V0.2 Release

import requests
import time
import subprocess

IP = "Your_Bitaxe_IP_Address" # Replace with your Bitaxe IP address

def get_shares_accepted(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        shares_accepted = data.get("sharesAccepted", "Not available")
        return shares_accepted
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

def restart_bitaxe():
    try:
        # Execute the restart command
        subprocess.run(["curl", "-X", "POST", "http://{IP}/api/system/restart"], check=True)
        print(" Bitaxe is restarting...")
    except subprocess.CalledProcessError as e:
        print(f"Failed to restart Bitaxe: {e}")

if __name__ == "__main__":
    api_url = "http://{IP}/api/system/info" 
    previous_shares = None # Setup inintal shares count
    restart_count = 0 # Keep count of how many times restart was triggered

    while True:
        shares_accepted_count = get_shares_accepted(api_url)
        
        print(f"Current Shares Accepted: {shares_accepted_count}, Restart Count: {restart_count}")
        
        # Countdown before next check in 300 seconds
        for i in range(300, 0, -1):
            print(f"Checking again in {i} seconds...", end='\r')
            time.sleep(1)

        # Check if shares have increased
        if previous_shares is not None and shares_accepted_count == previous_shares:
            restart_bitaxe()
            restart_count = restart_count + 1
            for j in range(180,0,-1): # Wait for 180 seconds after restart
                print(f"Checking after restart in {j} seconds...", end='\r')  
                time.sleep(1)
        
        previous_shares = shares_accepted_count
