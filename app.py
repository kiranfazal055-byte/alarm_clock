# To run this app, make sure you have Streamlit and pyttsx3 installed.
# Install via: pip install streamlit pyttsx3
# Then run: streamlit run this_file.py

import streamlit as st
import pyttsx3
import threading
import datetime
import time

st.title("Simple Alarm Clock App")

# Input for alarm time (time of day)
alarm_time = st.time_input("Set the alarm time", value=datetime.time(8, 0))  # Default to 8:00 AM

# Input for the message to speak
message = st.text_input("Enter the message to speak", value="Wake up!")

# Button to set the alarm
if st.button("Set Alarm"):
    if message:
        def trigger_alarm():
            # Get current datetime
            now = datetime.datetime.now()
            
            # Combine today's date with the selected time
            alarm_datetime = datetime.datetime.combine(now.date(), alarm_time)
            
            # If the time is in the past, set it for tomorrow
            if alarm_datetime < now:
                alarm_datetime += datetime.timedelta(days=1)
            
            # Calculate seconds to wait
            wait_seconds = (alarm_datetime - now).total_seconds()
            
            # Wait until the alarm time
            time.sleep(wait_seconds)
            
            # Initialize text-to-speech engine
            engine = pyttsx3.init()
            engine.say(message)
            engine.runAndWait()
        
        # Run the alarm in a background thread so the app doesn't block
        threading.Thread(target=trigger_alarm).start()
        
        st.success(f"Alarm set for {alarm_time.strftime('%H:%M')} with message: '{message}'")
    else:
        st.warning("Please enter a message.")
