import numpy as np
from matplotlib import pyplot as plt
import math as Math

g = 9.8  # gravitational acceleration in m/s^2
vo = 5.0   # initial velocity in m/s

resolution = 100
PI = Math.pi
# print(PI)
alpha = 45*(Math.pi/180.0)
# print(Math.sin(alpha))
x = []
y = []

start_time = 0
end_time = 1

delta = (end_time - start_time) / resolution

for i in range(resolution):
    t = delta * i
    print(t)
    x.append(vo * Math.cos(alpha) * t)
    y.append(vo*Math.sin(alpha)*t - 0.5 * g * (t**2))

plt.plot(x, y)
plt.xlabel("Horizontal Distance (m)")
plt.ylabel("Vertical Position (m)")
plt.title("Projectile Motion")
plt.show()
