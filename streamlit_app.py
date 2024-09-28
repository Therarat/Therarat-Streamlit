#pip install google-generativeai
import streamlit as st
import google.generativeai as genai

st.title("🐧 My chatbot app")
st.subheader("Conversation")
st.write("We are EASY DIY for reparing your Motorcycle")

# Capture Gemini API Key
gemini_api_key = st.text_input("Gemini API Key: "
                               , placeholder="AIzaSyCmmUgYhuq0hPp2jXfzvlFW0eJHjYnGqD0"
                               , type="password"
                               )
# Initialize the Gemini Model
if gemini_api_key:
    try:
        # Configure Gemini with the provided API Key
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-pro")
        st.success("Gemini API Key successfully configured.")
    except Exception as e:
        st.error(f"An error occurred while setting up the Gemini model: {e}")
# Initialize session state for storing chat history

#print("We are EASY DIY for reparing your Motorcycle")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Initialize with an empty list

# Dropdown for selecting the expertise level
expertise_level = st.selectbox("Choose your expertise level:", ["Beginner", "Intermediate", "Expert"])

# Dropdown for selecting the repair interval
repair_interval = st.selectbox("Choose the repair schedule:", ["Monthly Repair", "Yearly Repair", "5-Year Repair"])

# Define context based on expertise level
if expertise_level == "Beginner":
    expert_context = "You are an expert motorcycle repair technician. Respond in a simple and easy-to-understand way for a beginner motorcycle owner."
elif expertise_level == "Intermediate":
    expert_context = "You are an expert motorcycle repair technician. Provide moderately detailed advice to an intermediate motorcycle owner."
else:
    expert_context = "You are an expert motorcycle repair technician. Respond with detailed, expert-level advice from a motorcycle owner's perspective."

# Add the repair interval to the context
if repair_interval == "Monthly Repair":
    repair_context = "The user is asking for advice related to monthly motorcycle repairs."
elif repair_interval == "Yearly Repair":
    repair_context = "The user is asking for advice related to yearly motorcycle repairs."
else:
    repair_context = "The user is asking for advice related to 5-year motorcycle repairs."

# Combine the expertise level context with the repair interval context
full_context = f"{expert_context}\n{repair_context}"

# Display previous chat history using st.chat_message (if available)
for role, message in st.session_state.chat_history:
    st.chat_message(role).markdown(message)

# Capture user input and generate bot response
if user_input := st.chat_input("Type your message here..."):
    # Store and display user message
    st.session_state.chat_history.append(("user", user_input))
    st.chat_message("user").markdown(user_input)

    # Combine full context with user input
    context_with_input = f"{full_context}\n\n{user_input}"

    # Assume `model` is your Google Generative AI instance
    if model:
        try:
            response = model.generate_content(context_with_input)
            bot_response = response.text
            # Store and display the bot response
            st.session_state.chat_history.append(("assistant", bot_response))
            st.chat_message("assistant").markdown(bot_response)
        except Exception as e:
            st.error(f"An error occurred while generating the response: {e}")
