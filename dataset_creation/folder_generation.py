# Splits up the audio files into folders based of sentences in the subtitles
import os
from pydub import AudioSegment
import json
import random



def split_segment(segment, start, end):
    new_segment = segment[start:end]
    return new_segment


def save_data(training_directory, audio_segment, start, end, text, serialno):
    id = str(serialno) + "_" + str(start) + "_" + str(end)

    folder_path = os.path.join(training_directory, id)
    os.mkdir(folder_path)

    audio_path = os.path.join(folder_path, id + "_" + "audio_temp.wav")
    audio_segment.export(audio_path, format='wav')

    subtitles_path = os.path.join(folder_path, id + "_subtitles.txt")
    subtitles = open(subtitles_path, "w")
    subtitles.write(text)
    subtitles.close()


def generate_folders(training_data_directory, audio_path, json_path):
    audio_file = AudioSegment.from_wav(audio_path)

    json_file = open(json_path)
    json_data = json.load(json_file)
    sentences = json_data['sentences']

    # os.mkdir(training_data_directory)

    i = 0

    while i < len(sentences):
        sentence = sentences[i]
        start = sentence['start']
        end = sentence['end']
        text = sentence['text']

        segment = split_segment(audio_file, start, end)

        # 2/3 of the sentences will be combined
        if random.random() < 0.66 and i < len(sentences) - 2:
            sentence_2 = sentences[i+1]
            start2 = sentence_2['start']
            end2 = sentence_2['end']
            text2 = sentence_2['text']
            segment2 = split_segment(audio_file, start2, end2)
            segment += AudioSegment.silent(duration=150)
            segment += segment2
            text += " " + text2
            i += 1

        save_data(training_data_directory, segment, start, end2, text, i)
        i += 1


if __name__ == "__main__":
    data_dir_name = "data"
    audio_file = "transcriber_test.wav"
    json_file = "updated.json"
    generate_folders(data_dir_name, audio_file, json_file)
