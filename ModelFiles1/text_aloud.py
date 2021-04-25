'''from encoder.params_model import model_embedding_size as speaker_embedding_size
from utils.argutils import print_args
from utils.modelutils import check_model_paths'''
from synthesizer.inference import Synthesizer
from encoder import inference as encoder
from vocoder import inference as vocoder
from pathlib import Path
import numpy as np
'''import soundfile as sf
import librosa
import argparse
import torch
import sys
from audioread.exceptions import NoBackendError'''
import sounddevice as sd
from torch import multiprocessing
import time


def generate_embedding():
    in_fpath = "data/Miller_2.wav"
    ## Computing the embedding
    # First, we load the wav using the function that the speaker encoder provides. This is
    # important: there is preprocessing that must be applied.

    # The following two methods are equivalent:
    # - Directly load from the filepath:
    preprocessed_wav = encoder.preprocess_wav(in_fpath)
    # - If the wav is already loaded:
    '''original_wav, sampling_rate = librosa.load(str(in_fpath))
    preprocessed_wav = encoder.preprocess_wav(original_wav, sampling_rate)'''
    print("Loaded file succesfully")

    # Then we derive the embedding. There are many functions and parameters that the
    # speaker encoder interfaces. These are mostly for in-depth research. You will typically
    # only use this function (with its default parameters):
    embed = encoder.embed_utterance(preprocessed_wav)
    print("Created the embedding")
    return embed


# generates wav file from text
def generate_audio(text, embedding, synthesizer):
    # The synthesizer works in batch, so you need to put your data in a list or numpy array
    texts = [text]
    embeds = [embedding]
    # If you know what the attention layer alignments are, you can retrieve them here by
    # passing return_alignments=True
    print("not done synthesizing spectrograms")
    specs = synthesizer.synthesize_spectrograms(texts, embeds)
    print("done w spectrograms")
    spec = specs[0]

    print("Created the mel spectrogram")

    ## Generating the waveform
    print("Synthesizing the waveform:")

    # Synthesizing the waveform is fairly straightforward. Remember that the longer the
    # spectrogram, the more time-efficient the vocoder.
    generated_wav = vocoder.infer_waveform(spec)
    ## Post-generation
    # There's a bug with sounddevice that makes the audio cut one second earlier, so we
    # pad it.
    generated_wav = np.pad(generated_wav, (0, synthesizer.sample_rate), mode="constant")

    # Trim excess silences to compensate for gaps in spectrograms (issue #53)
    generated_wav = encoder.preprocess_wav(generated_wav)

    # playing the file
    print("trying to play sound")
    sd.play(generated_wav, synthesizer.sample_rate)
    sd.wait()


# generates wav files from odd lines
def process_odds(odds, embedding):
        print("processing odds")
        for sentence in odds:
            for i in range(5):
                time.sleep(5)
                print("running")
            print("generating odd sentence: " + sentence)
            generate_audio(sentence, embedding)

# generates wav files from even lines
def process_evens(evens, embedding, synthesizer):
    for sentence in evens:
        print("generating even sentence: " + sentence)
        generate_audio(sentence, embedding, synthesizer)

# plays audio from queue
def play_audio(generated_wavs):
    last_time = time.time()
    while True:
        if not generated_wavs.empty():
            sd.stop()
            sd.play(generated_wavs.get(), synthesizer.sample_rate)
            sd.wait()
            last_time = time.time()
        else:
            if time.time() - last_time > 100:
                print("done")
                break



if __name__ == "__main__":
    global synthesizer
    # load models
    encoder.load_model(Path("encoder/saved_models/prt_youtube2.pt"))
    syn_path = Path("synthesizer/saved_models/pretrained/pretrained.pt")
    synthesizer = Synthesizer(syn_path)
    synthesizer.load()
    vocoder.load_model(Path("vocoder/saved_models/pretrained/pretrained.pt"))
    encoder.embed_utterance(np.zeros(encoder.sampling_rate))

    # generating the embedding
    print("generating embedding")
    embedding = generate_embedding()

    count = 0
    evens = []
    odds = []

    # creating even and odd lists
    with open("recognized.txt", "r") as lines:
        for text in lines.readlines():
            if text != "" and text != "\n" and len(text) >= 4:
                if count % 2 == 0:
                    evens.append(text)
                    count += 1
                else:
                    odds.append(text)
                    count += 1

    # creating queue of wavs to be spoken
    #generated_wavs = multiprocessing.Queue()


    p1 = multiprocessing.Process(target=process_evens, args=(evens, embedding, synthesizer))
    #p2 = multiprocessing.Process(target=process_odds, args=(odds, embedding))
    # starting process 1
    p1.start()
    print("started p1")
    # starting process 2
    #p2.start()
    #print("started p2")

    # wait until process 1 is finished
    p1.join()
    # wait until process 2 is finished
    #p2.join()




#param
    #["safjhdkh", "kfahjlh", "fkjahjkh", "fadgsdg"]
    #convert them into mel spectrogram

#todo
    #multiprocessing
    #even and odd lines
    #read them sequentially by creating global list








    # Save it on the disk
    '''filename = "demo_output_%02d.wav" % num_generated
    print(generated_wav.dtype)
    sf.write(filename, generated_wav.astype(np.float32), synthesizer.sample_rate)
    num_generated += 1
    print("\nSaved output as %s\n\n" % filename)'''


