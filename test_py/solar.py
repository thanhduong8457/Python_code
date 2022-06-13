#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%# NLX
#python3 sollar_angle.py day month st/ct time
#Nước Mắt Em Lau Bằng Tình Yêu Mới
#https://power.larc.nasa.gov/data-access-viewer/
import sys
import math
import numpy as np

pi = math.pi

def sin(temp):
    return math.sin(temp)

def cos(temp):
    return math.cos(temp)

def arcsin(temp):
    return np.arcsin(temp)

convert_day = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]

clock_time = 'no'
#clock_time = 'yes'
ST = 12
CT = 12
##########################################################################################

for i in range(1, 13):
    
    month = i #while loop

    # Need to type Day and Month here
    day = 15
    n = convert_day[month - 1] - 1 + day
    # Vi Do
    L = 11.1451
    # Kinh Don giua mui gio
    LT = 15*7 # mui gio +7
    # Kinh Do
    LL = 108.2105

    ######### DO NOT EDIT STILL HERE ######### ######### DO NOT EDIT STILL HERE ######### 
    B = 360/364*(n-81)
    E = 9.28*sin(2*B*pi/180) - 7.53*cos(B*pi/180) - 1.5*sin(B*pi/180)

    if clock_time == 'yes':
        ST = CT + (LT - LL)/15 + E/60

    H = 15*(12 - ST)
    # Find Delta
    delta = 23.45*sin((360/365)*(n - 81)*pi/180)
    # Find Beta
    beta = arcsin(cos(L*pi/180)*cos(delta*pi/180)*cos(H*pi/180)
            + sin(L*pi/180)*sin(delta*pi/180))*180/pi

    if(beta>90):
        beta = 180 - beta

    m = 1/sin(beta*pi/180)
    tilt = 90 - beta
    phiS = arcsin((cos(delta*pi/180)*sin(H*pi/180))/cos(beta*pi/180))*180/pi

    print('month:  ', month,'  tilt: ' ,tilt,'  phiS: ' ,phiS)