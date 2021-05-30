import os
import shutil
import json
from pydub import AudioSegment

try:
    shutil.rmtree("download_output")
    os.mkdir("download_output")
except:
    os.mkdir("download_output")

def download_audio(url):

    os.system("youtube-dl --no-check-certificate -f bestaudio -o \"download_output/audio_temp.%(ext)s\" \""+url+"\"")

    
    audio = None
    try:

        # Save as m4a
        audio = AudioSegment.from_file("download_output/audio_temp.m4a")
        # delete the m4a
        os.remove("download_output/audio_temp.m4a")
    except:
        # Convert webm to wav
        os.system("ffmpeg -loglevel warning -i download_output/audio_temp.webm -ar 16000 -sample_fmt s16 -ac 1 -vn download_output/" + "audio_temp" + ".wav") #saves as .wav
        
        # Save wav as audiosegment
        audio = AudioSegment.from_file("download_output/audio_temp.wav")
        
        # Delete webm
        os.remove("download_output/audio_temp.webm")
    
        # Delete wav
        os.remove("download_output/audio_temp.wav")
    
    return audio
    

# testing
