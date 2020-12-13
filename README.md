# GANs-TTS
GANs project for inspirit

**MAKE SURE YOU ARE USING PYTHON 3.7**

Steps to use:

1 Download Real-Time-Voice-Cloning [RTVC] from github.

2 Switch encoder_preprocess.py & preprocess.py in RTVC with the given replacements

3 Put saved_models into RTVC/encoder

4 Put the temp folder in the location you will run Youtube.py
        This is because python has trouble creating .webm files

5 Run Youtube.py

6 run pip3 install -r RTVC/requirments.txt

7 Run encoder_preprocess.py  Path/to/out/Youtube_dataset

8 Run encoder_train.py pretrained Path/to/out/Youtube_dataset/SV2TTS/encoder
