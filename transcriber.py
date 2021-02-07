import sys
import time
import os
import requests
import json
import const

# reads audio files
api_key = const.api_key #put your own key

def read_file(filename, chunk_size=5242880):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data

# uploads file to API
def upload(filename, new_key=api_key):
    headers_upload = {'authorization': new_key}
    response_upload = requests.post('https://api.assemblyai.com/v2/upload',
                                    headers=headers_upload,
                                    data=read_file(filename))

    return response_upload.json()

# Transcribes audio
def transcribe(endpoint, response_upload, new_key=api_key):
    json_transcription = {
        "audio_url": response_upload["upload_url"],
        "language_model": "assemblyai_media"
    }
    headers_transcription = {
        "authorization": api_key,
        "content-type": "application/json"
    }

    # Sending video for transcription
    response_transcription = requests.post(endpoint, json=json_transcription, headers=headers_transcription)
    response = response_transcription.json()

    # making get requests until the transcription is finished
    while response['status'] != 'completed':
        endpoint_get = "https://api.assemblyai.com/v2/transcript/" + response['id']
        headers = {
            "authorization": api_key,
        }
        response = requests.get(endpoint_get, headers=headers)
        try:
            response = response.json()
            print(response['status'])
        except AttributeError:
            pass

    return response








if __name__ == '__main__':
    # looping through audio files
    api_key = "39a86dbe224549e08e16178bffd9bf3a"
    for audio_file in os.listdir('tts-model/sampleAudios'):
        if audio_file.endswith('.wav'):
            filename = "tts-model/sampleAudios/" + audio_file
            read_file(filename, chunk_size=5242880)

            # uploading file to API
            response_upload = upload(filename, api_key)

            # where the transcript will be located
            endpoint = "https://api.assemblyai.com/v2/transcript"

            # preparing to transcribe the audio
            response = transcribe(endpoint, response_upload, api_key)

            # writing transcript to transcript file
            with open('assembly_output/transcripts.txt', 'a') as transcript_file:
                transcript_file.write(audio_file + " | " + response['text'] + "\n")

            # writing complete json to a json file
            with open('assembly_output/' + audio_file[:-4] + '.json', 'w') as json_file:
                text = json.dumps(response)
                json_file.write(text)

            print('file ' + audio_file + 'done!')
