import transcriber
import correct_transcriptions
import folder_generation
import yt_download

import threading

import json
from pydub import AudioSegment 

import threading
import time

import os
import shutil


maxThreads = 3
runningThreads = 0

totalThreads = 0

def save_json_file(path, data):
    with open(path, 'w') as json_file:
        text = json.dumps(data)
        json_file.write(text)
        

audio_data_directory = "audio_data"

class transcribeThread(threading.Thread):
    def __init__(self,s_urls,s):
        print("New Thread")
        threading.Thread.__init__(self)
        global runningThreads
        global totalThreads
        totalThreads += 1
        runningThreads += 1
        self.threadID = totalThreads
        self.name = "Thread " + str(self.threadID)
        print("Total Threads: ", runningThreads)
        self.speaker_urls = s_urls
        self.speaker = s
        
    def run(self):
        for speaker_url in speaker_urls:
            
            folders_from_url(speaker_url, speaker)
                            
        print(self.name," is done")
        runningThreads -= 1
        
        

def folders_from_url(yt_url, speaker_dir):
    
    audio_segment = yt_download.download_audio(yt_url)

    # YT video id at end of URl
    audio_id = yt_url[-11:]

    # Make a folder for that individual audio file (url)
    audio_dir = os.path.join(speaker_dir, audio_id) 
    os.mkdir(audio_dir)

    # Save the audio segment / audio to that folder as a .wav file
    audio_file = os.path.join(audio_dir, (audio_id+".wav"))
    audio_segment.export(audio_file, format="wav")
    print("Saved audio file to ", audio_file)

    # Get and save transcriptions
    print("Getting transcriptions...")

    transcriptions = transcriber.get_transcriptions(audio_file)
    transcriptions_json_path = os.path.join(audio_dir, "transcriptions.json")
    save_json_file(transcriptions_json_path, transcriptions)
    print("Got transcriptions")

    # Update the transcriptions to fix some errors with the assembly API
    updated = correct_transcriptions.combine_file(transcriptions_json_path)
    save_json_file(transcriptions_json_path, updated)
    print("Updating transcriptions")

    # Generate folders based of clips from the audio file
    folder_generation.generate_folders(audio_dir,  audio_file, transcriptions_json_path)
    print("Saved folders!") 

            
print("Running")
try:
    shutil.rmtree(audio_data_directory)
    os.mkdir(audio_data_directory)
except:
    os.mkdir(audio_data_directory)
    
with open("urls.json") as json_file:

    urls_json = json.load(json_file)
    
    for speaker in urls_json:

        speaker_urls = urls_json[speaker]

        speaker = os.path.join(audio_data_directory, speaker)
        os.mkdir(speaker)
        while(True):
            if(runningThreads != maxThreads):
                tempThread = transcribeThread(speaker_urls,speaker)
                tempThread.start()
                break;
            else:
                print ("Max Threads reached")
                print ("Trying Again")
                time.sleep(10)
    
    print("DONE, Waiting on Threads Finishing")

