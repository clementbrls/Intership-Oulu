import numpy as np
import matplotlib.pyplot as plt

def find(mic0,mic1,delta,dist):
    x1=mic0.x
    y1=mic0.y
    r1=dist

    x2=mic1.x
    y2=mic1.y
    r2=dist+delta

    d=np.sqrt((x2-x1)**2+(y2-y1)**2)
    a=(r1**2-r2**2+d**2)/(2*d)
    x_mid=x1+a*(x2-x1)/d
    y_mid=y1+a*(y2-y1)/d

    h=np.sqrt(r1**2-a**2)

    xa=x_mid+h*(y2-y1)/d
    ya=y_mid+h*(x2-x1)/d

    xb=x_mid-h*(y2-y1)/d
    yb=y_mid-h*(x2-x1)/d

    return xa,ya,xb,yb
    



def whereItCouldBe(mic0,mic1,delta):
    x=np.empty(0)
    y=np.empty(0)

    distmin=(mic0.dist(mic1)-delta)/2
    print(distmin)
    distmax=1000
    res=1000
    for i in np.logspace(np.log10(distmin+(1/res)),np.log10(distmax),res):
        u=find(mic0,mic1,delta,i)
        x=np.append(x,u[0])
        y=np.append(y,u[1])
        x=np.append(u[2],x)
        y=np.append(u[3],y)
    return x,y


