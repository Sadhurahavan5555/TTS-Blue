import openai
import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
from gtts import gTTS
import IPython.display as ipd

img  = Image.open('Blue.png')
st.set_page_config(page_title='Blue', page_icon=img,)

hide_main_style = """
        <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        </style>
"""

st.markdown(hide_main_style, unsafe_allow_html=True)

with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Bot","Notes"],
        icons=["robot","bell fill"],
        menu_icon=None,
        default_index=0,
    )
if selected == "Notes":
    st.markdown("▸ I have used the OpenAi API key") 
    st.markdown("▸ I have added a TTS(Text to Speech) and some GUI")
    st.markdown("Check out my github")
    st.link_button("GitHub","https://github.com/Sadhurahavan5555")



if selected == "Bot":

    st.title("BLUE")
    user_message = "👤"
    name = "🤖"

    openai.api_key = st.secrets["API_KEY"]

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Type Here"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message(user_message):
            st.markdown(prompt)

        with st.chat_message(name = "assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

            tts = gTTS(full_response, lang='en')
            tts.save('assistant_response.mp3')

            st.audio('assistant_response.mp3', format='audio/mp3', start_time=0)

        st.session_state.messages.append({"role": "assistant", "content": full_response})

