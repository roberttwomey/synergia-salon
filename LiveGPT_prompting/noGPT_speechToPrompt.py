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
            {"role": "system", "content": "You are assisting in creating a prompt for stable diffusion. It is generating over live video input. Use what the user says and translate it using important subjects in their speech to craft a well-worded prompt for stable diffusion."},
         message
        ]
    )

    # Extract the chatbot's message from the response.
    # Assuming there's at least one response and taking the last one as the chatbot's reply.
    chatbot_response = response.choices[0].message['content']
    return chatbot_response.strip()


# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

# # recognize speech using Sphinx
# try:
#     print("Sphinx thinks you said " + r.recognize_sphinx(audio))
# except sr.UnknownValueError:
#     print("Sphinx could not understand audio")
# except sr.RequestError as e:
#     print("Sphinx error; {0}".format(e))

# # recognize speech using Google Speech Recognition
# try:
#     # for testing purposes, we're just using the default API key
#     # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
#     # instead of `r.recognize_google(audiwordso)`
#     print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
# except sr.UnknownValueError:
#     print("Google Speech Recognition could not understand audio")
# except sr.RequestError as e:
#     print("Could not request results from Google Speech Recognition service; {0}".format(e))

# # recognize speech using Google Cloud Speech
# GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""INSERT THE CONTENTS OF THE GOOGLE CLOUD SPEECH JSON CREDENTIALS FILE HERE"""
# try:
#     print("Google Cloud Speech thinks you said " + r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS))
# except sr.UnknownValueError:
#     print("Google Cloud Speech could not understand audio")
# except sr.RequestError as e:
#     print("Could not request results from Google Cloud Speech service; {0}".format(e))

# # recognize speech using Wit.ai
# WIT_AI_KEY = "INSERT WIT.AI API KEY HERE"  # Wit.ai keys are 32-character uppercase alphanumeric strings
# try:
#     print("Wit.ai thinks you said " + r.recognize_wit(audio, key=WIT_AI_KEY))
# except sr.UnknownValueError:
#     print("Wit.ai could not understand audio")
# except sr.RequestError as e:
#     print("Could not request results from Wit.ai service; {0}".format(e))

# # recognize speech using Microsoft Bing Voice Recognition
# BING_KEY = "INSERT BING API KEY HERE"  # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings
# try:
#     print("Microsoft Bing Voice Recognition thinks you said " + r.recognize_bing(audio, key=BING_KEY))
# except sr.UnknownValueError:
#     print("Microsoft Bing Voice Recognition could not understand audio")
# except sr.RequestError as e:
#     print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))

# # recognize speech using Microsoft Azure Speech
# AZURE_SPEECH_KEY = "INSERT AZURE SPEECH API KEY HERE"  # Microsoft Speech API keys 32-character lowercase hexadecimal strings
# try:
#     print("Microsoft Azure Speech thinks you said " + r.recognize_azure(audio, key=AZURE_SPEECH_KEY))
# except sr.UnknownValueError:
#     print("Microsoft Azure Speech could not understand audio")
# except sr.RequestError as e:
#     print("Could not request results from Microsoft Azure Speech service; {0}".format(e))

# # recognize speech using Houndify
# HOUNDIFY_CLIENT_ID = "INSERT HOUNDIFY CLIENT ID HERE"  # Houndify client IDs are Base64-encoded strings
# HOUNDIFY_CLIENT_KEY = "INSERT HOUNDIFY CLIENT KEY HERE"  # Houndify client keys are Base64-encoded strings
# try:
#     print("Houndify thinks you said " + r.recognize_houndify(audio, client_id=HOUNDIFY_CLIENT_ID, client_key=HOUNDIFY_CLIENT_KEY))
# except sr.UnknownValueError:
#     print("Houndify could not understand audio")
# except sr.RequestError as e:
#     print("Could not request results from Houndify service; {0}".format(e))

# # recognize speech using IBM Speech to Text
# IBM_USERNAME = "INSERT IBM SPEECH TO TEXT USERNAME HERE"  # IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
# IBM_PASSWORD = "INSERT IBM SPEECH TO TEXT PASSWORD HERE"  # IBM Speech to Text passwords are mixed-case alphanumeric strings
# try:
#     print("IBM Speech to Text thinks you said " + r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD))
# except sr.UnknownValueError:
#     print("IBM Speech to Text could not understand audio")
# except sr.RequestError as e:
#     print("Could not request results from IBM Speech to Text service; {0}".format(e))

# recognize speech using whisper
try:
    
    words = r.recognize_whisper(audio, language="english")
    print("Whisper thinks you said " + words)
    #revisedPrompt = chat_with_openai(words)
    print("New Prompt: " + words)
    file1 = open("prompt.txt", "w")
    
 
    # \n is placed to indicate EOL (End of Line)
    # file1.write(words + "\n")
    file1.writelines(words)
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
