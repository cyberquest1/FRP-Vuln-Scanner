import requests
import argparse
import subprocess
import re

def check_web_vulnerability(url):
    """
    Check for FRP bypass vulnerabilities at the specified URL.
    """
    try:
        response = requests.get(url)
        # Example check for a specific vulnerability
        if 'some_keyword_indicating_vulnerability' in response.text:
            print(f"[+] Vulnerability found at: {url}")
        else:
            print(f"[-] No vulnerability found at: {url}")
    except requests.exceptions.RequestException as e:
        print(f"[!] Error checking {url}: {e}")

def check_android_vulnerability():
    """
    Check for FRP vulnerabilities on connected Android devices.
    """
    try:
        # List connected devices
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        devices = result.stdout.strip().split('\n')[1:]  # Skip the first line

        if not devices:
            print("[!] No devices connected.")
            return

        for device in devices:
            device_id = device.split()[0]
            print(f"[+] Checking device: {device_id}")

            # Check if USB debugging is enabled
            adb_output = subprocess.run(['adb', '-s', device_id, 'getprop', 'persist.sys.usb.config'], capture_output=True, text=True)
            usb_config = adb_output.stdout.strip()

            if "debug" not in usb_config:
                print(f"[-] USB debugging is off for device {device_id}.")
                # Check for FRP bypass by simulating a connection
                # Replace the following command with the actual FRP check command
                frp_check_output = subprocess.run(['adb', '-s', device_id, 'shell', 'some_frp_check_command'], capture_output=True, text=True)
                if 'some_keyword_indicating_vulnerability' in frp_check_output.stdout:
                    print(f"[+] FRP vulnerability found on device {device_id}.")
                else:
                    print(f"[-] No FRP vulnerability found on device {device_id}.")
            else:
                print(f"[+] USB debugging is enabled for device {device_id}.")
    except Exception as e:
        print(f"[!] Error checking Android devices: {e}")

def main():
    parser = argparse.ArgumentParser(description="FRP Vulnerability Scanner")
    parser.add_argument("--url", help="URL of the target to check for FRP vulnerabilities")
    parser.add_argument("--android", action="store_true", help="Check for FRP vulnerabilities on connected Android devices")
    args = parser.parse_args()

    if args.url:
        check_web_vulnerability(args.url)
    elif args.android:
        check_android_vulnerability()
    else:
        print("[!] Please specify a target (URL or Android)")

if __name__ == "__main__":
    main()
