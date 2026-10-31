import requests
import time

# Replace with your actual 10-digit PNR and RapidAPI Key
PNR_NUMBER = "YOUR_10_DIGIT_PNR"
API_KEY = "YOUR_RAPIDAPI_KEY"

def check_pnr():
    url = f"https://irctc1.p.rapidapi.com/api/v3/getPNRStatus?pnrNumber={PNR_NUMBER}"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "irctc1.p.rapidapi.com"
    }
    
    while True:
        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            
            # Navigate the JSON response to find the status
            status = data.get('data', {}).get('PassengerStatus', [{}])[0].get('CurrentStatus', 'Unknown')
            
            if 'CNF' in status:
                print(f"SUCCESS: Your ticket is Confirmed! (Status: {status})")
                break
            else:
                print(f"Current Status: {status}. Checking again in 10 minutes...")
                
        except Exception as e:
            print(f"Error checking status: {e}. Retrying in 10 minutes...")
            
        # Wait for 10 minutes (600 seconds) before checking again
        time.sleep(600)

if __name__ == "__main__":
    print(f"Starting PNR tracker for {PNR_NUMBER}...")
    check_pnr()
