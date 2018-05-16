# Equalizer Pi
This is a project that I made for fun that displays audio on a visualizer.

Currently, the visualizer is based on a 8x20 grid of LEDs. I plan on making this more 
flexible in the future, but for now, this will have to do.

Based on Lightshowpi, it currently takes audio in from shairport-sync input, 
and outputs it to the LEDs after doing a bit of audio processing. 
Direct mic input is in the works, but for now shairport is the best way to stream audio.

## Installation

### Install Virtualenv
This project requires third party libraries to run, which are located in `requirements.txt`.
I would recommend a virtualenv in order to keep your global python path clean. 
On mac, install this using homebrew using `brew install virtualenv`
On Ubuntu, install using `sudo apt install virtualenv`. It may already be installed on 16.04.

### Activate Virtual Environment
Then to activate virtualenv, run `source <virtualenv_name>/bin/activate`. You should see a prompt
similar to 

`(equalizer) ➜  cd-router-dna-tests git:(master) ✗` in zsh. The important part
is the part in the parentheses which specifies your current virtualenv.

### Install Libraries from requirements.txt
Once you are in your virtualenv, run `pip install -r requirements.txt` to install necessary libraries.

## Running
To run the library, simply use `./equalizer.py` to start the equalizer. There are also flags
you can use to modify the behavior of the equalizer.

```
optional arguments:
  -h, --help       show this help message and exit
  --use-shairport  Indicates whether audio will be played over shairport or
                   not

```