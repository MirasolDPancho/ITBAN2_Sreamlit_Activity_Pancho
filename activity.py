import streamlit as st
import re

# App title and header
st.title("📱 Welcome to the Streamlit App")
st.header("🔐 User Information Form")

# Input fields
with st.form("user_form"):
    name = st.text_input("👤 Enter your full name")
    age = st.number_input("🎂 Enter your age", min_value=1, max_value=120)
    address = st.text_area("🏠 Enter your address")
    email = st.text_input("📧 Enter your email address")
    pin = st.text_input("🔢 Enter your 4-digit PIN", type="password")
    submitted = st.form_submit_button("Submit")

# Function to validate email
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email)

# Function to validate PIN
def is_valid_pin(pin):
    return len(pin) == 4 and pin.isdigit()

# Display results after form submission
if submitted:
    if not is_valid_email(email):
        st.error("❌ Invalid email format! Please enter a valid email address.")
    elif not is_valid_pin(pin):
        st.error("❌ PIN must be exactly 4 digits.")
    else:
        st.success("✅ Submission received!")
        st.write("You entered:")
        st.write(f"👤 Name: {name}")
        st.write(f"🎂 Age: {age}")
        st.write(f"🏠 Address: {address}")
        st.write(f"📧 Email: {email}")
        st.write(f"🔒 PIN: {'*' * len(pin)} (hidden for privacy)")
