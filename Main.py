# import google-generativeapi
# https://aistudio.google.com/


from dotenv import load_dotenv
import os

load_dotenv()
key = str(os.getenv("GEMINI_API_KEY"))
# print(key)

import time
from google import genai
global client
global s

client = genai.Client(api_key=key)

s="Answer Questions Based on the pdf please!"


import asyncio


import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader

from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
API_VOICE = os.getenv("API_VOICE")
client1 = ElevenLabs(
    api_key=API_VOICE
)


if 'count' not in st.session_state:
    st.session_state['count'] = 0
if 'oldChat' not in st.session_state:
    st.session_state['oldChat'] = ""
if 'u_res' not in st.session_state:
    st.session_state['u_res'] = []
if 'a_res' not in st.session_state:
    st.session_state['a_res'] = []




    


file = st.file_uploader("Choose a file")

if file is not None:

    reader=PdfReader(file)

    oldChat="PDF Text: "
    if st.session_state['oldChat']=="":
        for i in range(len(reader.pages)):
            
            st.session_state['oldChat']+=reader.pages[i].extract_text()+"\n"
    
    
    prompt = st.chat_input("Say something")
    ans=""

    if st.button("Set Value") and not(prompt):
        prompt="Summarize this pdf for me please! Thanks!"
        time.sleep(5)
    if prompt:

        response = client.models.generate_content(model="gemini-3-flash-preview", 
        contents=st.session_state['oldChat']+prompt,config={'system_instruction':s})
        res=response.text
        st.session_state['oldChat']+="user: "+prompt+"Gemini: "+res+"\n"
        st.session_state['u_res'].append(prompt)
        st.session_state['a_res'].append(res)
        audio = client1.text_to_speech.convert(
    text=res,
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
)

        play(audio)
        ans=res
        st.session_state['count']+=1
 
    for i in range(st.session_state['count']):
        something = st.chat_message("user")
        something.write(st.session_state['u_res'][i])

        something2 = st.chat_message("assistant")
        something2.write(st.session_state['a_res'][i])
        



# if __name__ == "__main__":
#     asyncio.run(main())
