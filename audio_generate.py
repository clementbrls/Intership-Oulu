import audio_tools as at
from pydub import AudioSegment
from mic import Mic

input_file="./Abeille1.wav"
audio = AudioSegment.from_file(input_file)

mic1=Mic(0,0,0)
mic2=Mic(5000,0,0)
mic3=Mic(0,5000,0)
mic4=Mic(0,0,5000)



#Generation premier audio
audio0=at.gen_spacialize(audio,200,5000,0,mic1)
audio0=at.extract_audio_second(1000,audio0)
#audio0=at.add_noise_to_audio(audio0,50)
audio0.export("./Abeille1_0.wav", format='wav')


audio1=at.gen_spacialize(audio,200,5000,0,mic2)
audio1=at.extract_audio_second(1000,audio1)
#audio1=at.add_noise_to_audio(audio1,50)
audio1.export("./Abeille1_1.wav", format='wav')

#generation deuxieme audio
audio2=at.gen_spacialize(audio,200,5000,0,mic3)
audio2=at.extract_audio_second(1000,audio2)
#audio2=at.add_noise_to_audio(audio2,50)
audio2.export("./Abeille1_2.wav", format='wav')

