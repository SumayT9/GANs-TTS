import time
import requests
import json
import const

api_key = const.get_api_key()

# reads audio files
def read_file(filename, chunk_size=5242880):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data


# uploads file to API
def upload(filename, key=api_key):
    print(filename)
    headers_upload = {'authorization': key}
    response_upload = requests.post('https://api.assemblyai.com/v2/upload',
                                    headers=headers_upload,
                                    data=read_file(filename))

    return response_upload.json()


# Transcribes audio
def transcribe(response_upload, key=api_key, endpoint="https://api.assemblyai.com/v2/transcript", labels=False):
    json_transcription = {
        "audio_url": response_upload["upload_url"],
        "language_model": "assemblyai_media",
        "speaker_labels": labels,
        "punctuate": False,
        "format_text": False
    }
    
    headers_transcription = {
        "authorization": key,
        "content-type": "application/json"
    }

    # Sending video for transcription
    print("attempting to get transcribe")
    response_transcription = requests.post(endpoint, json=json_transcription, headers=headers_transcription)
    response = response_transcription.json()

    # making get requests until the transcription is finished
    
    while response['status'] != 'completed':
        endpoint_get = "https://api.assemblyai.com/v2/transcript/" + response['id']
        headers = {
            "authorization": key,
        }
        response = requests.get(endpoint_get, headers=headers)
        try:
            response = response.json()
            print(response['status'])
        except AttributeError:
            pass
        time.sleep(1)
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
