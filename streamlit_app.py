import streamlit as st 
import requests

# Set the app title 
st.title('FISA Dynamics SDN BHD')
st.title('LEAD By FarhanNuri')

# Add a welcome message 
st.write('Left Hand : Syahmi Amirul')
st.write('Right Hand : Iddin Tod')
st.write('Co Pilot : Arif Akmal')
# Create a text input 
widgetuser_input = st.text_input('Enter a custom message:', 'Hello, Streamlit!') 

# Display the customized message 
st.write('Customized Message:', widgetuser_input)


#API calls
response = requests.get('https://api.vatcomply.com/rates?base=MYR')

if response.status_code == 200:
    data = response.json()
    st.write('Output:')
    st.json(data)  # nicely formatted JSON output
else:
    st.error(f"API call failed with status code: {response.status_code}")


