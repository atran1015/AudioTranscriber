# Program execution instructions
1. Using command line
	- run "source env/bin/activate" OR make your own virtual environment and run "pip install -r requirements.txt"

	- ./transcriber.py


2. Using the executable file (currently only Linux-compatible)
	- in the "dist" folder, click and run the transcriber executable

# Setup Instruction files:
README.md

requirements.txt

# Outputs generated:
convertedmp3.mp3

convertedwav.wav

texts.txt

audio-chunks

audio-chunks/chunk[number].wav

# Test videos:
french.mp4

japanese.mp4

mandarin.mp4

spanish.mp4

# Executable builds:
build/transcriber

dist/

transcriber.spec

# Algorithm evaluation:
evaluation and data/

actualtext.txt

sampletexts.txt

Evaluation.R

Highlight text difference evaluation.docx

Word Error Rate (WER) evaluation.docx

# Actual Program:
transcriber.py

# About transcriber.py:
* The functions: They are associated with button clicks and it is where the SpeechRecognition A.I. is being used
* Codes outside of functions: They provide the front-end look

# Note:
Some demo videos are placed in the folder, if you wish to use your own video:

* make sure that it is placed in the same folder as transcriber.py (or in the dist folder if you are using the executable version) in order for video conversion to work

an "audio-chunks" folder will be generated where the program is

# Specifications:
Video format - .mp4, length has to be less than 1 minute

Audio format - .wav

Languages available - Mandarin, French, Spanish, Japanese
