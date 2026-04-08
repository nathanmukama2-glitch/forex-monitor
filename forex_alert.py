import streamlit as st
import yfinance as yf
from twilio.rest import Client
import time

# --- CONFIGURATION ---
# Replace with your actual credentials
TWILIO_SID = 'AC412603a0b82a46ddb73eaa955333c645'
TWILIO_TOKEN = 'd9ed0a3bbccaa45010f17bbd4ca2d9a7'

# Phone Numbers (Use E.164 format: +256...)
TWILIO_NUMBER = '+14155238886'  # Your Twilio Trial Number
MY_NUMBER = '+256786324893'     # Your personal phone number

# --- ALERT FUNCTIONS ---

def send_all_alerts(price, level_type):
    """Sends SMS, WhatsApp, and makes a Phone Call simultaneously."""
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    msg_text = f"🚨 {level_type} BREAKOUT! {price:.4f}. Check your charts now!"

    # 1. Send SMS (The direct alarm)
    try:
        client.messages.create(body=msg_text, from_=TWILIO_NUMBER, to=MY_NUMBER)
    except Exception as e:
        st.error(f"SMS Error: {e}")

    # 2. Send WhatsApp (The record)
    try:
        client.messages.create(body=msg_text, from_=f'whatsapp:{TWILIO_NUMBER}', to=f'whatsapp:{MY_NUMBER}')
    except Exception as e:
        st.error(f"WhatsApp Error: {e}")

    # 3. Make Phone Call (The LOUD wake-up alarm)
    try:
        client.calls.create(
            twiml=f'<Response><Say voice="alice" loop="3">{msg_text}</Say></Response>',
            from_=TWILIO_NUMBER,
            to=MY_NUMBER
        )
    except Exception as e:
        st.error(f"Call Error: {e}")

# --- STREAMLIT INTERFACE ---
st.set_page_config(page_title="Forex Alarm Pro", page_icon="📈")
st.title("📈 Doctor Nathan's Forex Alarm")
st.markdown("Monitoring the markets while you work.")

col1, col2 = st.columns(2)
with col1:
    symbol = st.selectbox("Currency Pair", ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "AUDUSD=X"])
with col2:
    interval = st.number_input("Check every (seconds)", value=30, min_value=10)

ceiling = st.number_input("Set Ceiling (Resistance)", format="%.4f", value=1.0950)
support = st.number_input("Set Support (Floor)", format="%.4f", value=1.0820)

if st.button("🚀 Start 24/7 Monitoring"):
    st.info(f"System Active. Watching {symbol}...")
    price_display = st.empty()
    
    while True:
        try:
            # Get live price
            ticker = yf.Ticker(symbol)
            current_price = ticker.fast_info['last_price']
            price_display.metric(label=f"Current {symbol}", value=f"{current_price:.4f}")

            # Check levels
            if current_price >= ceiling:
                send_all_alerts(current_price, "CEILING")
                st.success("LEVEL BROKEN! Call and SMS initiated.")
                break # Stop after alerting to avoid multiple calls

            elif current_price <= support:
                send_all_alerts(current_price, "SUPPORT")
                st.success("LEVEL BROKEN! Call and SMS initiated.")
                break

            time.sleep(interval)
        except Exception as e:
            st.error(f"Connection Error: {e}")
            time.sleep(10)
