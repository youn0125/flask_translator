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

CLOUD_STORAGE_BUCKET = os.environ.get('CLOUD_STORAGE_BUCKET')

app = Flask(__name__)       # our Flask app

"""
Create the endpoint(index.html)
"""
@app.route('/')
def index():
    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()

    # Use the Cloud Datastore client to fetch information from Datastore about
    # each photo.
    query = datastore_client.query(kind='Speech')
    audio_entities = list(query.fetch())

    # Return a Jinja2 HTML template and pass in image_entities as a parameter.
    return render_template('index.html', audio_entities=audio_entities)

@app.route('/upload_speech', methods=['GET', 'POST'])
def upload_speech():
    #upload file to bucket

    speech_file = request.files['file']

    storage_client = storage.Client()
   
    bucket = storage_client.get_bucket(CLOUD_STORAGE_BUCKET)

    blob = bucket.blob(speech_file.filename)
   
    blob.upload_from_string(speech_file.read(), content_type=speech_file.content_type)

    blob.make_public()

    source_uri = 'gs://{}/{}'.format(CLOUD_STORAGE_BUCKET, blob.name)

    datastore_client = datastore.Client()

    current_datetime = datetime.now()

    kind = 'Speech'

    name = blob.name

    key = datastore_client.key(kind, name)

    entity = datastore.Entity(key)
    entity['blob_name'] = blob.name
    entity['audio_public_url'] = blob.public_url
    entity['timestamp'] = current_datetime

    datastore_client.put(entity)


    # speech to text

    client = speech.SpeechClient()
    
    # specify location of speech
    audio = speech.types.RecognitionAudio(uri=source_uri) # need to specify speech.types

    # set language to Turkish
    # removed encoding and sample_rate_hertz
    config = speech.types.RecognitionConfig(language_code='tr-TR') # need to specify speech.types

    # get response by passing config and audio settings to client
    response = client.recognize(config, audio)
    
    #get transcription
    transcription = response.results[0].alternatives[0].transcript

    print("Transcription: " + transcription)
    
    # create Client object
    translate_client = translate.Client()

    # decode text if it's a binary type
    if isinstance(transcription, six.binary_type):
        transcription = transcription.decode('utf-8')

    # get translation result by passing text and target language to client
    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(transcription, target_language='en')

    # only interested in translated text
    translation = result['translatedText']

    print(u'Text: {}'.format(result['input']))
    print(u'Translation: {}'.format(result['translatedText']))
    print(u'Detected source language: {}'.format(
        result['detectedSourceLanguage']))
    
    return redirect('/')

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
