from synthesizer.inference import Synthesizer
from encoder import inference as encoder
from vocoder import inference as vocoder
from pathlib import Path
import numpy as np
import sounddevice as sd
from torch import multiprocessing
from nltk import tokenize
import string
import time


class TextAloud():
    def break_text(self, text_file, sent_len):
        file_text = ""
        with open(text_file, "r") as lines:
            file_text = lines.read()

        file_text = file_text.replace("\n", " ")
        #print(file_text)
        text = tokenize.word_tokenize(file_text.translate(dict((ord(char), None) for char in string.punctuation)))
        text_length = len(text)
        prev_ind = 0
        l1 = []
        l2 = []
        l3 = []
        l4 = []

        count = 1

        for i in range(sent_len,text_length, sent_len):
            tidbit = " ".join(text[prev_ind:i])
            if count == 1:
                l1.append(tidbit)
            elif count == 2:
                l2.append(tidbit)
            elif count == 3:
                l3.append(tidbit)
            elif count == 4:
                l4.append(tidbit)


            #l4.append("-----")

            prev_ind = i
            count += 1
            if count == 5:
                count = 1

        leftover = text_length % sent_len
        if leftover != 0:
            leftover_text = " ".join(text[text_length - leftover: text_length])
            if len(l4) < len(l3):
                l4.append(leftover_text)
            elif len(l3) < len(l2):
                l3.append(leftover_text)
            elif len(l2) < len(l1):
                l2.append(leftover_text)
            else:
                l1.append(leftover_text)

        return l1, l2, l3, l4


    def break_text_syllables(self, text_file, max_syllables):
        file_text = ""
        with open(text_file, "r") as lines:
            file_text = lines.read()

        file_text = file_text.replace("\n", " ")
        text = tokenize.word_tokenize(file_text.translate(dict((ord(char), None) for char in string.punctuation)))
        text_len = len(text)
        l1 = []
        l2 = []
        l3 = []
        l4 = []

        count = 0
        syllables = 0
        temp_list = []
        last_i = 0
        for i in range(text_len):
            word_syllables = count_syllables(text[i])
            temp_list.append(text[i])
            syllables += word_syllables
            if syllables >= max_syllables:
                tidbit = " ".join(temp_list)
                if count == 0:
                    l1.append(tidbit)
                elif count == 1:
                    l2.append(tidbit)
                elif count == 2:
                    l3.append(tidbit)
                else:
                    l4.append(tidbit)

                last_i = i
                syllables = 0
                if count == 3:
                    count = 0
                else:
                    count += 1
                temp_list = []

        if last_i < text_len:
            leftover = " ".join(text[i:text_len])
            if len(l4) < len(l3):
                l4.append(leftover)
            elif len(l3) < len(l2):
                l3.append(leftover)
            elif len(l2) < len(l1):
                l2.append(leftover)
            else:
                l1.append(leftover)

        return l1, l2, l3, l4







    def count_syllables(self, word):
        syllable_count = 0
        for w in word:
            if (
                    w == 'a' or w == 'e' or w == 'i' or w == 'o' or w == 'u' or w == 'A' or w == 'E' or w == 'I' or w == 'O' or w == 'U'):
                syllable_count = syllable_count + 1
        return syllable_count


    def generate_embedding(self, in_fpath):
        #in_fpath = "data/other_test.wav"
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
    def generate_audio(self, text, embedding, synthesizer):
        # The synthesizer works in batch, so you need to put your data in a list or numpy array
        texts = [text]
        embeds = [embedding]
        # If you know what the attention layer alignments are, you can retrieve them here by
        # passing return_alignments=True
        #print("not done synthesizing spectrograms")
        specs = synthesizer.synthesize_spectrograms(texts, embeds)
        #print("done w spectrograms")
        spec = specs[0]

        #print("Created the mel spectrogram")

        ## Generating the waveform
        #print("Synthesizing the waveform:")


        # Synthesizing the waveform is fairly straightforward. Remember that the longer the
        # spectrogram, the more time-efficient the vocoder.
        generated_wav = vocoder.infer_waveform(spec)
        ## Post-generation
        # There's a bug with sounddevice that makes the audio cut one second earlier, so we
        # pad it.
        generated_wav = np.pad(generated_wav, (0, synthesizer.sample_rate), mode="constant")

        # Trim excess silences to compensate for gaps in spectrograms (issue #53)
        generated_wav = encoder.preprocess_wav(generated_wav)

        return generated_wav


    def process_l1(self, l1, embedding, generated_wavs):
        syn_path = Path("synthesizer/saved_models/pretrained/pretrained2.pt")
        synthesizer = Synthesizer(syn_path)
        synthesizer.load()
        vocoder.load_model(Path("vocoder/saved_models/pretrained/pretrained.pt"))
        count = 0
        for sentence in l1:
            if sentence != "" and sentence != " ":
                generated_wavs.append((generate_audio(sentence, embedding, synthesizer), count))
                count += 4

    # generates wav files from odd lines
    def process_l2(self, l2, embedding, generated_wavs):
        syn_path = Path("synthesizer/saved_models/pretrained/pretrained.pt")
        synthesizer = Synthesizer(syn_path)
        synthesizer.load()
        vocoder.load_model(Path("vocoder/saved_models/pretrained/pretrained.pt"))
        count = 1
        for sentence in l2:
            if sentence != "" and sentence != " ":
                generated_wavs.append((generate_audio(sentence, embedding, synthesizer), count))
                count += 4

    def process_l3(self, l3, embedding, generated_wavs):
        syn_path = Path("synthesizer/saved_models/pretrained/pretrained.pt")
        synthesizer = Synthesizer(syn_path)
        synthesizer.load()
        vocoder.load_model(Path("vocoder/saved_models/pretrained/pretrained.pt"))
        count = 2
        for sentence in l3:
            if sentence != "" and sentence != " ":
                generated_wavs.append((generate_audio(sentence, embedding, synthesizer), count))
                count += 4

    def process_l4(self, l4, embedding, generated_wavs):
        syn_path = Path("synthesizer/saved_models/pretrained/pretrained.pt")
        synthesizer = Synthesizer(syn_path)
        synthesizer.load()
        vocoder.load_model(Path("vocoder/saved_models/pretrained/pretrained.pt"))
        count = 3
        for sentence in l4:
            if sentence != "" and sentence != " ":
                generated_wavs.append((generate_audio(sentence, embedding, synthesizer), count))
                count += 4

    def process_l5(self, l5, embedding, generated_wavs):
        syn_path = Path("synthesizer/saved_models/pretrained/pretrained.pt")
        synthesizer = Synthesizer(syn_path)
        synthesizer.load()
        vocoder.load_model(Path("vocoder/saved_models/pretrained/pretrained.pt"))
        count = 4
        for sentence in l5:
            if sentence != "" and sentence != " ":
                generated_wavs.append((generate_audio(sentence, embedding, synthesizer), count))
                count += 7

    def process_l6(self, l6, embedding, generated_wavs):
        syn_path = Path("synthesizer/saved_models/pretrained/pretrained.pt")
        synthesizer = Synthesizer(syn_path)
        synthesizer.load()
        vocoder.load_model(Path("vocoder/saved_models/pretrained/pretrained.pt"))
        count = 5
        for sentence in l6:
            if sentence != "" and sentence != " ":
                generated_wavs.append((generate_audio(sentence, embedding, synthesizer), count))
                count += 7

    def process_l7(self, l7, embedding, generated_wavs):
        syn_path = Path("synthesizer/saved_models/pretrained/pretrained.pt")
        synthesizer = Synthesizer(syn_path)
        synthesizer.load()
        vocoder.load_model(Path("vocoder/saved_models/pretrained/pretrained.pt"))
        count = 6
        for sentence in l7:
            if sentence != "" and sentence != " ":
                generated_wavs.append((generate_audio(sentence, embedding, synthesizer), count))
                count += 7




    # plays audio from queue
    def play_audio(self, generated_wavs, synthesizer, total_len):
        time.sleep(120)
        element = 0
        while True:
            for j in range(len(generated_wavs)):
                wav_tup = generated_wavs[j]
                #print("\n\n\n" + "wav_tup[1]: " + str(wav_tup[1]) + " element= " + str(element) + "\n\n")
                if wav_tup[1] == element:
                    sd.stop()
                    sd.play(wav_tup[0], synthesizer.sample_rate)
                    element += 1
                    sd.wait()
                    generated_wavs.pop(j)
                    break
            if element == total_len:
                break

        print("\n\n\n----------done playing audio-------------\n\n\n")
        #print(done_sents)

    def main(self, path_to_wav):
        # print(multiprocessing.cpu_count())
        global synthesizer
        global vocoder
        # load models
        encoder.load_model(Path("encoder/saved_models/prt_youtube2.pt"))
        syn_path = Path("synthesizer/saved_models/pretrained/pretrained.pt")
        synthesizer = Synthesizer(syn_path)
        synthesizer.load()
        vocoder.load_model(Path("vocoder/saved_models/pretrained/pretrained.pt"))
        encoder.embed_utterance(np.zeros(encoder.sampling_rate))

        # generating the embedding
        print("generating embedding")
        embedding = self.generate_embedding(path_to_wav)

        print("breaking text")
        l1, l2, l3, l4 = self.break_text("recognized.txt", sent_len=34)
        print("done breaking text")
        total_len = len(l1) + len(l2) + len(l3) + len(l4)

        # creating queue of wavs to be spoken
        manager = multiprocessing.Manager()
        generated_wavs = manager.list()

        p1 = multiprocessing.Process(target=self.process_l1, args=(l1, embedding, generated_wavs))
        p2 = multiprocessing.Process(target=self.process_l2, args=(l2, embedding, generated_wavs))
        p3 = multiprocessing.Process(target=self.process_l3, args=(l3, embedding, generated_wavs))
        p4 = multiprocessing.Process(target=self.process_l4, args=(l4, embedding, generated_wavs))
        p5 = multiprocessing.Process(target=self.play_audio, args=(generated_wavs, synthesizer, total_len))

        '''p5 = multiprocessing.Process(target=process_l5, args=(l5, embedding, generated_wavs))
        p6 = multiprocessing.Process(target=process_l6, args=(l6, embedding, generated_wavs))
        p7 = multiprocessing.Process(target=process_l7, args=(l7, embedding, generated_wavs))'''

        p1.start()
        p2.start()
        p3.start()
        p4.start()

        p5.start()
        '''
        p6.start()
        p7.start()
        p8.start()'''
        p1.join()
        p2.join()
        p3.join()
        p4.join()
        p5.join()
        '''
        p6.join()
        p7.join()
        p8.join()'''

if __name__ == "__main__":
    multiprocessing.set_start_method('spawn', force=True)
    print("creating reader")
    reader = TextAloud()
    reader.main("data/Miller_2.wav")

    '''
    todo
    
    look into speeding up wavenet
    possibly training on large files
    weight pruning
    
    '''
