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
# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client(api_key=key)
# chat = client.chats.create(model="gemini-3-preview")
s="Answer Questions Based on the pdf please!"
# while True:
#     time.sleep(5)
#     user= input("Ask: ")
#     if user.lower()=="quit":
#         break
#     response = chat.send_message(user)#,config={'system_instruction':s})
#     print(response.text)

import asyncio

# async def askgem(askedVal:str)-> str:

# while True:

# response = client.models.generate_content(model="gemini-3-flash-preview", contents=askedVal,config={'system_instruction':s})
# res=response.text
# print(res)

# interaction =  client.interactions.create(
#     model="gemini-3-flash-preview",
#     input="Tell me a short joke about math."
# )

# print(interaction.outputs[-1].text)
import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader#,PdfWriter

from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
API_VOICE = os.getenv("API_VOICE")
client1 = ElevenLabs(
    api_key=API_VOICE
)


# st.title("My First Streamlit App")
# st.write("Hello, *world!*")

if 'count' not in st.session_state:
    st.session_state['count'] = 0
if 'oldChat' not in st.session_state:
    st.session_state['oldChat'] = ""
if 'u_res' not in st.session_state:
    st.session_state['u_res'] = []
if 'a_res' not in st.session_state:
    st.session_state['a_res'] = []




    


file = st.file_uploader("Choose a file")
# file = open("Computing_Cheat_Sheet.pdf","rb")
if file is not None:

    reader=PdfReader(file)
#a=reader.metadata 
#a.title
    oldChat="PDF Text: "
    if st.session_state['oldChat']=="":
        for i in range(len(reader.pages)):
            
            st.session_state['oldChat']+=reader.pages[i].extract_text()+"\n"
    #if True: #while True
        # time.sleep(10)
    # st.button("Set Value")

    
    prompt = st.chat_input("Say something")
    ans=""

    if st.button("Set Value") and not(prompt):
        prompt="Summarize this pdf for me please! Thanks!"
        time.sleep(5)
    if prompt:
        # user = input("Ask: ")
            # if prompt.lower()=="quit":
            #     break
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
    #     with st.chat_message("User", avatar=None):
    #         for i in st.session_state['u_res']:
    #             st.write(i)
    # # if prompt:
    # #     st.write(f"User has sent the following prompt: {prompt}")

    #     with st.chat_message("assistant"):
    #         for i in st.session_state['a_res']:
    #             st.write(i)
    for i in range(st.session_state['count']):
        something = st.chat_message("user")
        something.write(st.session_state['u_res'][i])

        something2 = st.chat_message("assistant")
        something2.write(st.session_state['a_res'][i])
        


# if prompt:
#     st.write(f"User has sent the following prompt: {prompt}")




    # return res

# async def main():
#     while True:
#         user= input("Ask: ")
#         if user.lower()=="quit":
#             break
#         # task1 = asyncio.create_task(asyncio.to_thread(askgem,user))
#         res=await askgem(user)
#         print(res)
#         # print(f"Tasks Results: {res.text}")




# if __name__ == "__main__":
#     asyncio.run(main())