import streamlit as st
import yfinance as yf
from twilio.rest import Client
import time

# --- CONFIGURATION ---
# Replace these with your Twilio credentials
TWILIO_SID = 'AC412603a0b82a46ddb73eaa955333c645'
TWILIO_TOKEN = 'ae3436bc226dcf781a424cbcd327e951'
TWILIO_WHATSAPP_FROM = 'whatsapp:+14155238886'  # Twilio Sandbox Number
MY_WHATSAPP_TO = 'whatsapp:+256786324893'        # Your Number

# --- FUNCTIONS ---
def send_alert(message):
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    client.messages.create(
        body=message,
        from_=TWILIO_WHATSAPP_FROM,
        to=MY_WHATSAPP_TO
    )

def get_live_price(symbol):
    ticker = yf.Ticker(symbol)
    data = ticker.fast_info
    return data['last_price']

# --- STREAMLIT UI ---
st.set_page_config(page_title="Forex Breakout Alert", page_icon="📈")
st.title("📈 Forex Support/Ceiling Monitor")
st.write("Monitor the market and get WhatsApp alerts when levels break.")

# Inputs
symbol = st.selectbox("Select Currency Pair", ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "AUDUSD=X"])
ceiling = st.number_input("Set Ceiling (Resistance)", format="%.4f", value=1.0950)
support = st.number_input("Set Support (Floor)", format="%.4f", value=1.0820)

# Monitoring Logic
if st.button("🚀 Start Monitoring"):
    st.info(f"Monitoring {symbol}... I will alert you at {MY_WHATSAPP_TO}")
    placeholder = st.empty()
    
    while True:
        try:
            current_price = get_live_price(symbol)
            placeholder.metric(label=f"Current {symbol} Price", value=f"{current_price:.4f}")
            
            if current_price >= ceiling:
                msg = f"🚀 BREAKOUT! {symbol} broke the CEILING at {current_price:.4f}. Time to trade!"
                send_alert(msg)
                st.success("Alert sent to WhatsApp!")
                break # Stop monitoring after alert
                
            elif current_price <= support:
                msg = f"📉 BREAKDOWN! {symbol} broke SUPPORT at {current_price:.4f}. Time to trade!"
                send_alert(msg)
                st.success("Alert sent to WhatsApp!")
                break
                
            time.sleep(10) # Checks every 10 seconds
            
        except Exception as e:
            st.error(f"Error: {e}")
            break