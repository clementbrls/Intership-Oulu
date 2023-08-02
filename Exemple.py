import audio_tools as at
from pydub import AudioSegment
from mic import Mic
import crosscorrelation as cc
import Geometry as m
import matplotlib.pyplot as plt
import numpy as np

x_bee=-480 #coordinate of the bee in mm
y_bee=-500
z_bee=0

mic0=Mic(0,0,0) #coordinate of the mic in mm
mic1=Mic(50,0,0)
mic2=Mic(0,50,0)
mic3=Mic(0,0,100)

audio=AudioSegment.from_file("./Abeille1.wav")

#Generation audio
audio0=at.gen_spacialize(audio,x_bee,y_bee,z_bee,mic0)
audio0=at.extract_audio_second(1000,audio0)
#audio0=at.add_noise_to_audio(audio0,30)

audio1=at.gen_spacialize(audio,x_bee,y_bee,z_bee ,mic1)
audio1=at.extract_audio_second(1000,audio1)
#audio1=at.add_noise_to_audio(audio1,30)

audio2=at.gen_spacialize(audio,x_bee,y_bee,z_bee ,mic2)
audio2=at.extract_audio_second(1000,audio2)
#audio2=at.add_noise_to_audio(audio2,30)

audio3=at.gen_spacialize(audio,x_bee,y_bee,z_bee ,mic3)
audio3=at.extract_audio_second(1000,audio3)
#audio3=at.add_noise_to_audio(audio3,30)


delta1_ms=cc.crosscorrelate(audio0,audio1)
delta2_ms=cc.crosscorrelate(audio0,audio2)
#delta3_ms=cc.crosscorrelate(audio0,audio3)
print(delta1_ms,delta2_ms)

delta1=-1*delta1_ms/1000*340*1000
delta2=-1*delta2_ms/1000*340*1000
#delta3=-1*delta3_ms/1000*340*1000
#print(delta1,delta2)

delta1=35.519911231336
delta2=36.891061953462

x1,y1 = m.whereItCouldBe(mic0,mic1,delta1)
x2,y2 = m.whereItCouldBe(mic0,mic2,delta2)


print("Coordonée réel : ",x_bee,y_bee)
#print("Coordonée estimé : ",x_i,y_i)

plt.plot(x1,y1,'r')
plt.plot(x2,y2,'b')
plt.show()







