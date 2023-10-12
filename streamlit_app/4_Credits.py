import streamlit as st

st.header('This is a header with a divider', divider='rainbow')

st.text('This is some text.')

st.sidebar.header('Sidebar')
account_number = st.sidebar.text_input('Enter Account Number', max_chars=8)

if st.sidebar.button('Submit'):
    st.sidebar.text('Account number submitted: {}'.format(account_number))
    # You can also add logic here that will run when the button is clicked.
    
def show():
    st.header("Data Dictionary")
    # Display your data dictionary here, e.g., 
    st.write("Account Number: Unique 8 digit number for each account")
