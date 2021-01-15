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
    if(not os.path.isfile("URLs/"+filename)):
        continue

    links = open('URLs/'+filename, 'r')
    title = filename[:-4]
    print("\nprocessing group "+title)
    
    #download videos
    for index,url in enumerate(links):
        url = url.replace("\n", "")
        dir = url[-11:]
        os.system("mkdir out\\Youtube_dataset\\" + dir)
        
        # print("getting video...", end="")
        
        #print("youtube-dl --no-check-certificate -f bestaudio -R \"infinite\" -o \"temp/audio.%(ext)s\" \""+url+"\"")
        os.system("youtube-dl --no-check-certificate -f bestaudio -R \"infinite\" -o \"temp/audio.%(ext)s\" \""+url+"\"")
        
        #   filename = "temp/" + os.listdir("temp")[0]
        #   print("finished downloading (", filename, ")", sep="")
        #remove illegal characters
        for c in "\"\' |&?!()+-*/":
            title = title.replace(c, "")

        # print("converting to wav...", end="")
        #os.system("ffmpeg -i temp/"+title+".webm -c:a pcm_f32le input/"+title+".wav")
        #pydub.AudioSegment.from_file(filename).export("input/"+title+".wav", format="wav")
        # print("finished converting (input/"+title+".webm)")
        ytSuccesses += 1

        # print("splitting...", end="")
        # fileDir = dir + "/" + title + ".wav"
        # subprocess.check_output("ffmpeg -loglevel warning -i "+fileDir+" -ar 16000 -sample_fmt s16 -ac 1 -f segment -segment_time "+str(lengthOfClip)+" -vn -c copy out/"+title+"_%03d.wav", shell=True)
        #command = ['ffmpeg', '-i', fileDir, '-f', 'segment', '-segment_time', '3', 'out/'+title+'%09d.wav']
        #subprocess.run(command,stdout=subprocess.PIPE,stdin=subprocess.PIPE)
        if(os.path.exists("temp/audio.webm")):
            os.system("ffmpeg -loglevel warning -i temp/audio.webm -ar 16000 -sample_fmt s16 -ac 1 -f segment -segment_time "+str(lengthOfClip)+" -vn -af silenceremove=1:0:-42dB out/Youtube_dataset/"+dir+"/"+title+"_"+str(index)+"_%04d.wav")
        elif(os.path.exists("temp/audio.m4a")):
            os.system("ffmpeg -loglevel warning -i temp/audio.m4a -ar 16000 -sample_fmt s16 -ac 1 -f segment -segment_time "+str(lengthOfClip)+" -vn -af silenceremove=1:0:-42dB out/Youtube_dataset/"+dir+"/"+title+"_"+str(index)+"_%04d.wav")
        else:
            print("did not perform ffmpeg")
        # print("finished")
        # print()

        if(os.path.exists("temp/audio.webm")):
            os.remove("temp/audio.webm")
        if(os.path.exists("temp/audio.m4a")):
            os.remove("temp/audio.m4a")

print(ytSuccesses, "Youtube videos successfully downloaded")


