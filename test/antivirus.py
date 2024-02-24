import requests
from dotenv import load_dotenv
import os

# Load API Key from .env file
load_dotenv()
API_KEY = os.getenv('VIRUSTOTAL_API_KEY')

def scan_file(file_path):
    """
    Submits a file to the VirusTotal API for scanning.
    """
    url = 'https://www.virustotal.com/vtapi/v2/file/scan'
    params = {'apikey': API_KEY}
    
    # Using a context manager to ensure the file is properly closed
    with open(file_path, 'rb') as file_to_scan:
        files = {'file': (os.path.basename(file_path), file_to_scan)}
        response = requests.post(url, files=files, params=params)
    
    if response.status_code == 200:
        scan_results = response.json()
        return scan_results
    else:
        return {"error": f"HTTP Error: {response.status_code}", "message": response.text}

def interpret_scan_results(scan_results):
    """
    Interprets the scan results from VirusTotal API.
    """
    total_engines = scan_results.get('total', 0)
    positive_detections = scan_results.get('positives', 0)
    
    # Determine threat level based on the ratio of positive detections
    threshold = 0.1 * total_engines
    if positive_detections > threshold:
        threat_level = 'High'
    elif positive_detections > 0:
        threat_level = 'Moderate'
    else:
        threat_level = 'None'

    # Extracting detailed results
    detailed_results = scan_results.get('scans', {})
    engine_results = {engine: info.get('detected', False) for engine, info in detailed_results.items()}

    return {
        'threat_level': threat_level,
        'positive_detections': positive_detections,
        'total_engines': total_engines,
        'detailed_engine_results': engine_results
    }

# Example usage
if __name__ == '__main__':
    # Adjusted path to target 'done.exe' within the 'checker' directory
    file_path = r"C:\Users\devil\OneDrive\Desktop\checker\exe\done.exe"
    scan_response = scan_file(file_path)
    if 'error' not in scan_response:
        interpreted_results = interpret_scan_results(scan_response)
        print(interpreted_results)
    else:
        print(scan_response)
