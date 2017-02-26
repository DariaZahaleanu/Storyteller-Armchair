import serial
import pyaudio
import sys
import os
import wave
import glob

recording = False
frames = []
sound_path = '/home/pi/Desktop/daria/'
currRecNum = len(glob.glob('/home/pi/Desktop/daria/soundFile_*.wav'))+1
numBack = 1

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 48000
CHUNK = 2048
##RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = ""
 
##audio = pyaudio.PyAudio()

try:
    ser = serial.Serial("/dev/ttyUSB0", 9600)
except:
    ser = serial.Serial("/dev/ttyUSB1", 9600)

ser.flush()
##stream = audio.open(format=FORMAT, channels=CHANNELS,
##            rate=RATE, input=True,
##            frames_per_buffer=CHUNK)
def playRecording(path):
    print(path)
    wf = wave.open(path, 'rb')
    p = pyaudio.PyAudio()
    play_stream = p.open(format =
                    p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)
    # read data (based on the chunk size)
    data = wf.readframes(CHUNK)

    # play stream (looping from beginning of file to the end)
    while data != '':
        # writing to the stream is what *actually* plays the sound.
        play_stream.write(data)
        data = wf.readframes(CHUNK)
    # cleanup stuff.
    play_stream.close()    
    p.terminate()
  
def startRecording():
    recording = True
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
 
def stopRecording():
    recording = False    
    stream.stop_stream()
    stream.close()
    audio.terminate()
    WAVE_OUTPUT_FILENAME = "soundFile_" + str(currRecNum) + ".wav"
    currRecNum+=1
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
    numBack = 1
    frames = []

while 1:
    if (ser.inWaiting() > 0):
        arduinoMsg = ser.readline()
        #if arduinoMsg == ' ':
         #   continue
        #print('|'+arduinoMsg+'|')
        try:
            arduinoMsg = int(arduinoMsg[0])
        except:
            continue
        if arduinoMsg == 1: ## 1: START RECORDING
            playRecording('/home/pi/Desktop/daria/default_sound_files/StartTellingTheStory.wav')
            
            ##start recording
            print('start recording msg')
##            startRecording()
            recording = True
            audio = pyaudio.PyAudio()
            stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)

        elif arduinoMsg == 4: ## 0: STOP RECORDING
            ##stop recording
            print('stop recording msg')
##            stopRecording()
            recording = False    
            stream.stop_stream()
            stream.close()
            audio.terminate()
            WAVE_OUTPUT_FILENAME = "soundFile_" + str(currRecNum) + ".wav"
            currRecNum+=1
            waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            waveFile.setnchannels(CHANNELS)
            waveFile.setsampwidth(audio.get_sample_size(FORMAT))
            waveFile.setframerate(RATE)
            waveFile.writeframes(b''.join(frames))
            waveFile.close()
            frames = []       
            playRecording('/home/pi/Desktop/daria/default_sound_files/StoryRecorded.wav')
        elif arduinoMsg == 2:## 1: play most recent
            playRecording(sound_path+'soundFile_' + str(currRecNum-1) +'.wav')
        elif arduinoMsg == 3:#play playback
            print('received si2gnal')
            if currRecNum-1-numBack >= 1:
                playRecording(sound_path+'soundFile_' + str(currRecNum-1-numBack) +'.wav')
                numBack+=1
    else:
        if recording:
            data = stream.read(CHUNK)
            frames.append(data)


