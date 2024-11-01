
import base64
import logging
import sys

from brains import chatgpt
from session_manager import update_conversation, fix_typos_in_wake_word, is_user_talking_to_me
from speech_module.transcription import LiveTranscription

import os

import streamlit as st
# from streamlit_chat import message

from llama_cpp import Llama

from speech_module.tts_model import TextToSpeechModel

from speech_module.inference import Inference
import numpy as np

tts = TextToSpeechModel()
live_inference = Inference()

with open("system_prompt.txt", "r") as f:
    system_prompt = f.read()


def alpaca_model(conversation, model):
    response = model.create_chat_completion(conversation)
    return response['choices'][0]['message']['content']

def pipeline(audio, engine="gpt"):


    float64_buffer = np.frombuffer(
        audio, dtype=np.int16) / 32767

    transcript, confidence = live_inference.buffer_to_text(float64_buffer)
    transcript = transcript.lower()
    print("user:", transcript)
    
    if len(transcript) == 0:
        
        return {"speech": b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', 
        "response": "0", 
        "transcript": "0"}
    # logger.info("TTS model loaded")

    # print(system_prompt)
    conversation = {"system": system_prompt, 
                    "user": " "}
    

    update_conversation(conversation, "user", transcript)
    
    # print(conversation)

    response = chatgpt(conversation) 
    
    print("Alice:", response)

    # print("Prompt invoked: ", conversation) 
    # update_conversation(conversation, "system", response)
    # message(response, is_user=True, avatar_style="adventurer", seed="Whiskers")

    speech = tts.tts_generator(response)
    
    return {"speech": speech, 
            "response": response, 
            "transcript": transcript}
                    # autoplay_audio(speech_file)

    #         if transcript == "quit": 
    #             message("Goodbye!", is_user=True, avatar_style="adventurer", seed="Whiskers")
    #             # live_transcription.stop()
    #             exit()
            
    #         if transcript == "restart":
    #             # live_transcription.stop()
    #             os.execvp(sys.executable, [os.environ.get("WORKDIR")+'/.venv/bin/python'] + sys.argv)

    # except KeyboardInterrupt:
    #     live_transcription.stop()
    #     exit()
