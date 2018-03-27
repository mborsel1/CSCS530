import matplotlib
matplotlib.use('TkAgg')

import pylab as PL
import random as RD
import scipy as SP

RD.seed()

width = 30
height = 30
initProb = 0.005 #probability of starting with infection
blightRate = 0.25 #rate of blight spread to nearby city blocks
recoveryRate = 0.15 #rate of regrowth of blighted city blocks
percent_blighted = float('nan')

def bRate (val = blightRate): #rate of blight spread to nearby city blocks, parameter can be changed in model

    global blightRate
    blightRate = float(val)
    return val

def rRate (val = recoveryRate): #rate of recovery of blighted city blocks, parameter can be changed in model
 
    global recoveryRate
    recoveryRate = float(val)
    return val

def init():
    global time, config, nextConfig

    time = 0
    
    config = SP.zeros([height, width])
    for x in xrange(width):
        for y in xrange(height):
            if RD.random() < initProb:
                state = 1
            elif initProb < RD.random() < initProb + initProb:
                state = 0.6
            elif initProb + initProb < RD.random() < initProb + initProb + initProb:
                state = 0.25
            else:
                state = 0.1
            config[y, x] = state

    nextConfig = SP.zeros([height, width])

def draw():
    PL.cla()
    PL.pcolor(config, vmin = 0, vmax = 1, cmap = PL.cm.jet)
    PL.axis('image')
#    PL.title('t = ' + str(time))
    message = r't = {0}     blighted: {1}%'
    blighted_pct = round(100*percent_blighted, 2)  
    PL.title(message.format(time, blighted_pct))

def step():
    global time, config, nextConfig, percent_blighted

    time += 1
    btotal = 0
    
    for x in xrange(width):
        for y in xrange(height):
            state = config[y, x]
            
            aval = 0
            bval = 0
            cval = 0
            dval = 0

            if state < 1:
                for dx in xrange(-1, 2):
                    for dy in xrange(-1, 2):
                        if 0 < y+dy < height - 1: #boundary condition
                            if 0 < x+dx < width - 1:
                                aval += config[(y+dy)%height, (x+dx)%width]
                                
                for ddx in xrange(-2,3):
                    for ddy in xrange(-2,3):
                        if 0 < y+ddy < height-1:
                            if 0 < x+ddx < width - 1:
                                bval += config[(y+ddy)%height, (x+ddx)%width]
                                
                cval = bval - aval
                dval = aval / 9                
                state = ((dval * 2) + (cval / 16)) / 3
                
                if RD.random() < 0.4:
                    if RD.random() < blightRate:
                        state = state + 0.1
                        if state > 1:
                            state = 1
                else:
                    if RD.random() < recoveryRate:
                        state = state - 0.35
                        if state < 0:
                            state = 0


            if state == 1:
                if RD.random() < 0.005:
                    state = 0
#                elif RD.random() < 0.01:
#                    state = 0.75
#            if 0.75 < state < 1:
#                if RD.random() < 0.1:
#                    state = 1
#            if 0.5 < state < .75:
#                if RD.random() < 0.1:
#                    state = .8
            if state == 0:
                if RD.random() < 0.0005:
                    state = 1
#            else:             
#                if counter == 5:
#                    state = 0.95
#                    counter = 0
#                else:
#                    counter += 1
            
            #btotal += config[(y+dy)%height, (x+dx)%width]
            btotal += config[y, x]
            percent_blighted = btotal / (height * width)               
                            

            nextConfig[y, x] = state

    config, nextConfig = nextConfig, config

import pycxsimulator
pSetters = [bRate, rRate]
pycxsimulator.GUI(parameterSetters = pSetters).start(func = [init,draw,step])#(parameterSetters = pSetters).start(func=[init,draw,step])
