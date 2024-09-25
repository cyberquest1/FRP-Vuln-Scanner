import unittest
from unittest.mock import patch
import subprocess
import main  # Assuming your main.py is named this way

class TestFRPVulnScanner(unittest.TestCase):

    @patch('requests.get')
    def test_check_web_vulnerability(self, mock_get):
        # Simulate a successful response from the web
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "some_keyword_indicating_vulnerability"

        url = "http://example.com"
        with self.assertLogs(level='INFO') as log:
            main.check_web_vulnerability(url)
            self.assertIn(f"[+] Vulnerability found at: {url}", log.output)

    @patch('subprocess.run')
    def test_check_android_vulnerability_no_devices(self, mock_run):
        # Simulate no devices connected
        mock_run.return_value.stdout = "List of devices attached\n"

        with self.assertLogs(level='INFO') as log:
            main.check_android_vulnerability()
            self.assertIn("[!] No devices connected.", log.output)

    @patch('subprocess.run')
    def test_check_android_vulnerability_with_device(self, mock_run):
        # Simulate one connected device with debugging off
        mock_run.side_effect = [
            subprocess.CompletedProcess(args=[], returncode=0, stdout="device_id\tdevice"),
            subprocess.CompletedProcess(args=[], returncode=0, stdout="mtp,adb"),
            subprocess.CompletedProcess(args=[], returncode=0, stdout="some_keyword_indicating_vulnerability"),
        ]

        with self.assertLogs(level='INFO') as log:
            main.check_android_vulnerability()
            self.assertIn("[+] Checking device: device_id", log.output)
            self.assertIn("[+] FRP vulnerability found on device device_id.", log.output)

if __name__ == '__main__':
    unittest.main()
