import sys
import time
import os
import requests
import json


# reads audio files
def read_file(filename, chunk_size=5242880):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data


# uploads file to API
def upload(filename, api_key):
    headers_upload = {'authorization': api_key}
    response_upload = requests.post('https://api.assemblyai.com/v2/upload',
                                    headers=headers_upload,
                                    data=read_file(filename))

    return response_upload.json()


# Transcribes audio
def transcribe(response_upload, api_key, endpoint="https://api.assemblyai.com/v2/transcript", labels=False):
    json_transcription = {
        "audio_url": response_upload["upload_url"],
        "language_model": "assemblyai_media",
        "speaker_labels": labels
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

# extracts speakers and respective utterances for speaker diarization
def find_speakers(response):
    speakers = {}
    clip_lengths = {}
    for utterance in response["utterances"]:
        if utterance["speaker"] in speakers:
            speakers[utterance["speaker"]].append([utterance["start"], utterance["end"], utterance["text"]])
            clip_lengths[utterance["speaker"]] += (utterance["end"] - utterance["start"])
        else:
            speakers[utterance["speaker"]] = [[utterance["start"], utterance["end"], utterance["text"]]]
            clip_lengths[utterance["speaker"]] = (utterance["end"] - utterance["start"])

    # find the primary speaker
    max_len = 0
    for speaker in list(clip_lengths.keys()):
        if clip_lengths[speaker] < max_len:
            del clip_lengths[speaker]
        else:
            max_len = clip_lengths[speaker]

    return speakers[list(clip_lengths.keys())[0]]

# writes transcript to file
def write_file(audio_file_name, path, response):
    with open(path, 'a') as transcript_file:
        transcript_file.write(audio_file_name + " | " + response['text'] + "\n")

# writes transcript file
def write_file_wlabels(audio_file_name, speaker_dict):
    with open('assembly_output/transcripts_2.txt', 'a') as transcript_file:
        pass



def save_json(audio_file_name, response):
    # writing complete json to a json file
    with open('assembly_output/' + audio_file_name[:-4] + '_2.json', 'w') as json_file:
        text = json.dumps(response)
        json_file.write(text)


if __name__ == '__main__':
    # looping through audio files
    api_key = "39a86dbe224549e08e16178bffd9bf3a"
    labels = False
    for audio_file in os.listdir('tts-model/sampleAudios'):
        if audio_file.endswith('.wav'):
            filename = "tts-model/sampleAudios/" + audio_file
            read_file(filename, chunk_size=5242880)

            # uploading file to API
            response_upload = upload(filename, api_key)

            # where the transcript will be located
            endpoint = "https://api.assemblyai.com/v2/transcript"

            # transcribing the audio
            response = transcribe(response_upload, api_key, endpoint=endpoint, labels=labels)

            # use only for speaker labels
            if labels:
                speakers = find_speakers(response)


            # writing transcript to transcript file
            if labels:
                write_file_wlabels(audio_file, speakers)
            else:
                write_file(audio_file, 'assembly_output/transcripts.txt', response)

            # writing complete json to a json file
            save_json(audio_file, response)

            print('file ' + audio_file + 'done!')
