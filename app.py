import streamlit as st
from gtts import gTTS
import io
import base64
import datetime
import time
import threading

st.title("Alarm Clock with Voice Message 🎙️")

alarm_time = st.time_input("Set the alarm time", value=datetime.time(8, 0))
message = st.text_input("Enter the message to speak", value="Wake up!")

if st.button("Set Alarm"):
    if message:
        def trigger_alarm():
            now = datetime.datetime.now()
            alarm_datetime = datetime.datetime.combine(now.date(), alarm_time)
            if alarm_datetime < now:
                alarm_datetime += datetime.timedelta(days=1)
            
            wait_seconds = (alarm_datetime - now).total_seconds()
            time.sleep(wait_seconds)
            
            # Generate speech with gTTS
            tts = gTTS(text=message, lang='en')
            audio_bytes = io.BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            
            # Auto-play audio in browser
            audio_base64 = base64.b64encode(audio_bytes.read()).decode()
            audio_tag = f'''
            <audio autoplay="true">
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
            '''
            st.markdown(audio_tag, unsafe_allow_html=True)
            st.success(f"🔔 Alarm triggered: {message}")
        
        threading.Thread(target=trigger_alarm, daemon=True).start()
        st.success(f"Alarm set for {alarm_time.strftime('%H:%M')} — Message: '{message}'")
    else:
        st.warning("Enter a message!")

st.info("Note: Alarms longer than ~10-15 minutes may not work reliably on the cloud version (app can sleep). Run locally for long alarms!")
