import streamlit as st
import cx_Oracle

# Setting up a connection to the Oracle database (replace with your credentials)
dsn = cx_Oracle.makedsn('hostname', 'port', sid='sid')
connection = cx_Oracle.connect(user='username', password='password', dsn=dsn)

def get_account_data(account_number):
    """Fetch account data from the Oracle database."""
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM accounts WHERE account_number = {account_number}")
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    return data, columns

def show():
    st.header("Enter Account Number")
    account_number = st.text_input("Account Number", max_chars=8)
    if len(account_number) == 8:
        data, columns = get_account_data(account_number)
        st.table(data)
