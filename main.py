import streamlit as st
import openai

# Set OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Constants
QUESTION_PLACEHOLDER = "یہاں لکھیں"
CHATBOT_TITLE = "باٹ صاحب"
CHATBOT_DESCRIPTION = "باٹ صاحب سے بات کیجئے"
CHATBOT_INTRO = "اسلام علیکم! 👋  آج میں آپ کی کیا مدد کر سکتا ہوں؟"

st.set_page_config(page_title=CHATBOT_TITLE, page_icon=" 🤖 ")

# Styles
streamlit_style = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu&display=swap');

    * {
        font-family: 'Noto Nastaliq Urdu', serif;
        text-align: right;
    }              
    
    .basic-font {
        font-size: 2rem;        
    }
</style>
"""
st.markdown(streamlit_style, unsafe_allow_html=True)
basic_font_template = '<p class="basic-font">{}</p>'
# st.markdown(basic_font_template.format(CHATBOT_DESCRTIPTION), ...

st.title(CHATBOT_TITLE + " 🤖 ")
st.divider()
st.subheader(CHATBOT_DESCRIPTION)

# Chat Messages Container
with st.chat_message("assistant"):
    st.write(CHATBOT_INTRO)

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Respond in Urdu prompt
master_prompt = "Respond in the Urdu language to the folowing text: {}"

# React to user input
if prompt := st.chat_input(QUESTION_PLACEHOLDER):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": master_prompt.format(m["content"])}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
