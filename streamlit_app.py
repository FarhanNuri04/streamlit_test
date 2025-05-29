import streamlit as st
import requests

# Set background color using CSS
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(to right, #a2c4fc, #ffffff);
    }
    .stApp {
        background: linear-gradient(to right, #a2c4fc, #ffffff);
        padding: 20px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Set the app title
st.title('🌐 FISA Dynamics SDN BHD')
st.subheader('🚀 LEAD By FarhanNuri')

# Add a welcome message
st.write('🫱 Left Hand: Syahmi Amirul')
st.write('🫲 Right Hand: Iddin Tod')
st.write('🧭 Co Pilot: Arif Akmal')

# Text input
widgetuser_input = st.text_input('✏️ Enter a custom message:', 'Hello, Streamlit!')
st.write('📢 Customized Message:', widgetuser_input)

# Get exchange rates from API
response = requests.get('https://api.vatcomply.com/rates?base=MYR')

if response.status_code == 200:
    data = response.json()
    rates = data.get('rates', {})
    currency_list = sorted(rates.keys())

    # Dropdown for selecting currency
    selected_currency = st.selectbox('💱 Select a currency to convert from MYR:', currency_list)

    # Display the exchange rate
    rate = rates.get(selected_currency)
    st.success(f"💹 1 MYR = {rate} {selected_currency}")

    # Input for amount conversion
    amount = st.number_input(f"Enter amount in MYR to convert to {selected_currency}:", min_value=0.0, value=1.0)
    converted = amount * rate
    st.info(f"💰 {amount:.2f} MYR = {converted:.2f} {selected_currency}")

else:
    st.error(f"API call failed with status code: {response.status_code}")
