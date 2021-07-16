import os
import shutil
import json

from pydub import AudioSegment

try:
    shutil.rmtree("download_output")
    os.mkdir("download_output")
except:
    os.mkdir("download_output")

def download_audio(url,speaker):

    print("")
    print("")
    print("")
    print("SPEAKER: " + speaker)
    print("URL: " + url)
    print("AAAAAAA: " + "youtube-dl --no-check-certificate -f bestaudio -o \"download_output/" + speaker + ".webm\" \""+url+"\"")
    print("")
    print("")
    print("")
    
    os.system("youtube-dl --no-check-certificate -f bestaudio -o \"download_output/" + speaker + ".webm\" \""+url+"\"")

    
    audio = None

    # Saveas m4a
    audio = AudioSegment.from_file("download_output/" + speaker + ".webm")
                    
    # delete the m4a
    os.remove("download_output/" + speaker + ".webm")
                
    return audio
    

# testing
