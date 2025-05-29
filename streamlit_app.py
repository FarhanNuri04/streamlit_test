import streamlit as st
import requests

# CSS untuk ubah font + background gradient
st.markdown(
    """
    <style>
    html, body, [class*="css"]  {
        font-family: 'Georgia', serif !important;
        background: linear-gradient(to right, #a2c4fc, #ffffff);
    }
    input, textarea, select, button {
        font-family: Arial, sans-serif !important; /* Kekalkan font biasa untuk input */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Tajuk utama
st.title('🌐 FISA Dynamics SDN BHD')
st.subheader('🚀 LEAD By FarhanNuri')

# Pasukan
st.write('🫱 Left Hand: Syahmi Amirul')
st.write('🫲 Right Hand: Iddin Tod')
st.write('🧭 Co Pilot: Arif Akmal')

# Input mesej
widgetuser_input = st.text_input('✏️ Enter a custom message:', 'Hello, Streamlit!')
st.write('📢 Customized Message:', widgetuser_input)

# API exchange
response = requests.get('https://api.vatcomply.com/rates?base=MYR')

if response.status_code == 200:
    data = response.json()
    rates = data.get('rates', {})
    currency_list = sorted(rates.keys())

    # Pilih mata wang
    selected_currency = st.selectbox('💱 Select a currency to convert from MYR:', currency_list)

    # Papar kadar tukaran
    rate = rates.get(selected_currency)
    st.success(f"💹 1 MYR = {rate} {selected_currency}")

    # Kira tukaran
    amount = st.number_input(f"Enter amount in MYR to convert to {selected_currency}:", min_value=0.0, value=1.0)
    converted = amount * rate
    st.info(f"💰 {amount:.2f} MYR = {converted:.2f} {selected_currency}")

else:
    st.error(f"API call failed with status code: {response.status_code}")
