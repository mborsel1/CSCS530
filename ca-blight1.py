import matplotlib
matplotlib.use('TkAgg')

import pylab as PL
import random as RD
import scipy as SP
import numpy as NP

RD.seed()

width = 50
height = 50
initProb = 0.001 #probability of starting with infection
blightRate = 0.1 #rate of blight spread to nearby city blocks
recoveryRate = 0.2 #rate of regrowth of blighted city blocks
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
            else:
                state = 0
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
            counter = 0

            if state < 1:
                for dx in xrange(-1, 2):
                    for dy in xrange(-1, 2):
                        if 0 < y+dy < height - 1: #boundary condition
                            if 0 < x+dx < width - 1:
                                aval += config[(y+dy)%height, (x+dx)%width]
                state = aval / 9
                if RD.random() < 0.5:
                    if RD.random() < blightRate:
                        state = state + 0.15
                        if state > 1:
                            state = 1
                else:
                    if RD.random() < recoveryRate:
                        state = state - 0.1
                        if state < 0:
                            state = 0
                
            else:
                if counter == 5:
                    state = 0.95
                    counter = 0
                else:
                    counter += 1
            
            btotal += config[(y+dy)%height, (x+dx)%width]
            percent_blighted = btotal / (height * width)               
                            
                            

    
    
#                                if config[(y+dy)%height, (x+dx)%width] == 1:
#                                   # print y+dy%height
#                                   #state = mean value of all surrounding cells
#                                   #or, state = mean value of all surround cells +- x
#                                   #or, state = value of one random neighbor
#                                    if RD.random() < recoveryRate:
#                                        state = 1
#                                elif config[(y+dy)%height, (x+dx)%width] == 2:
#                                    if RD.random() < blightRate:
#                                        state = 2
                                        
                                
#            elif state == 1:
#                for dx in xrange(-1, 2):
#                    for dy in xrange(-1, 2):
#                        if 0 < y+dy < height - 1:
#                            if 0 < x+dx < width - 1:
#                                if config[(y+dy)%height, (x+dx)%width] == 2:
#                                    if RD.random() < blightRate:
#                                        state = 2
                                        
                                
#            else:
#                if counter == 1:
#                    state = 0
#                    counter = 0
#                else:
#                    counter += 1

#    percent_blighted = #sum of all cell values / (height*width) *100.0
            nextConfig[y, x] = state

    config, nextConfig = nextConfig, config

import pycxsimulator
pSetters = [bRate, rRate]
pycxsimulator.GUI(parameterSetters = pSetters).start(func = [init,draw,step])#(parameterSetters = pSetters).start(func=[init,draw,step])
