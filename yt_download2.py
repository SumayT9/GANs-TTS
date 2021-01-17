import os
from os import path
import json
#os.system("pip3 install youtube-dl pydub pysrt")


#IO folders
os.system("mkdir out")
os.system("mkdir temp")
os.system("mkdir out/Youtube_dataset")

import pydub
import subprocess
import sys, getopt
from youtube_search import YoutubeSearch

lengthOfClip = 3
ytSuccesses = 0

for filename in os.listdir('URLs'):
    if(not os.path.isfile("URLs/"+filename)):
        continue

    links = open('URLs/'+filename, 'r')
    name = filename[:-4]
    for c in "\"\' |&?!()+-*/":
        name = name.replace(c, "")
    dir = name
    os.system("mkdir out/Youtube_dataset/" + dir)

    titleNum = 0;

    #download videos
    for url in links:
        title = name + "_" + str(titleNum)
        titleNum += 1
        subdir = title

        os.system("youtube-dl --no-check-certificate -f bestaudio -o \"temp/audio.%(ext)s\" \""+url+"\"")
        ytSuccesses += 1
        if(path.exists("temp/audio.webm")):
            os.system("ffmpeg -loglevel warning -i temp/audio.webm -ar 16000 -sample_fmt s16 -ac 1 -vn temp/" + title + ".wav") #saves as .wav
        elif(path.exists("temp/audio.webm")):
            os.system("ffmpeg -loglevel warning -i temp/audio.m4a -ar 16000 -sample_fmt s16 -ac 1 -vn temp/" + title + ".wav") #saves as .wav
        else:
            continue


        os.system("mkdir out/Youtube_dataset/"+dir+"/"+subdir)
        
        file = "temp/" + title + ".wav"
        os.system("ffmpeg -i " + file + " -af silencedetect=noise=-30dB:d=0.2 -f null - 2> vol.txt") #CHANGE SILENCE TIME AT: d=
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
            i = 1
            clip = 0
            try:
                if text[0] == 0.0:
                    time = text[1]
                else:
                    time = 0.0
                    temp = float(text[0])
                    os.system("ffmpeg -loglevel warning -ss " + str(time) + " -i " + file + " -t " + str(temp) + " -c copy out/Youtube_dataset/" + dir + "/" + subdir + "/" + title + "_" + str(clip) + ".wav")
                    time = text[1]
                    clip += 1
            except:
                print("no silence")
                os.system("ffmpeg -loglevel warning -i " + file + " -c copy out/Youtube_dataset/" + dir + "/" + subdir + "/" + title + "_" + str(clip) + ".wav")
            totalTime = 0;
            while i < len(text):
                j = 2
                try:
                    temp = float(text[i+j]) - float(time)
                    while (temp < 5) & (i+j < len(text)): #CHANGE MIN TIME HERE
                        j += 3
                        temp = float(text[i+j]) - float(time)
                    i += (j - 2)
                    j = 2
                except:
                    print("error") #Fix later not a huge issue just might lose one clip per video in worst case
                    break;
                    
                os.system("ffmpeg -loglevel warning -ss " + str(time) + " -i " + file + " -t " + str(temp) + " -c copy out/Youtube_dataset/" + dir + "/" + subdir + "/" + title + "_" + str(clip) + ".wav")
                i += 3
                print("len:" + str(temp))
                totalTime += temp
                try:
                    time = text[i]
                except:
                    print("exited loop")
                print("Cut")
                #Change name to your user name
        
                os.system("autosub -F json out/Youtube_dataset/" + dir + "/" + subdir + "/" + title + "_" + str(clip) + ".wav")
                with open("out/Youtube_dataset/" + dir + "/" + subdir + "/" + title + "_" + str(clip) + ".json") as J:
                    data = json.load(J)
                    with open("out/Youtube_dataset/" + dir + "/" + subdir + "/" + title + ".txt","a+") as txt:
                        txt.write(title + "_" + str(clip) + ".wav | ")
                        for content in data:
                            txt.write(content['content'])
                            txt.write(" ")
                        txt.write("\r\n")
                os.remove("out/Youtube_dataset/" + dir + "/" + subdir + "/" + title + "_" + str(clip) + ".json")



                clip += 1
            print("\n------------------------------------\n")
            print("Total Clips:" + str(clip))
            print("Avg Time: " + str(totalTime/clip))
            print("Done!")
            if(path.exists("temp/audio.webm")):
                os.remove("temp/audio.webm")
            else:
                os.remove("temp/audio.m4a")
                
        
        
print(ytSuccesses, "Youtube videos successfully downloaded")

