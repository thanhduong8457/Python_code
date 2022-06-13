import math as Math
import numpy as np
from numpy.linalg import inv
import delta_define
import time

# e=delta_define.e()
# f=delta_define.f()
# re=delta_define.l2()
# rf=delta_define.l1()

e  = 86.5   #endeffector
f  = 346.4  #base
re = 465    #endeffector arm
rf = 200    #Base arm
        

# Constantes Trigonometricas
sqrt3=delta_define.sqrt3()
pi=delta_define.pi()
sin120=sqrt3/2.0
cos120=delta_define.cos120()
tan60=sqrt3
sin30=delta_define.sin30()
tan30=delta_define.tan30()

# Transformacion unidades
dtr=delta_define.dtr()
mtmm=delta_define.mtmm()
mmtm=delta_define.mmtm()
rtd= delta_define.rtd()

def delta_calcForward(theta1, theta2, theta3):
    x0=0.0
    y0=0.0
    z0=0.0
  
    t = (f-e)*tan30/2.0
    dtr = pi/180.0

    theta1 *= dtr
    theta2 *= dtr
    theta3 *= dtr

    y1 = -(t + rf*Math.cos(theta1))
    z1 = -rf*Math.sin(theta1)

    y2 = (t + rf*Math.cos(theta2))*sin30
    x2 = y2*tan60
    z2 = -rf*Math.sin(theta2)

    y3 = (t + rf*Math.cos(theta3))*sin30
    x3 = -y3*tan60
    z3 = -rf*Math.sin(theta3)

    dnm = (y2-y1)*x3-(y3-y1)*x2

    w1 = y1*y1 + z1*z1
    w2 = x2*x2 + y2*y2 + z2*z2
    w3 = x3*x3 + y3*y3 + z3*z3

  # x = (a1*z + b1)/dnm
    a1 = (z2-z1)*(y3-y1)-(z3-z1)*(y2-y1)
    b1 = -((w2-w1)*(y3-y1)-(w3-w1)*(y2-y1))/2.0

  # y = (a2*z + b2)/dnm
    a2 = -(z2-z1)*x3+(z3-z1)*x2
    b2 = ((w2-w1)*x3 - (w3-w1)*x2)/2.0

  # a*z^2 + b*z + c = 0
    a = a1*a1 + a2*a2 + dnm*dnm
    b = 2.0*(a1*b1 + a2*(b2-y1*dnm) - z1*dnm*dnm)
    c = (b2-y1*dnm)*(b2-y1*dnm) + b1*b1 + dnm*dnm*(z1*z1 - re*re)

  # discriminant
    d = b*b - 4.0*a*c
    if (d < 0.0):
        return [1,0,0,0] # non-existing povar. return error,x,y,z
  
    z0 = -0.5*(b+Math.sqrt(d))/a
    x0 = (a1*z0 + b1)/dnm
    y0 = (a2*z0 + b2)/dnm

    return [0,x0,y0,z0]# return error,x,y,z

if __name__ == "__main__":

  theta_1 = 0
  theta_2 = 0
  theta_3 = 0

  temp,x,y,z = delta_calcForward(theta_1, theta_2, theta_3)
  print(x,y,z)
        
