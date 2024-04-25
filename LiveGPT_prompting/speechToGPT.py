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

sound_device = int(os.environ.get('AUDIODEVICE'))

def main():
    """
    Main interaction loop for the chatbot.
    """
    print("Welcome to Chatbot! Type 'quit' to exit.")

    user_input = ""
    while user_input.lower() != "quit":
        with sr.Microphone(device_index=sound_device) as source:
            r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening
            print("Say something!")
            audio = r.listen(source)
            
        user_input = r.recognize_whisper(audio, language="english")
        print("You: " + user_input)
        # user_input = input("You: ")

        if user_input.lower() != "quit":
            response = chat_with_openai(user_input)  # Pass user_input as an argument
            print(f"Chatbot: {response}")

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
            {"role": "system", "content": "You are assisting in a live theater performance. You will recieve a line from the actor, and your job is to respond by feeding them a line to say. Keep it in context with what they said and respond with a line that fits within the conversation and relates to synergy and nature. Limit your response length to 100 words or less."},
         message
        ]
    )

    # Extract the chatbot's message from the response.
    # Assuming there's at least one response and taking the last one as the chatbot's reply.
    chatbot_response = response.choices[0].message['content']
    return chatbot_response.strip()


if __name__ == "__main__":
    main() 