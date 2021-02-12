# GANs-TTS
GANs project

**MAKE SURE YOU ARE USING PYTHON 3.7**

Steps to use:

1 Download Real-Time-Voice-Cloning [RTVC] from github.

2 Switch encoder_preprocess.py & preprocess.py in RTVC with the given replacements

3 Put saved_models into RTVC/encoder

4 Create a folder called URLs and place textfiles containing URLs to be downloaded

5 run pip3 install ffmpeg on the CLI

6 add your assembly api key to const.py  [http://assemblyai.com]

7 Run yt_download.py

8 Run pip3 install -r RTVC/requirments.txt

9 Run encoder_preprocess.py  Path/to/out/Youtube_dataset

10 Open a visdom server in a seperate CLI (command line interface)

11 Run encoder_train.py pretrained Path/to/out/Youtube_dataset/SV2TTS/encoder
