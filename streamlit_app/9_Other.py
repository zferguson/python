import streamlit as st
from streamlit_app import homepage, modify_data, data_dictionary

st.title("Streamlit Oracle App")
page = st.sidebar.selectbox("Choose a page", ["Homepage", "Modify Data", "Data Dictionary"])

if page == "Homepage":
    homepage.show()
elif page == "Modify Data":
    modify_data.show()
else:  # Data Dictionary
    data_dictionary.show()
