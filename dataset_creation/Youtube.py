
import os
import sys, getopt

listOfUrl = False

def parse(argv):
    length = 3
    url = []
    title = []
    search = "baseball commentary"
    max = 5
    speaker_num = 1
    
    try:
      opts, args = getopt.getopt(argv,"hl:u:t:q:m:s:",["length=","url=","title=","search=","max_results=","speaker="])
    except getopt.GetoptError:
      print ('Youtube.py -l <length> -u <url[s]> -t <title> -q <query> -m <max_results> -s <speaker number>')
      sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
          print ('Youtube.py -l <length> -u <url> -t <title> -q <query> -m <max_results> -s <speaker number>')
          sys.exit()
       elif opt in ("-l", "--length"):
          length = arg
       elif opt in ("-u", "--url"):
          url.append(arg)
          listOfUrl = True
       elif opt in ("-t", "--title"):
          title.append(arg)
       elif opt in ("-q", "--search"):
          search = arg
       elif opt in ("-m", "--max_results"):
          max = arg
       elif opt in ("-s", "--speaker"):
          speaker_num = arg
       return length,url,title,search,max,speaker_num

if(len(sys.argv) >= 2):
   lengthOfClip, url, title, search_query, max_results, speaker = parse(sys.argv[1:])
   lengthOfClip = int(lengthOfClip)
   max_results = int(max_results)
   speaker = int(speaker)
   
else:
   lengthOfClip = 3
   url = ""
   title = ""
   search_query = "baseball commentary"
   max_results = 2
   speaker = 1


#searching for youtube videos
from youtube_search import YoutubeSearch
#downloading youtube audio
os.system("pip3 install youtube-dl pydub pysrt")
#for converting webm to wav
import pydub

import subprocess


#ffmpeg
os.system("brew install ffmpeg")
os.system("pip3 install ffmpeg")

#IO folders
os.system("mkdir out")
os.system("mkdir temp")
#os.system("touch temp/audio.m4a")
#os.system("touch temp/audio.webm")

os.system("mkdir out/Youtube_dataset")


videos = []
#get search results
if(url == ""):
   results = YoutubeSearch(search_query, max_results=max_results).to_dict()
   
   #get links from results
   for video in results:
     url = "youtube.com" + video["url_suffix"]
     title = video["title"]
     duration = video["duration"]
     if(duration.count(":") < 2):  #ensure the files we download are not longer than 59:59
       print("'" + title + "': " + url+" ("+duration+")")
     videos.append((url, title))
   print()

   ytSuccesses = 0
else:
   if(url.len == title.len):
      i = 0
      while(i < url.len):
         videos.append((url.get(i),title.get(i)))
   else:
      videos.append(url.get(i),str(i) + "_video")


#download videos
for url, title in videos:
  if(not listOfUrl):
     dir = "sp"+str(speaker)
  os.system("mkdir out/Youtube_dataset/" + dir)
  speaker += 1
  print("getting video...", end="")
  os.system("youtube-dl -f bestaudio -o \"temp/audio.%(ext)s\" "+url)
  filename = "temp/" + os.listdir("temp")[0]
  print("finished downloading (", filename, ")", sep="")
  #remove illegal characters
  for c in "\"\' |&?!()+-*/":
    title = title.replace(c, "")

  print("converting to wav...", end="")
  #os.system("ffmpeg -i temp/"+title+".webm -c:a pcm_f32le input/"+title+".wav")
  #pydub.AudioSegment.from_file(filename).export("input/"+title+".wav", format="wav")
  print("finished converting (input/"+title+".webm)")
  ytSuccesses += 1

  print("splitting...", end="")
  fileDir = dir + "/" + title + ".wav"
  # subprocess.check_output("ffmpeg -loglevel warning -i "+fileDir+" -ar 16000 -sample_fmt s16 -ac 1 -f segment -segment_time "+str(lengthOfClip)+" -vn -c copy out/"+title+"_%03d.wav", shell=True)
  #command = ['ffmpeg', '-i', fileDir, '-f', 'segment', '-segment_time', '3', 'out/'+title+'%09d.wav']
  #subprocess.run(command,stdout=subprocess.PIPE,stdin=subprocess.PIPE)
  os.system("ffmpeg -loglevel warning -i temp/audio.webm -ar 16000 -sample_fmt s16 -ac 1 -f segment -segment_time "+str(lengthOfClip)+" -vn out/Youtube_dataset/"+dir+"/"+title+"_%03d.wav")
  print("finished")
  print()
  
  #os.remove(filename)

print(ytSuccesses, "Youtube videos successfully downloaded")


