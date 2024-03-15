import openai
import os
import requests
import uuid
from flask import Flask, request, jsonify, send_file, render_template
#import elevenlabs


# Add your OpenAI API key
OPENAI_API_KEY = ""
openai.api_key = OPENAI_API_KEY

# Add your ElevenLabs API key
ELEVENLABS_API_KEY = ""
ELEVENLABS_VOICE_STABILITY = 0.50
ELEVENLABS_VOICE_SIMILARITY = 0.75
ELEVENLABS_VOICE_STYLE = 0.9

# Choose your favorite ElevenLabs voice
ELEVENLABS_VOICE_NAME = "Marcus"
ELEVENLABS_ALL_VOICES = []

app = Flask(__name__)


def get_voices() -> list:
    """Fetch the list of available ElevenLabs voices.

    :returns: A list of voice JSON dictionaries.
    :rtype: list

    """
    url = "https://api.elevenlabs.io/v1/voices"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY
    }
    response = requests.get(url, headers=headers)
    return response.json()["voices"]


def transcribe_audio(filename: str) -> str:
    """Transcribe audio to text.

    :param filename: The path to an audio file.
    :returns: The transcribed text of the file.
    :rtype: str

    """
    with open(filename, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript.text


def generate_reply(conversation: list) -> str:
    """Generate a ChatGPT response.

    :param conversation: A list of previous user and assistant messages.
    :returns: The ChatGPT response.
    :rtype: str

    """
    response = openai.ChatCompletion.create(
      model="ft:gpt-3.5-turbo-0125:university-of-nebraska-lincoln:johnny-dolphin:90do1qS2",
      messages=[
            {"role": "system", "content": "You are John P. Allen, otherwise known as Johnny Dolphin, an author, poet, playwright, engineer, entrepreneur, and futurist. You also are the founder of Synergia Ranch, which serves as a site for exploring sustainable living practices, ecological research, and artistic endeavors. Your work frequently revolves around exploring innovative approaches to address environmental challenges and envisioning potential futures for humanity. You are very familiar with your memoir called Me and The Biospheres and will reference specific events from your life. You are acting as John Allen at Synergia Ranch during a show utilizing AI called Theater of Latent Possibilities. It reimagines the Synergia Archive with AI. You will respond in the first person as John Allen and will limit your response length to 100 words or less."},
        ] + conversation
    )
    return response["choices"][0]["message"]["content"]


def generate_audio(text: str, output_path: str = "") -> str:
    """Converts

    :param text: The text to convert to audio.
    :type text : str
    :param output_path: The location to save the finished mp3 file.
    :type output_path: str
    :returns: The output path for the successfully saved file.
    :rtype: str

    """
    voices = ELEVENLABS_ALL_VOICES
    # try:
    #     voice_id = next(filter(lambda v: v["name"] == ELEVENLABS_VOICE_NAME, voices))["voice_id"]
    # except StopIteration:
    #     voice_id = voices[0]["voice_id"]
    voice_id = "G8XrPBomxawzpcztpngK"
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    #print(voice_id)
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "content-type": "application/json"
    }
    data = {
        "text": text,
        "voice_settings": {
            "stability": ELEVENLABS_VOICE_STABILITY,
            "similarity_boost": ELEVENLABS_VOICE_SIMILARITY,
            #"style": 0.9,
        }
    }
    
    response = requests.post(url, json=data, headers=headers)
    print(response.content)
    with open(output_path, "wb") as output:
        output.write(response.content)
    return output_path


@app.route('/')
def index():
    """Render the index page."""
    return render_template('index.html', voice=ELEVENLABS_VOICE_NAME)


@app.route('/transcribe', methods=['POST'])
def transcribe():
    """Transcribe the given audio to text using Whisper."""
    if 'file' not in request.files:
        return 'No file found', 400
    file = request.files['file']
    recording_file = f"{uuid.uuid4()}.wav"
    recording_path = f"uploads/{recording_file}"
    os.makedirs(os.path.dirname(recording_path), exist_ok=True)
    file.save(recording_path)
    transcription = transcribe_audio(recording_path)
    return jsonify({'text': transcription})


@app.route('/ask', methods=['POST'])
def ask():
    """Generate a ChatGPT response from the given conversation, then convert it to audio using ElevenLabs."""
    conversation = request.get_json(force=True).get("conversation", "")
    reply = generate_reply(conversation)
    reply_file = f"{uuid.uuid4()}.mp3"
    reply_path = f"outputs/{reply_file}"
    os.makedirs(os.path.dirname(reply_path), exist_ok=True)
    generate_audio(reply, output_path=reply_path)
    return jsonify({'text': reply, 'audio': f"/listen/{reply_file}"})


@app.route('/listen/<filename>')
def listen(filename):
    """Return the audio file located at the given filename."""
    return send_file(f"outputs/{filename}", mimetype="audio/mp3", as_attachment=False)


if ELEVENLABS_API_KEY:
    if not ELEVENLABS_ALL_VOICES:
        ELEVENLABS_ALL_VOICES = get_voices()
    if not ELEVENLABS_VOICE_NAME:
        ELEVENLABS_VOICE_NAME = ELEVENLABS_ALL_VOICES[0]["name"]

if __name__ == '__main__':
    app.run()
