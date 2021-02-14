import os
import json
os.system("pip3 install youtube-dl pydub pysrt")


#IO folders
os.system("mkdir out")
os.system("mkdir temp")
os.system("mkdir content")
os.system("mkdir out/Youtube_dataset")

import pydub
import subprocess
import sys, getopt
from youtube_search import YoutubeSearch

import transcriber

import threading
import time

lengthOfClip = 3
ytSuccesses = 0
totalSeconds = 0

threads = 0
runningThreads = 0

class transcribeThread(threading.Thread):
    def __init__(self,numThreads,dir,title):
        print("Thread being made")
        global runningThreads
        threading.Thread.__init__(self)
        self.threadID = numThreads
        self.name = "Thread " + str(self.threadID)
        runningThreads += 1
        self.dir = dir
        self.title = title
    def run(self):
        print(self.name + " is running")
        #try:
        global runningThreads
        transcriber.read_file(dir)
        response_upload = transcriber.upload(dir)
        response_transcription = transcriber.transcribe(response_upload,labels=True)
        utterences = transcriber.find_speakers(response_transcription)
        numClips = 0
        txt = open("out/Youtube_dataset/" + self.title[:-2] + "/" + self.title + ".txt","a+")
        for clip in utterences:
            txt.write(self.title + "_" + str(numClips) + ".wav | ")
            txt.write(str(clip[2]))
            txt.write("\r\n")
            os.system("ffmpeg -loglevel warning -ss " + str(int(clip[0])/1000) + " -i temp/" + self.title + ".wav" + " -t " + str((int(clip[1])-int(clip[0]))/1000) + " -c copy out/Youtube_dataset/" + self.title[:-2] + "/" + self.title + "_" + str(numClips) + ".wav")
            numClips += 1
        print("Done with " + self.name)
        runningThreads -= 1
        #except:
           #print("error in thread, retrying")
           #self.run()
    
        

for filename in os.listdir('URLs'):
    if(not(os.path.isfile(filename))):
        continue
    links = open('URLs/'+filename, 'r')
    title = filename[:-4]
    os.system("mkdir out/Youtube_dataset/" + title)
    titleNum = 0;
    #download videos
    for url in links:
            
        title = title + "_" + str(titleNum)
        os.system("youtube-dl --no-check-certificate -f bestaudio -o \"temp/audio.%(ext)s\" \""+url+"\"")
        for c in "\"\' |&?!()+-*/":
            title = title.replace(c, "")
        ytSuccesses += 1
        try:
            os.system("ffmpeg -loglevel warning -i temp/audio.webm -ar 16000 -sample_fmt s16 -ac 1 -vn temp/" + title + ".wav") #saves as .wav
        except:
            os.system("ffmpeg -loglevel warning -i temp/audio.m4a -ar 16000 -sample_fmt s16 -ac 1 -vn temp/" + title + ".wav") #saves as .wav
        
        
      
                    #os.system("ffmpeg -loglevel warning -ss " + str(time) + " -i " + file + " -t " + str(temp) + " -c copy out/Youtube_dataset/" + dir + "/" + title + "_" + str(clip) + ".wav")
        print("Thread made")
       
        dir = "temp/" + title + ".wav"
        tempThread = transcribeThread(threads,dir,title)
        title = title[:-2]
        titleNum += 1
        threads += 1
        tempThread.start()
        
            
            
        #print("\n------------------------------------\n")
        #print("Total Clips:" + str(clip))
        #print("Avg Time: " + str(totalTime/clip))
        #print("Done!")
        #totalSeconds += totalTime
                


print(ytSuccesses, "Youtube videos successfully downloaded")
print("Threads are being finished")
trys = 0
while(runningThreads != 0):
    trys += 1
    print(str(runningThreads))
    time.sleep(10)
print(str(trys) + " calls to finish")


