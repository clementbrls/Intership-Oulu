# Localisation Audio3D

To start using the project just do :

    pip install -r .\requirements.txt

You can use "Exemple3D.py" to test the program, just change the coordinates of the fake bee and the fakes mics and it will create audios that correspond to what the mics would have recorded
    
    x_bee= 30
    y_bee= -400
    z_bee= 500
    
    mic0=Mic(0,0,0)
    mic1=Mic(300,0,0)
    mic2=Mic(0,300,0)
    mic3=Mic(0,0,300)

If you want to add noise to the audios, just uncomment all this lines :
    
    #audio0=at.add_noise_to_audio(audio0,30)

The cross-corelation will do his magic and the result will be ploted, the bee is where the 3 graphs intersect

The accuracy is around few centimeters, but it depends on the noise and the distance between the mics

To better understand the math behind the graphs : https://www.geogebra.org/calculator/dsefftru
By using "Exemple2D.py" you will better understand how the program works

## What to do next?
For now the coordinates are only approximated, so it would be a good thing to find a way to get the exact coordinates of the bee using math
The cross-corelation algorithm works quite well, but it needs to be tested in real life.
