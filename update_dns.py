import requests, os
from dotenv import load_dotenv

# file to store last IP
last_ip_file = "last_ip.txt"


def get_public_ip():
    return requests.get("https://api.ipify.org").text

def read_last_ip():
    try:
        with open(last_ip_file, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def write_last_ip(ip):
    with open(last_ip_file, "w") as f:
        f.write(ip)

def update_dns(update_url):
    response = requests.get(update_url)
    return response.status_code == 200


def main():
    load_dotenv()

    print("checking DNS..")

    # dynamic update URL from FreeDNS
    update_url = str(os.getenv('UPDATE_URL'))

    current_ip = get_public_ip()
    last_ip = read_last_ip()

    if current_ip != last_ip:
        if update_dns(update_url):
            print(f"IP updated to {current_ip}")
            write_last_ip(current_ip)
        else:
            print("Failed to update IP")
    else:
        print("IP has not changed")
