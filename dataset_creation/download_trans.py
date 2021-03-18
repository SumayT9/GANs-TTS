import os
from os import path
from dataset_creation import transcriber
from pydub import AudioSegment

# os.system("pip3 install youtube-dl pydub pysrt")


# IO folders
os.system("mkdir out")
os.system("mkdir temp")
os.system("mkdir out/Youtube_dataset")


lengthOfClip = 3
ytSuccesses = 0

# for some reason, I was having trouble with the commands, so I reference the one specifically from
py37prefix = ""
if (True):
    py37prefix = "python3 -m "

for filename in os.listdir('../URLs'):
    if (not os.path.isfile("URLs/" + filename)):
        continue

    links = open('URLs/' + filename, 'r')
    name = filename[:-4]
    for c in "\"\' |&?!()+-*/":
        name = name.replace(c, "")
    dir = name
    os.system("mkdir out/Youtube_dataset/" + dir)
    print("\nProcessing " + dir + "...")

    titleNum = 0;

    # download videos
    for url in links:
        title = name + "_" + str(titleNum)
        titleNum += 1
        subdir = title
        print("processing " + title + "...")

        # os.system("youtube-dl --no-check-certificate -f bestaudio -o \"temp/audio.%(ext)s\" \""+url+"\"")
        os.system(
            py37prefix + "youtube_dl --no-check-certificate -f bestaudio -o \"temp/audio.%(ext)s\" \"" + url + "\"")
        ytSuccesses += 1
        if (path.exists("temp/audio.webm")):
            os.system(
                "ffmpeg -loglevel warning -i temp/audio.webm -ar 16000 -sample_fmt s16 -ac 1 -vn temp/" + title + ".wav")  # saves as .wav
        elif (path.exists("temp/audio.m4a")):
            os.system(
                "ffmpeg -loglevel warning -i temp/audio.m4a -ar 16000 -sample_fmt s16 -ac 1 -vn temp/" + title + ".wav")  # saves as .wav
        else:
            continue

        os.system("mkdir out/Youtube_dataset/" + dir + "/" + subdir)

        # transcribing the video to get videos with one speaker (first transcription)
        api_key = const.get_api_key()
        transcriber.read_file("temp/" + title + ".wav")
        response_upload = transcriber.upload("temp/" + title + ".wav", api_key)
        response = transcriber.transcribe(response_upload, api_key, labels=True)
        speaker_times = transcriber.find_speakers(response)

        # video_count
        count = 0

        # name of the file
        file = "temp/" + title + ".wav"
        vid = AudioSegment.from_wav(file)
        for speaker_time in  speaker_times:

            # split clip based on times
            start = speaker_time[0]
            end = speaker_time[1]
            ''' here we have to split, after we perform these 
            splits then we might need to trim for time, unsure though-we have to see how it turns out'''

            # splitting the file
            clip = vid[start:end]
            # unfamiliar with the exact structure of the dataset, but fill this in so it extracts to the correct location
            clip.export("youtube_dataset/" + title + "_" + count + ".wav", format="wav")

            '''after this we run the transcriber to transcribe the vid one final time'''

            #loop through files in a subdirectory of the dataset
            transcriber.read_file('''insert_filepath_here''')
            response_upload = transcriber.upload('''insert same filepath here''', api_key)
            response_transcription = transcriber.transcribe(response_upload, api_key, labels=False)
            transcriber.write_file('''name_of_file''', '''path of transcript''', response_transcription)

            '''file should be transcribed and downloaded here'''

            if (path.exists("temp/audio.webm")):
                os.remove("temp/audio.webm")
            if (path.exists("temp/audio.m4a")):
                os.remove("temp/audio.m4a")

print(ytSuccesses, "Youtube videos successfully downloaded")

