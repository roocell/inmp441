##############################################
# INMP441 MEMS Microphone + I2S Module
##############################################
# .wav files of MEMS mic recording
#
# --------------------------------------------
# -- by Josh Hrisko, Maker Portal LLC
# --------------------------------------------
#  https://makersportal.com/blog/recording-stereo-audio-on-a-raspberry-pi
##############################################
#
import pyaudio
import numpy as np
import time,wave,datetime,os

##############################################
# function for setting up pyserial
##############################################
#
def pyserial_start():
    audio = pyaudio.PyAudio() # create pyaudio instantiation
    ##############################
    ### create pyaudio stream  ###
    # -- streaming can be broken down as follows:
    # -- -- format             = bit depth of audio recording (16-bit is standard)
    # -- -- rate               = Sample Rate (44.1kHz, 48kHz, 96kHz)
    # -- -- channels           = channels to read (1-2, typically)
    # -- -- input_device_index = index of sound device
    # -- -- input              = True (let pyaudio know you want input)
    # -- -- frames_per_buffer  = chunk to grab and keep in buffer before reading
    ##############################
    stream = audio.open(format = pyaudio_format,rate = samp_rate,channels = chans, \
                        input_device_index = dev_index,input = True, \
                        frames_per_buffer=CHUNK)
    stream.stop_stream() # stop stream to prevent overload
    return stream,audio

def pyserial_end():
    stream.close() # close the stream
    audio.terminate() # close the pyaudio connection

#
##############################################
# function for grabbing data from buffer
##############################################
def data_grabber(rec_len, volume_gain=10.0):
    stream.start_stream()  # start data stream
    stream.read(CHUNK, exception_on_overflow=False)  # flush port first
    t_0 = datetime.datetime.now()  # get datetime of recording start
    print('Recording Started.')
    data, data_frames = [], []  # variables
    for frame in range(0, int((samp_rate * rec_len) / CHUNK)):
        # grab data frames from buffer
        stream_data = stream.read(CHUNK, exception_on_overflow=False)
        # Adjust volume/gain
        audio_data = np.frombuffer(stream_data, dtype=buffer_format)
        adjusted_audio_data = np.int16(audio_data * volume_gain)
        data_frames.append(adjusted_audio_data.tobytes())  # append data
        data.append(adjusted_audio_data)
    stream.stop_stream()  # stop data stream
    print('Recording Stopped.')
    return data, data_frames, t_0

#
##############################################
# Save data as .wav file
##############################################
#
def data_saver(t_0):
    data_folder = './data/' # folder where data will be saved locally
    if os.path.isdir(data_folder)==False:
        os.mkdir(data_folder) # create folder if it doesn't exist
    filename = datetime.datetime.strftime(t_0,
                                          '%Y_%m_%d_%H_%M_%S_pyaudio') # filename based on recording time
    wf = wave.open(data_folder+filename+'.wav','wb') # open .wav file for saving
    wf.setnchannels(chans) # set channels in .wav file 
    wf.setsampwidth(audio.get_sample_size(pyaudio_format)) # set bit depth in .wav file
    wf.setframerate(samp_rate) # set sample rate in .wav file
    wf.writeframes(b''.join(data_frames)) # write frames in .wav file
    wf.close() # close .wav file
    return filename
#
##############################################
# Main Data Acquisition Procedure
##############################################
#   
if __name__=="__main__":
    #
    ###########################
    # acquisition parameters
    ###########################
    #
    CHUNK          = 44100  # frames to keep in buffer between reads
    samp_rate      = 44100 # sample rate [Hz]
    pyaudio_format = pyaudio.paInt16 # 16-bit device
    buffer_format  = np.int16 # 16-bit for buffer
    chans          = 1 # only read 1 channel
    dev_index      = 0 # index of sound device    (from dumpaudio.py)
    #
    #############################
    # stream info and data saver
    #############################
    #
    stream,audio = pyserial_start() # start the pyaudio stream   
    record_length =  5 # seconds to record
    input('Press Enter to Record Data (Turn Freq. Generator On)')
    data_chunks,data_frames,t_0 = data_grabber(record_length) # grab the data
    data_saver(t_0) # save the data as a .wav file
    pyserial_end() # close the stream/pyaudio connection