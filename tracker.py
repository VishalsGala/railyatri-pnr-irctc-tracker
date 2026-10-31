import streamlit as st
import requests
import time

st.set_page_config(page_title="PNR Tracker", page_icon="🚆")
st.title("IRCTC Live PNR Tracker")

pnr_number = st.text_input("Enter 10-digit PNR", max_chars=10)
api_key = st.text_input("Enter RapidAPI Key", type="password")

if st.button("Start Tracking"):
    if len(pnr_number) == 10 and api_key:
        status_placeholder = st.empty()
        
        url = f"https://irctc1.p.rapidapi.com/api/v3/getPNRStatus?pnrNumber={pnr_number}"
        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "irctc1.p.rapidapi.com"
        }
        
        while True:
            try:
                response = requests.get(url, headers=headers)
                data = response.json()
                
                status = data.get('data', {}).get('PassengerStatus', [{}])[0].get('CurrentStatus', 'Unknown')
                
                if 'CNF' in status:
                    status_placeholder.success(f"SUCCESS: Ticket Confirmed! (Status: {status})")
                    st.balloons()
                    break
                else:
                    status_placeholder.info(f"Current Status: {status}. Next check in 10 minutes...")
                    
            except Exception as e:
                status_placeholder.error("Error fetching data. Retrying in 10 minutes...")
                
            # Wait 10 minutes before the next API call
            time.sleep(600)
    else:
        st.error("Please enter a valid 10-digit PNR and API Key.")
