import os

#searching for youtube videos
from youtube_search import YoutubeSearch
#downloading youtube audio
os.system("pip install youtube-dl pydub pysrt")
#for converting webm to wav
import pydub

#ffmpeg
os.system("brew install ffmpeg")
os.system("pip install ffmpeg")

#IO folders
os.system("mkdir input")
os.system("mkdir out")
os.system("mkdir temp")

import os
import subprocess



#variables
search_query = "baseball commentary" #@param {type: "string"}
max_results = 30 #@param {type: "integer"}

lengthOfClip = 3 #@param{type:"integer"}



#get search results
results = YoutubeSearch(search_query, max_results=max_results).to_dict()

#get links from results
videos = []
for video in results:
  url = "youtube.com" + video["url_suffix"]
  title = video["title"]
  duration = video["duration"]
  if(duration.count(":") < 2):  #ensure the files we download are not longer than 59:59
    print("'" + title + "': " + url+" ("+duration+")")
  videos.append((url, title))
print()

ytSuccesses = 0

#download videos
for url, title in videos:
  
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
  fileDir = "input/" + title + ".wav"
  # subprocess.check_output("ffmpeg -loglevel warning -i "+fileDir+" -ar 16000 -sample_fmt s16 -ac 1 -f segment -segment_time "+str(lengthOfClip)+" -vn -c copy out/"+title+"_%03d.wav", shell=True)
  #command = ['ffmpeg', '-i', fileDir, '-f', 'segment', '-segment_time', '3', 'out/'+title+'%09d.wav']
  #subprocess.run(command,stdout=subprocess.PIPE,stdin=subprocess.PIPE)
  os.system("ffmpeg -loglevel warning -i temp/audio.webm -ar 16000 -sample_fmt s16 -ac 1 -f segment -segment_time "+str(lengthOfClip)+" -vn out/"+title+"_%03d.wav")
  print("finished")
  print()
  #os.remove(filename)

print(ytSuccesses, "Youtube videos successfully downloaded")
