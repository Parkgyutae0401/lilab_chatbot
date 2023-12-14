import streamlit as st
from streamlit_chat import message
import requests
 
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
API_TOKEN = "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"
headers = {"Authorization": f"Bearer {API_TOKEN}"}
 
st.header("🤖LILAB Bot (Demo)")
st.markdown("(https://sites.google.com/view/cau-li/home?authuser=0)")

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("");
             background-attachment: fixed;
             background-size: cover
             
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url() 
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
 
if 'past' not in st.session_state:
    st.session_state['past'] = []
 
def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
 
 
with st.form('form', clear_on_submit=True):
    user_input = st.text_input('입력해주세요: ', '', key='input')
    submitted = st.form_submit_button('보내기')
 
if submitted and user_input:
    output = query({
        "inputs": {
            "past_user_inputs": st.session_state.past,
            "generated_responses": st.session_state.generated,
            "text": user_input,
        },
        "parameters": {"repetition_penalty": 1.33},
    })
 
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output["generated_text"])
 
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))