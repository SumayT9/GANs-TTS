import os
#os.system("pip3 install youtube-dl pydub pysrt")

#ffmpeg
#os.system("brew install ffmpeg")
#os.system("pip3 install ffmpeg")

#IO folders
os.system("mkdir out")
os.system("mkdir temp")
os.system("mkdir content")
os.system("mkdir out/Youtube_dataset")

import pydub
import subprocess
import speech_recognition as sr
import sys, getopt
from youtube_search import YoutubeSearch

lengthOfClip = 3
ytSuccesses = 0

for filename in os.listdir('URLs'):
    if(not os.path.isfile("URLs/"+filename)):
        continue

    links = open('URLs/'+filename, 'r')
    title = filename[:-4]
    #remove illegal characters
    for c in "\"\' |&?!()+-*/":
        title = title.replace(c, "")
    dir = title
    os.system("mkdir out/Youtube_dataset/" + dir)
    
    #download videos
    for url in links:
        
        url = url.replace("\n", "")
        os.system("youtube-dl --no-check-certificate -f bestaudio -o \"temp/audio.%(ext)s\" \""+url+"\"")
        for c in "\"\' |&?!()+-*/":
            title = title.replace(c, "")
        ytSuccesses += 1

        if(os.path.exists("temp/audio.webm")):  #sometimes files are downloaded as m4a files
            os.system("ffmpeg -loglevel warning -i temp/audio.webm -ar 16000 -sample_fmt s16 -ac 1 -vn temp/" + title + ".wav") #saves as .wav
        elif(os.path.exists("temp/audio.m4a")):
            os.system("ffmpeg -loglevel warning -i temp/audio.m4a -ar 16000 -sample_fmt s16 -ac 1 -vn temp/" + title + ".wav") #saves as .wav
        
        
        filename = "temp/" + title + ".wav"
        os.system("ffmpeg -i " + filename + " -af silencedetect=noise=-30dB:d=0.2 -f null - 2> vol.txt") #CHANGE SILENCE TIME AT: d=
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
                    os.system("ffmpeg -f wav -ss " + str(time) + " -i " + filename + " -t " + str(temp) + " -c copy out/Youtube_dataset/" + dir + "/" + title + "_" + str(clip) + ".wav")
                    time = text[1]
                    clip += 1
            except:
                print("no silence")
                os.system("ffmpeg -f wav -i " + filename + " -c copy out/Youtube_dataset/" + dir + "/" + title + "_" + str(clip) + ".wav")
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
                    
                os.system("ffmpeg -loglevel warning -ss " + str(time) + " -i " + filename + " -t " + str(temp) + " -c copy out/Youtube_dataset/" + dir + "/" + title + "_" + str(clip) + ".wav")
                i += 3
                print("len:" + str(temp))
                totalTime += temp
                try:
                    time = text[i]
                except:
                    print("exited loop")
                print("Cut")
                recog = sr.Recognizer()
                with sr.AudioFile("out/Youtube_dataset/" + dir + "/" + title + "_" + str(clip) + ".wav") as source:
                    audio = recog.record(source) #read entire audio file
                try:
                    output = recog.recognize_sphinx(audio)
                    file = open("content/" + title + "_" + str(clip) + " captions.txt", "w")
                    file.write(output)
                    file.close()
                    print("", "content/" + title + "_" + str(clip) + " captions.txt", " generated", sep="\"")
                except sr.UnknownValueError:
                    print("Sphinx could not understand audio")
                except sr.RequestError as e:
                    print("Sphinx error; {0}".format(e))
                except Exception as e:
                    print("--------------------")
                    print("An exception occured")
                    print(e)
                    print(sys.exc_info())
                    print(sys.exc_info()[2].tb_lineno)
                clip += 1
            print("\n------------------------------------\n")
            print("Total Clips:" + str(clip))
            print("Avg Time: " + str(totalTime/clip))
            print("Done!")
                
        if(os.path.exists("temp/audio.webm")):
            os.remove("temp/audio.webm")
        if(os.path.exists("temp/audio.m4a")):
            os.remove("temp/audio.m4a")
        
        
print(ytSuccesses, "Youtube videos successfully downloaded")
