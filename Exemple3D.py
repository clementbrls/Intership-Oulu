import audio_tools as at
from pydub import AudioSegment
from mic import Mic
import crosscorrelation as cc
import Geometry as m
import matplotlib.pyplot as plt
import numpy as np

x_bee = 300  # coordinate of the bee in mm
y_bee = -400
z_bee = 500

mic0 = Mic(0, 0, 0)  # coordinate of the mic in mm
mic1 = Mic(300, 0, 0)
mic2 = Mic(0, 300, 0)
mic3 = Mic(0, 0, 300)

audio=AudioSegment.from_file("./abeille.mp3")

#Generation audio
audio0=at.gen_spacialize(audio,x_bee,y_bee,z_bee,mic0)
audio0=at.extract_audio_second(1000,audio0)
#audio0=at.add_noise_to_audio(audio0,30)

audio1=at.gen_spacialize(audio,x_bee,y_bee,z_bee,mic1)
audio1=at.extract_audio_second(1000,audio1)
#audio1=at.add_noise_to_audio(audio1,30)

audio2=at.gen_spacialize(audio,x_bee,y_bee,z_bee,mic2)
audio2=at.extract_audio_second(1000,audio2)
#audio2=at.add_noise_to_audio(audio2,30)

audio3=at.gen_spacialize(audio,x_bee,y_bee,z_bee,mic3)
audio3=at.extract_audio_second(1000,audio3)
#audio3=at.add_noise_to_audio(audio3,30)



delta1_ms=cc.crosscorrelate(audio0,audio1)
delta2_ms=cc.crosscorrelate(audio0,audio2)
delta3_ms=cc.crosscorrelate(audio0,audio3)

delta1=-1*delta1_ms/1000*340*1000
delta2=-1*delta2_ms/1000*340*1000
delta3=-1*delta3_ms/1000*340*1000


'''
def offset(x_bee, y_bee, z_bee, mic):
    x_mic = mic.x
    y_mic = mic.y
    z_mic = mic.z
    distance = np.sqrt((x_bee-x_mic)**2+(y_bee-y_mic)**2+(z_bee-z_mic)**2)
    distance*1000/(340*1000)
    return distance


#delta
delta0 = offset(x_bee, y_bee, z_bee, mic0)
delta1 = offset(x_bee, y_bee, z_bee, mic1)
delta2 = offset(x_bee, y_bee, z_bee, mic2)
delta3 = offset(x_bee, y_bee, z_bee, mic3)

delta1 = delta1-delta0
delta2 = delta2-delta0
delta3 = delta3-delta0
delta0 = 0
'''
print("Coordonée réel : ", x_bee, y_bee, z_bee)
m.WhereItIs(mic0, mic1, mic2, mic3, delta1, delta2, delta3)

points1 = m.whereItCouldBe3D(mic0, mic1, delta1)
points2 = m.whereItCouldBe3D(mic0, mic2, delta2)
points3 = m.whereItCouldBe3D(mic0, mic3, delta3)

points1, points2, points3 = m.reduce(points1, points2, points3,200)

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
plt.show()





#print("coordonées estimé : ", m.find_intersect(points1, points2, points3))
# print("Coordonée estimé : ",x_i,y_i)



#print("Coordonée estimé : ", m.find_intersect(points1, points2, points3))
