import requests
import os
import ctypes
import platform
import colorama
from colorama import Fore, Back, Style
import random
import json

colorama.init(autoreset=True)
version = "1.0.0"

def send_webhook(message):
    webhook_url = "error_discord_webhook_url"
    
    payload = {
        "content": message
    }

    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending webhook message: {e}")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_program_files_path():
    # Get the correct path for the "Program Files" directory
    if platform.system() == 'Windows':
        return os.path.join(os.environ['ProgramFiles'], 'Zephyr')
    else:
        # Add support for other operating systems if needed
        return None

def check_internet_connection():
    try:
        requests.get('http://www.google.com', timeout=1)
        return True
    except requests.ConnectionError:
        return False

def main():
    if not is_admin():
        print(f"{Fore.RED}Please run the OS as an administrator!")
        print()
        input(f"{Fore.GREEN}Press enter to leave.{Fore.WHITE}")
        exit()
        return

    zephyr_path = get_program_files_path()

    if zephyr_path:
        # Create Zephyr folder if it doesn't exist
        os.makedirs(zephyr_path, exist_ok=True)

        # Path to old_data.txt
        file_path = os.path.join(zephyr_path, 'old_data.txt')

        if os.path.exists(file_path) and os.path.getsize(file_path) > 0 and not check_internet_connection():
            # Run the script from old_data.txt if it exists and has content
            with open(file_path, 'r') as file:
                script = file.read()
        elif check_internet_connection():
            # Fetch the script from the link if old_data.txt doesn't exist or is empty
            try:
                response = requests.get("main_file")
                script = response.content.decode("utf-8")

                # Write the script content to old_data.txt
                with open(file_path, 'w') as file:
                    file.write(script)
            except Exception as e:
                id = random.randint(10000000000, 99999999999999999)
                send_webhook(f"**__{id}__**:\n\n{e}")
                print(f"{Fore.RED}Please contact owner with this error id: {Fore.YELLOW}{id}")
                print()
                input(f"{Fore.GREEN}Press enter to leave.{Fore.WHITE}")
                exit()
                return
        else:
            # Display a message if there is no internet connection and old_data.txt is empty
            print("Please connect to the internet first.")
            print()
            input(f"{Fore.GREEN}Press enter to leave.{Fore.WHITE}")
            exit()
            return


        # Execute the script in a global namespace
        globals_dict = {}
        try:
            exec(script, globals_dict)
        except Exception as e:
            id = random.randint(10000000000, 99999999999999999)
            send_webhook(f"**__{id}__**:\n\n{e}")
            print(f"{Fore.RED}Please contact owner with this error id: {Fore.YELLOW}{id}")
            print()
            input(f"{Fore.GREEN}Press enter to leave.{Fore.WHITE}")
            return

        # Get the run and end functions from the globals
        run = globals_dict.get("run")
        end = globals_dict.get("end")

        # Check if the run and end functions are defined
        if run and end and callable(run) and callable(end):
            run()
            end()
        else:
            id = random.randint(10000000000, 99999999999999999)
            send_webhook(f"**__{id}__**:\n\nThe script doesnt have defined required functions.")
            print(f"{Fore.RED}Please contact owner with this error id: {Fore.YELLOW}{id}")
            print()
            input(f"{Fore.GREEN}Press enter to leave.{Fore.WHITE}")
            
def get_latest_version():
    try:
        response = requests.get("data_file")
        data = response.json()
        return data.get("latest_version")
    except Exception as e:
        id = random.randint(10000000000, 99999999999999999)
        send_webhook(f"**__{id}__**:\n\nData Error")
        return ""

def update_required(current_version, latest_version):
    if current_version != latest_version:
        return True
    else:
        return False

if check_internet_connection():
    if update_required(version, get_latest_version()):
        print(f"{Fore.RED}Please update your OS to latest version.")
        print(f"{Fore.YELLOW}Your version: {Fore.RED}{version} (Outdated)")
        print(f"{Fore.YELLOW}Latest version: {Fore.GREEN}{get_latest_version()}")
        print()
        print(f"{Fore.YELLOW}If you want to get help with installing latest version of this OS, please visit our help center, what you can reach at: {Fore.CYAN}https://zephyr.load-dev.xyz{Fore.YELLOW}. There you can select category and we will help you with preinstallation.")
        print(f"{Fore.RED}We are sorry for this complications, but OS was updated to version where the launcher has to be updated too! Please respect our requirements and we wish you a nice experience with {Fore.GREEN}Zephyr{Fore.RED}!")
        print()
        input(f"{Fore.GREEN}Press enter to leave!{Fore.WHITE}\n")    
    else:
        main()
else:
    main()
