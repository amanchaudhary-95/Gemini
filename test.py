import streamlit as st
import google.generativeai as genai
import time

@st.cache_resource
def get_model():
    genai.configure(api_key=st.secrets['gemini']['API_KEY'])
    model = genai.GenerativeModel('gemini-pro')
    return model

def on_change():
    st.session_state['history'] = st.session_state['user_log'][st.session_state['option']]

dev = """:blue[**NLP Application - Conversational Chat Bot**]  
    **Developed by** : Group 58  
    AMAN CHAUDHARY (2022aa05016)  
    ANEESH DAS (2022aa05135)  
    NAVINDRA RAY (2022aa05024)  
    VINODH KUMAR S (2022aa05190)"""
st.set_page_config(
    page_title='Conversational Chat Bot',
    page_icon='💬',
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
    'About': dev})
st.markdown('<style>div.block-container{padding-top:1.5rem;}</style>', unsafe_allow_html=True)

if 'user_log' not in st.session_state:
    st.session_state['history'] = []
    st.session_state['user_log'] = {}

st.subheader("🤖 Conversational Chat Bot", anchor=False, divider='rainbow')

st.sidebar.markdown('📝 :blue[<u>**Chat History**</u>]', unsafe_allow_html=True)
st.sidebar.radio(':blue[**Chat History**]', options=st.session_state['user_log'].keys(), label_visibility='collapsed', key='option', on_change=on_change)

for msg in st.session_state['history']:
    chat_msg = st.chat_message('assistant', avatar='🤖') if msg.role == 'model' else st.chat_message('user', avatar='👤')
    chat_msg.markdown(msg.parts[0].text, unsafe_allow_html=True)

if prompt := st.chat_input('Ask me anything'):
    with st.chat_message("user", avatar='👤'):
        st.markdown(prompt, unsafe_allow_html=True)
    with st.chat_message("assistant", avatar='🤖'):
        model = get_model()
        chat = model.start_chat(history=st.session_state['history'])
        resp = ""
        with st.spinner('Generating the response...'):
            place_holder = st.empty()
            for chunk in chat.send_message(prompt, stream=True):
                text = chunk.text.replace('•', '  *')
                resp += text + ' '
                time.sleep(0.05)
                place_holder.markdown(resp+"▌", unsafe_allow_html=True)
        place_holder.markdown(resp, unsafe_allow_html=True)
    st.session_state['history'] = chat.history

if len(st.session_state['history'])==0:
    c1, c2,_ = st.columns(3)
    c2.info(dev)
    st.toast("**Hi, I'm your personal assistant. Ask me anything**")

st.sidebar.divider()
col1, col2 = st.sidebar.columns(2)
if col1.button('✨ New Chat'):
    his = st.session_state['history'].copy()
    st.session_state['user_log'].update({st.session_state['history'][0].parts[0].text : his})
    st.session_state['history'].clear()
    st.rerun()

if col2.button('🧹 Clear Chat'):
    st.session_state['history'].clear()
    st.rerun()
