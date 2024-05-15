#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

# Import the os package
import os
import speech_recognition as sr

import sounddevice
import requests

r = sr.Recognizer()

from dotenv import load_dotenv


load_dotenv()

# Import the openai package
import openai

# Set openai.api_key to the OPENAI environment variable
openai.api_key = os.environ.get('OPENAI')

model_name="gpt-3.5-turbo"


def chat_with_openai(prompt):
    """
    Sends the prompt to OpenAI API using the chat interface and gets the model's response.
    """
    message = {
        'role': 'user',
        'content': prompt
    }

    # response = openai.ChatCompletion.create(
    #     model=model_name,
    #     messages=[message]
    # )

    response = openai.ChatCompletion.create(
      model=model_name,
      messages=[
            {"role": "system", "content": "Use this format: adjective] [subject] [doing action], [creative lighting style], extremely detailed, surrealism, uncanny valley, in the style of [art medium], [famous art style]. Using that format, replace the bracketed words with fitting ideas and subjects from the user, making the words more illustrative and descriptive. Feel free to expand upon the ideas a bit, and fill in any that can't be found from the user input with words or descriptions that work well with the rest."},
         message
        ]
    )

    # Extract the chatbot's message from the response.
    # Assuming there's at least one response and taking the last one as the chatbot's reply.
    chatbot_response = response.choices[0].message['content']
    return chatbot_response.strip()

try:
    
    words = input()
    # print("Whisper thinks you said " + words)
    revisedPrompt = chat_with_openai(words)
    print("New Prompt: " + revisedPrompt)
    file1 = open("prompt.txt", "w")
    
 
    # \n is placed to indicate EOL (End of Line)
    # file1.write(words + "\n")
    file1.writelines(revisedPrompt)
    file1.close()  # to change file access modes

except sr.UnknownValueError:
    print("Whisper could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Whisper")

# # recognize speech using Whisper API
# OPENAI_API_KEY = "INSERT OPENAI API KEY HERE"
# try:
#     print(f"Whisper API thinks you said {r.recognize_whisper_api(audio, api_key=OPENAI_API_KEY)}")
# except sr.RequestError as e:
#     print("Could not request results from Whisper API")
