#!/usr/bin/env python

# Copyright 2018 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import redirect, request, url_for, render_template
from flask.views import MethodView

import argparse
from google.cloud import vision
from google.cloud import speech
from google.cloud import translate
from google.cloud import language
from google.cloud.language import enums
import six


class Transvoice(MethodView):
    def get(self):
        return render_template('transvoice.html')

    def post(self):

        def transcribe_gcs(language, gcs_uri):
            """Transcribes the audio file specified by the gcs_uri."""

            # create ImageAnnotatorClient object
            client = speech.SpeechClient()

            # specify location of speech
            audio = speech.types.RecognitionAudio(uri=gcs_uri) # need to specify speech.types

            # set language to Turkish
            # removed encoding and sample_rate_hertz
            config = speech.types.RecognitionConfig(language_code=language) # need to specify speech.types

            # get response by passing config and audio settings to client
            response = client.recognize(config, audio)

            # naive assumption that audio file is short
            return response.results[0].alternatives[0].transcript

        def translate_text(target, text):
            """Translates text into the target language.
            Target must be an ISO 639-1 language code.
            See https://g.co/cloud/translate/v2/translate-reference#supported_languages
            """

            # create Client object
            translate_client = translate.Client()

            # decode text if it's a binary type
            if isinstance(text, six.binary_type):
                text = text.decode('utf-8')

            # get translation result by passing text and target language to client
            # Text can also be a sequence of strings, in which case this method
            # will return a sequence of results for each text.
            result = translate_client.translate(text, target_language=target)

            # only interested in translated text
            return result['translatedText']

        def compare_audio_to_image(language, audio):
            """Checks whether a speech audio is relevant to an image."""

            # speech audio -> text
            transcription = transcribe_gcs(language, audio)

            # text of any language -> english text
            translation = translate_text('en', transcription)

        parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument(
            'language', help='Language code of speech audio')
        parser.add_argument(
            'audio', help='GCS path for audio file to be recognised')
        args = parser.parse_args()
        compare_audio_to_image(args.language, args.audio)