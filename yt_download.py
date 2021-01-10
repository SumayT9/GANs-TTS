import os
os.system("pip3 install youtube-dl pydub pysrt")

#ffmpeg
os.system("brew install ffmpeg")
os.system("pip3 install ffmpeg")

#IO folders
os.system("mkdir out")
os.system("mkdir temp")
os.system("mkdir out\\Youtube_dataset")

import pydub
import subprocess
import os
import sys, getopt
from youtube_search import YoutubeSearch

lengthOfClip = 3
ytSuccesses = 0

for filename in os.listdir('URLs'):
    links = open('URLs/'+filename, 'r')
    title = filename[:-4]
    dir = title
    os.system("mkdir out\\Youtube_dataset\\" + dir)
    
    #download videos
    for url in links:
        
        os.system("youtube-dl --no-check-certificate -f bestaudio -o \"temp/audio.%(ext)s\" \""+url+"\"")
        for c in "\"\' |&?!()+-*/":
            title = title.replace(c, "")
        ytSuccesses += 1

        os.system("ffmpeg -loglevel warning -i temp/audio.webm -ar 16000 -sample_fmt s16 -ac 1 -c copy temp/" + title + ".wav") #saves as .wav
        
        
        file = "temp/" + title + ".wav"
        os.system("ffmpeg -i " + file + " -af silencedetect=noise=-30dB:d=0.3 -f null - 2> vol.txt") #CHANGE SILENCE TIME AT: d=
        with open('vol.txt', 'r+') as temp:
            text = temp.read()
            text = text.replace('silence_start: ','split')
            text = text.replace('silence_end: ','split')
            text = text.replace('| silence_duration: ','split')
            text = text.replace('\n[silencedetect @','split')
            text = text.replace('\nsize','split')
            text = text.split('split')
            text = text[1:]
            print("Trimming")
            i = 0
            while i < len(text):
                if "x" in text[i]: #0x564b3cb09040 acts strange as a srting idk why
                    text.remove(text[i])
                elif "-" in text[i]:
                    text[i] = "0.0"
                    i += 1
                else:
                    i += 1
            print(text)
            i = 1
            clip = 0
            try:
                if text[0] == 0.0:
                    time = text[1]
                else:
                    time = 0.0
                    temp = float(text[0])
                    os.system("ffmpeg -loglevel warning -ss " + str(time) + " -i " + file + " -t " + str(temp) + " -c copy out/Youtube_dataset/" + dir + file[6:len(file)-4] + "_" + str(clip) + ".wav")
                    time = text[1]
                    clip += 1
            except:
                print("no silence")
                os.system("ffmpeg -loglevel warning -i " + file + " -c copy out/Youtube_dataset/" + dir + file[6:len(file)-4] + "_" + str(clip) + ".wav")
            while i < len(text):
                j = 2
                temp = float(text[i+j]) - float(time)
                #Un-comment to add min time (Not fully tested)
                    #while (temp < 3) & (i+j < len(text)): #CHANGE MIN TIME HERE
                    #j += 2
                    #temp = float(text[i+j]) - float(time)
                os.system("ffmpeg -loglevel warning -ss " + str(time) + " -i " + file + " -t " + str(temp) + " -c copy out/Youtube_dataset/" + dir + file[6:len(file)-4] + "_" + str(clip) + ".wav")
                i += 3
                try:
                    time = text[i]
                except:
                    print("exit loop")
                clip += 1
                print("Cut")
            print("Done!")
        
        
print(ytSuccesses, "Youtube videos successfully downloaded")


