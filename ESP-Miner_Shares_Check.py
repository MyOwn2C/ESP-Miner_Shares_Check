# Version V0.3 Release

import requests
import time
import subprocess
import os
from rich.console import Console
from rich.prompt import IntPrompt, Prompt

console = Console()
console.print("[bold green]ESP-Miner Shares Check v0.3[/bold green]")

Device_ip = Prompt.ask("[bold yellow]Enter Bitaxe IP[/bold yellow]")
Check_Interval = IntPrompt.ask("[bold yellow]Enter time between checks (mins) Default = 10[/bold yellow]", default=10, show_default=True) * 60

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
        subprocess.run(["curl", "-X", "POST", f"http://{Device_ip}/api/system/restart"], check=True)
        print(" Bitaxe is restarting...")
    except subprocess.CalledProcessError as e:
        print(f"Failed to restart Bitaxe: {e}")

if __name__ == "__main__":
    api_url = f"http://{Device_ip}/api/system/info" 
    previous_shares = None # Setup inintal shares count
    restart_count = 0 # Keep count of how many times restart was triggered

    while True:
        shares_accepted_count = get_shares_accepted(api_url)
        
        console.print(f"Current Shares Accepted: [bold green]{shares_accepted_count}[/bold green], Restart Count: [bold red]{restart_count}[/bold red]")
        
        # Countdown before next check in 300 seconds
        for i in range(Check_Interval, 0, -1):
            console.print(f"Checking again in [bold blue]{i}[/bold blue] seconds...", end='\r')
            time.sleep(1)

        # Check if shares have increased
        if previous_shares is not None and shares_accepted_count == previous_shares:
            restart_bitaxe()
            restart_count = restart_count + 1
            for j in range(180,0,-1): # Wait for 180 seconds after restart
                console.print(f"Checking after restart in [bold red]{j}[/bold red] seconds...", end='\r')  
                time.sleep(1)
        
        previous_shares = shares_accepted_count
