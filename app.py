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

# Sidebar navigation
st.sidebar.title("SKY KAPTURE INTERIORS")
menu = ["Home", "About Us", "Our Services", "Contact Us"]
choice = st.sidebar.radio("Navigation", menu)

# Home Section
if choice == "Home":
    st.title("Sky Kapture Interiors")
    st.subheader("Trust us to elevate your space with a signature touch")
    st.write("We’re a modern interior design agency with a focus on quality craftsmanship and innovative design solutions. Whether you’re looking to refresh a room or undertake a complete renovation, trust Sky Kapture Interiors to elevate your interior design experience to new heights.")
    st.image("home_image.jpg")  # Replace with your own image

# About Us Section
elif choice == "About Us":
    st.title("About Us")
    st.write("""
    At Sky Kapture Interiors, we believe that the essence of a space lies in its design. We are a passionate team of interior designers dedicated to transforming ordinary spaces into extraordinary environments that reflect our clients’ personalities, aspirations, and lifestyles. With an unwavering commitment to creativity, functionality, and innovation, we bring dreams to life, one space at a time.
    """)
    st.image("about_us_image.jpg")  # Replace with your own image

# Our Services Section
elif choice == "Our Services":
    st.title("Our Services")
    services = {
        "Modular Kitchen": "With our keen eye for detail and commitment to excellence, we bring your dream kitchen to life, tailored precisely to your needs and preferences.",
        "Living Space Design": "Transform your living space into a captivating cinematic retreat with our expertly crafted interior designs tailored to your style and preferences.",
        "Bedroom Interior Design": "The bedroom interior design of different spaces, such as house, villa, and apartment, and other places for residential use.",
        "Home Garden Design": "From meticulous landscape design to precise maintenance, we ensure that every garden flourishes under our care, creating environments that inspire and delight.",
        "False Ceiling": "Our dedicated team specializes in creating stunning false ceilings tailored to your unique aesthetic preferences and functional requirements.",
        "Study Room Interiors": "With our expertise in interior design, we transform ordinary study spaces into inspiring environments that foster productivity and creativity."
    }
    
    for service, description in services.items():
        st.subheader(service)
        st.write(description)
        st.image(f"{service.replace(' ', '_').lower()}_image.jpg")  # Replace with your own images

# Contact Us Section
elif choice == "Contact Us":
    st.title("Contact Us")
    st.write("If you like our works and want to cooperate, don’t hesitate to contact us. We’ll get back to you.")
    
    with st.form(key='contact_form'):
        name = st.text_input("Your Name*")
        email = st.text_input("Email Address*")
        phone = st.text_input("Phone Number")
        interest = st.text_input("You interested in?")
        message = st.text_area("Message")
        submit_button = st.form_submit_button(label='Submit')
        
        if submit_button:
            st.write("Thank you for reaching out! We'll get back to you soon.")
    
    st.write("Address: 63A, TNHB Colony, Sowbagaya Nagar, Civil Aerodrome Post, Coimbatore, Tamil Nadu 641014")
    st.write("Phone: +91 99949 68165")
    st.write("Email: hello.skykaptureinteriors@gmail.com")

# Footer
st.sidebar.write("---")
st.sidebar.write("Sign up to stay up to date")
email = st.sidebar.text_input("Enter email address")
if st.sidebar.button("Subscribe"):
    st.sidebar.write("Thank you for subscribing!")
st.sidebar.write("COPYRIGHT 2024 © SKY KAPTURE INTERIORS")

# Myur (Groq Agent) Integration
st.header("Chat with Myur, Your Design Assistant")

# Display chat history
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f"<div style='border: 2px solid red; padding: 10px; margin: 10px 0; border-radius: 8px; width: 80%; float: right; clear: both;'>{message['content']}</div>", unsafe_allow_html=True)
    elif message["role"] == "assistant":
        st.markdown(f"<div style='border: 2px solid green; padding: 10px; margin: 10px 0; border-radius: 8px; width: 80%; float: left; clear: both;'>{message['content']}</div>", unsafe_allow_html=True)

# Chat input and submit button
user_input = st.text_input("Type your message here:", key="user_input")

if st.button("Send"):
    if user_input:
        # Append user input to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})

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

        # Clear the input buffer
        st.session_state.input_buffer = ""
        st.experimental_rerun()
    else:
        st.warning("Please enter some text to chat.")

