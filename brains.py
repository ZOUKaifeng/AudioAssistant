import json
import os
import openai
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from langchain.schema import HumanMessage, SystemMessage



def chatgpt(message, model="gpt-3.5-turbo"):

    load_dotenv(".env")

    # openai.api_type = "azure"
    openai.api_base = "https://api.chatanywhere.tech"  #os.environ.get("OPENAI_API_BASE") 
    # openai.api_version = "2023-03-15-preview"
    # openai.api_key = os.environ.get("OPENAI_API_KEY")
    OPENAI_API_KEY = "INPUT YOUR API KEY"
    # response = openai.ChatCompletion.create(
    #             engine=model,
    #             messages=content
    #         )

    # self.llm = ChatOpenAI(temperature=0,
    #             max_tokens=4096,
    #             openai_api_key="EMPTY", 
    #             openai_api_base="https://api.chatanywhere.tech", 
    #             model_name="gpt-3.5-turbo")
    
    llm = ChatOpenAI(model_name=model, temperature=0, openai_api_base="https://api.chatanywhere.tech", max_tokens=4096, openai_api_key=OPENAI_API_KEY)
    
    print(message)
    messages = [
        SystemMessage(content=message['system']),
        HumanMessage(content=message['user'])
    ]
    return llm(messages).content

    # output = response['choices'][0]['message']['content']
    # return output






if __name__ == "__main__":
    import time
    content = "who are you?"
    start = time.time()
    print(chatgpt(content))
    end = time.time()
    print("time", end-start) 