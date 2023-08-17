import audio_tools as at
from pydub import AudioSegment
from mic import Mic
import crosscorrelation as cc
import Geometry as m
import matplotlib.pyplot as plt
import numpy as np

# Coordinates of the bee
x_bee = 300
y_bee = -400
z_bee = 500

# coordinate of the mic in mm
mic0 = Mic(0, 0, 0)  
mic1 = Mic(300, 0, 0)
mic2 = Mic(0, 300, 0)
mic3 = Mic(0, 0, 300)

audio=AudioSegment.from_file("./bee.mp3")

#Fake audio generation
audio0=at.gen_spacialize(audio,x_bee,y_bee,z_bee,mic0)
audio0=at.extract_audio_second(1000,audio0)
#audio0=at.add_noise_to_audio(audio0,5)

audio1=at.gen_spacialize(audio,x_bee,y_bee,z_bee,mic1)
audio1=at.extract_audio_second(1000,audio1)
#audio1=at.add_noise_to_audio(audio1,5)

audio2=at.gen_spacialize(audio,x_bee,y_bee,z_bee,mic2)
audio2=at.extract_audio_second(1000,audio2)
#audio2=at.add_noise_to_audio(audio2,5)

audio3=at.gen_spacialize(audio,x_bee,y_bee,z_bee,mic3)
audio3=at.extract_audio_second(1000,audio3)
#audio3=at.add_noise_to_audio(audio3,5)

#calculate the time shift between the 4 mics
delta1_ms=cc.crosscorrelate(audio0,audio1)
delta2_ms=cc.crosscorrelate(audio0,audio2)
delta3_ms=cc.crosscorrelate(audio0,audio3)
#convert the time shift into distance
delta1=-1*delta1_ms/1000*340*1000
delta2=-1*delta2_ms/1000*340*1000
delta3=-1*delta3_ms/1000*340*1000


'''
#this is usefull to bypass the audio, and to just test the algorithm
def offset(x_bee, y_bee, z_bee, mic):
    x_mic = mic.x
    y_mic = mic.y
    z_mic = mic.z
    distance = np.sqrt((x_bee-x_mic)**2+(y_bee-y_mic)**2+(z_bee-z_mic)**2)
    distance*1000/(340*1000)
    return distance

delta0 = offset(x_bee, y_bee, z_bee, mic0)
delta1 = offset(x_bee, y_bee, z_bee, mic1)
delta2 = offset(x_bee, y_bee, z_bee, mic2)
delta3 = offset(x_bee, y_bee, z_bee, mic3)

delta1 = delta1-delta0
delta2 = delta2-delta0
delta3 = delta3-delta0
delta0 = 0
'''

print("real coord: ", x_bee, y_bee, z_bee)
coord = m.WhereItIs(mic0, mic1, mic2, mic3, delta1, delta2, delta3)
print("estimated coord: ", np.round(coord[0]), np.round(coord[1]), np.round(coord[2]))

points1 = m.whereItCouldBe3D(mic0, mic1, delta1, res=100)
points2 = m.whereItCouldBe3D(mic0, mic2, delta2, res=100)
points3 = m.whereItCouldBe3D(mic0, mic3, delta3, res=100)

#points1, points2, points3 = m.reduce(points1, points2, points3,150)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# show the mics
ax.scatter(mic0.x, mic0.y, mic0.z, c='r')
ax.scatter(mic1.x, mic1.y, mic1.z, c='orange')
ax.scatter(mic2.x, mic2.y, mic2.z, c='g')
ax.scatter(mic3.x, mic3.y, mic3.z, c='y') 
# show all the points
ax.plot(points1[:, 0], points1[:, 1], points1[:, 2], c='r', alpha=0.3)
ax.plot(points2[:, 0], points2[:, 1], points2[:, 2], c='green', alpha=0.3)
ax.plot(points3[:, 0], points3[:, 1], points3[:, 2], c='blue', alpha=0.3)
#the bee
ax.scatter(x_bee, y_bee, z_bee, c='white', marker='x', s=100, label='Bee', alpha=1)
#the estimated point
ax.scatter(coord[0], coord[1], coord[2], c='black', marker='x', s=100, label='Estimated', alpha=1)
plt.show()

