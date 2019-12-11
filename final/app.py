"""
A simple final project flask app.
"""

from datetime import datetime
import logging
import os
import six
from flask import Flask, redirect, render_template, request

from google.cloud import datastore
from google.cloud import storage
from google.cloud import speech
from google.cloud import translate_v2 as translate
from google.cloud import texttospeech

CLOUD_STORAGE_BUCKET = os.environ.get('CLOUD_STORAGE_BUCKET')

app = Flask(__name__)       # our Flask app

"""
Create the endpoint(index.html)
"""
@app.route('/')
def index():
    # Return a Jinja2 HTML template
    return render_template('index.html')

"""
Translate text and store audio file to bucke
"""
@app.route('/trans_text', methods=['GET', 'POST'])
def trans_text():
    # Trans text
    # get text the user entered
    input_text = request.form['text']
    # create Client object
    translate_client = translate.Client()
    # decode text if it's a binary type
    if isinstance(input_text, six.binary_type):
        transcription = transcription.decode('utf-8')
    # get translation result by passing text and target language to client
    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(input_text, target_language='en')
    # only interested in translated text
    translation = result['translatedText']


    # Translated text to speech
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()
    # Set the text input to be synthesized
    synthesis_input = texttospeech.types.SynthesisInput(text=translation)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

    # Select the type of audio file you want returned
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    # Store into bucket
    speech_file = 'output.mp3'
    # Create a Cloud Storage client.
    storage_client = storage.Client()
    # Get the bucket that the file will be uploaded to.
    bucket = storage_client.get_bucket(CLOUD_STORAGE_BUCKET)
    # Create a new blob and upload the file's content.
    blob = bucket.blob(speech_file)
    blob.upload_from_string(response.audio_content, content_type='audio/mpeg')
    # Make the blob publicly viewable.
    blob.make_public()

    #make entries
    entries = [dict(iText=input_text, transText=translation, 
        link= 'https://storage.cloud.google.com/' + CLOUD_STORAGE_BUCKET + '/'+ speech_file)]
    
    # Go to transtext.html.
    return render_template('transtext.html',entries=entries)

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

"""
local host port is 8080
"""
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
