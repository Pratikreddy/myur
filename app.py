import streamlit as st
from groq import Groq
import json

# Set up the page
st.set_page_config(page_title="Sky Kapture Interiors", layout="wide")

# Initialize the Groq client
groq_api_key = st.secrets["GROQ_API_KEY"]
myur_client = Groq(api_key=groq_api_key)

# Initial system message for Myur
system_message = """
You are Myur, a helpful assistant providing answers on behalf of Sky Kapture Interiors. Be professional and informative.

Company: Sky Kapture Interiors
Website: skykaptureinteriors.com

Trust us to elevate your space with a signature touch. At Sky Kapture Interiors, we believe that the essence of a space lies in its design. We are a passionate team of interior designers dedicated to transforming ordinary spaces into extraordinary environments that reflect our clients’ personalities, aspirations, and lifestyles. With an unwavering commitment to creativity, functionality, and innovation, we bring dreams to life, one space at a time.

About Us:
- Who we are: A team of creative and dedicated interior designers based in Coimbatore, Tamil Nadu, India.
- Our mission: To transform ordinary spaces into extraordinary environments with a signature touch.
- What we do: We offer a range of services including Modular Kitchen design, Living Space design, Bedroom Interior design, Home Garden design, False Ceiling design, and Study Room Interiors.

Contact Information:
- Address: 63A, TNHB Colony, Sowbagaya Nagar, Civil Aerodrome Post, Coimbatore, Tamil Nadu 641014
- Phone: +91 99949 68165
- Email: hello.skykaptureinteriors@gmail.com

Provide clear, concise, and helpful responses to any inquiries related to our services, team, projects, and how we can help transform spaces. Always maintain a professional and friendly tone.
"""

# Initialize chat history as a session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "system", "content": system_message}]
if "input_buffer" not in st.session_state:
    st.session_state.input_buffer = ""

# Title and description
st.title("Sky Kapture Interiors")
st.write("Trust us to elevate your space with a signature touch")

# Myur (Groq Agent) Integration
st.header("Chat with Myur, Your Design Assistant")

# Display chat history
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f"<div style='border: 2px solid red; padding: 10px; margin: 10px 0; border-radius: 8px; width: 80%; float: right; clear: both;'>{message['content']}</div>", unsafe_allow_html=True)
    elif message["role"] == "assistant":
        st.markdown(f"<div style='border: 2px solid green; padding: 10px; margin: 10px 0; border-radius: 8px; width: 80%; float: left; clear: both;'>{message['content']}</div>", unsafe_allow_html=True)

# Function to clear the input buffer
def clear_input():
    st.session_state.input_buffer = ""

# Chat input and submit button
user_input = st.text_input("Type your message here:", key="input_buffer")

if st.button("Send"):
    if user_input:
        message = user_input  # Store the input in a variable
        clear_input()  # Clear the input field

        # Append user input to chat history
        st.session_state.chat_history.append({"role": "user", "content": message})

        # Call Groq API with the entire chat history
        response = myur_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=st.session_state.chat_history,
            temperature=0.3,
            max_tokens=2000
        )
        chatbot_response = response.choices[0].message.content.strip()

        # Append chatbot response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": chatbot_response})

        st.experimental_rerun()
    else:
        st.warning("Please enter some text to chat.")
