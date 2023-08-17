from pydub import AudioSegment
from pydub.generators import WhiteNoise
import numpy as np

def add_noise_to_audio(audio, noise_level):

    #generate white noise
    noise = WhiteNoise().to_audio_segment(duration=len(audio))

    #Ajust noise level
    noise = noise - (60 - noise_level)

    noisy_audio = audio.overlay(noise)

    return noisy_audio

    
def extract_audio_second(start_ms,audio):
    # Extract the a second of the audio (1000 ms)
    first_second = audio[start_ms:start_ms+1000]
    return first_second

def apply_time_offset(audio, offset_ms):
    #convert the audio into a numpy array
    sig=np.array(audio.get_array_of_samples())
    offset_samples=int(offset_ms/1000*audio.frame_rate)
    sig=np.roll(sig,offset_samples)
    offset_audio=AudioSegment(sig.tobytes(),frame_rate=audio.frame_rate,sample_width=audio.sample_width,channels=audio.channels)
    return offset_audio


def gen_spacialize(audio,x_bee,y_bee,z_bee,mic):
    x_mic=mic.x
    y_mic=mic.y
    z_mic=mic.z
    distance=np.sqrt((x_bee-x_mic)**2+(y_bee-y_mic)**2+(z_bee-z_mic)**2)
    time_offset = distance*1000/(340*1000)
    offset_audio=apply_time_offset(audio, time_offset)
    return offset_audio

