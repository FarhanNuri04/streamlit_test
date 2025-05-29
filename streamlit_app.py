import streamlit as st
import requests

# Custom CSS for background and font
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(to right, #a2c4fc, #ffffff);
    }
    .stApp {
        font-family: 'Georgia', serif;
        background: linear-gradient(to right, #a2c4fc, #ffffff);
        padding: 20px;
        border-radius: 10px;
    }
    label, .stTextInput > div > div, .stSelectbox > div > div {
        font-family: Arial, sans-serif !important; /* keep input readable */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Set the app title
st.title('🌐 FISA Dynamics SDN BHD')
st.subheader('🚀 LEAD By FarhanNuri')

# Welcome team members
st.write('🫱 Left Hand: Syahmi Amirul')
st.write('🫲 Right Hand: Iddin Tod')
st.write('🧭 Co Pilot: Arif Akmal')

# Text input from user
widgetuser_input = st.text_input('✏️ Enter a custom message:', 'Hello, Streamlit!')
st.write('📢 Customized Message:', widgetuser_input)

# API call to get currency rates
response = requests.get('https://api.vatcomply.com/rates?base=MYR')

if response.status_code == 200:
    data = response.json()
    rates = data.get('rates', {})
    currency_list = sorted(rates.keys())

    # Dropdown selection
    selected_currency = st.selectbox('💱 Select a currency to convert from MYR:', currency_list)

    # Show exchange rate
    rate = rates.get(selected_currency)
    st.success(f"💹 1 MYR = {rate} {selected_currency}")

    # Amount input and conversion
    amount = st.number_input(f"Enter amount in MYR to convert to {selected_currency}:", min_value=0.0, value=1.0)
    converted = amount * rate
    st.info(f"💰 {amount:.2f} MYR = {converted:.2f} {selected_currency}")

else:
    st.error(f"API call failed with status code: {response.status_code}")
