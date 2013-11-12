#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Transmission Line Simulation
author: Cristóbal Ganter

Based on the script:

    Matplotlib Animation Example

    posted on: http://jakevdp.github.io/blog/2012/08/18/matplotlib-animation-tutorial/
    author: Jake Vanderplas
    email: vanderplas@astro.washington.edu
    website: http://jakevdp.github.com
    license: BSD
    Please feel free to use and modify this, but keep the above information. Thanks!
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

e = np.exp
j = np.complex(0,1)         #imaginary unit

Z0 = np.complex(2, 0)       #Impedance of the transmission line
ZG = Z0                     #Internal impedance of the generator
VG = np.complex(20, 0)      #Generator's voltage

a = 0                       #alpha: attenuation constant
b = 2*np.pi                 #beta: phase constant
g = np.complex(a, b)        #gamma: propagation constant

GL = np.complex(-1.0/5.0,0) #\Gamma_L: load reflection coefficient
GG = (ZG-Z0)/(ZG+Z0)        #\Gamma_G: generator reflection coefficient
L  = 10                     #Length of the transmission line

o = np.pi/4                 #omega
I = 20                      #Interval between frames


#The line names are a mess right now, sorry!
fig = plt.figure()
ax = plt.axes(xlim=(-1, L+1), ylim=(-abs(2*VG), abs(2*VG)))
line1, = ax.plot([], [], lw=1, color='#FF7F00')
line2, = ax.plot([], [], lw=1, color='#654CFF')
line3, = ax.plot([], [], lw=1, color='#FF7F00')
line4, = ax.plot([], [], lw=1, color='#FF4D8E')
line5, = ax.plot([], [], lw=1, color='#4DFF64')
line6, = ax.plot([], [], lw=1, color='#4DFF64')
line7, = ax.plot([], [], lw=4, color='#654CFF')
line8, = ax.plot([], [], lw=1, color='#FF4D8E')

def init():
    line1.set_data([], [])
    line2.set_data([], [])
    line3.set_data([], [])
    line4.set_data([], [])
    line5.set_data([], [])
    line6.set_data([], [])
    line7.set_data([], [])
    line8.set_data([], [])
    return line1, line2, line3, line4, line5, line6, line7, line8

def animate(k):
    t = 0.001*I*k
    x = np.linspace(0, L, 10000)
    
    #vp: voltage propagated towards load (v+)
    vp = ((VG*Z0/(Z0+ZG)) *
          (e(-g*x))/(1 - GG*GL*e(-2*g*L))*e(j*o*t)).real
    
    #ip: current propagated towards load (i+)
    ip = ((VG/(Z0+ZG)) *
          (e(-g*x))/(1 - GG*GL*e(-2*g*L))*e(j*o*t)).real
    
    #Vf: Voltage phasor
    Vf = ((VG*Z0/(Z0+ZG)) *
          (e(-g*x) + GL*e(-2*g*L)*e(g*x))/(1 - GG*GL*e(-2*g*L)))
          
    #If: Current phasor
    If = ((VG/(Z0+ZG)) *
          (e(-g*x) - GL*e(-2*g*L)*e(g*x))/(1 - GG*GL*e(-2*g*L)))
    
    #|Vf|
    magVf = abs(Vf*e(j*o*t))
    
    #Voltage on the line v(x, t)
    v = (Vf*e(j*o*t)).real
  
    #|If|
    magIf = abs(If*e(j*o*t))
    
    #Current on the line i(x, t)
    i = (If*e(j*o*t)).real
    
    line1.set_data(x, magVf)
    line3.set_data(x, -magVf)
    line2.set_data(x, v)
    line4.set_data(x, i)
    line5.set_data(x, magIf)
    line6.set_data(x, -magIf)
    #line7.set_data(x, vp)
    #line8.set_data(x, ip)
    return line1, line2, line3, line4, line5, line6, line7, line8

anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=400, interval=I, blit=True)
plt.show()


