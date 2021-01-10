# GANs-TTS
GANs project for inspirit

**MAKE SURE YOU ARE USING PYTHON 3.7**

Steps to use:

1 Download Real-Time-Voice-Cloning [RTVC] from github.

2 Switch encoder_preprocess.py & preprocess.py in RTVC with the given replacements

3 Put saved_models into RTVC/encoder

4 Create a folder called URLs and place textfiles containing URLs to be downloaded

5 Run yt_download.py

6 Run pip3 install -r RTVC/requirments.txt

7 Run encoder_preprocess.py  Path/to/out/Youtube_dataset

8 Open a visdom server in a seperate CLI (command line interface)

9 Run encoder_train.py pretrained Path/to/out/Youtube_dataset/SV2TTS/encoder
