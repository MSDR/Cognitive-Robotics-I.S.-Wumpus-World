#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep
from enum import Enum
import math
import os
os.system('setfont Lat15-TerminusBold14')
mL = LargeMotor('outA'); mL.stop_action = 'hold'
mR = LargeMotor('outB'); mR.stop_action = 'hold'
# print('Hello, my name is EV3!')
# Sound.speak('Hello, my name is EV3!').wait()
# mL.run_to_rel_pos(position_sp= 840, speed_sp = 250)
# mR.run_to_rel_pos(position_sp=-840, speed_sp = 250)
# mL.wait_while('running')
# mR.wait_while('running')
# Sensor check
c1=ColorSensor('in1')
c2=ColorSensor('in2')
colors=("unkown", "black", "blue", "green", "yellow", "red", "white", "brown")

class Directions(Enum):
    NORTH = .5*math.pi
    SOUTH = 1.5*math.pi
    EAST = 0
    WEST = math.pi

coords = [0,1]
angle = Directions.EAST

def printBoard():
    print("+-------+")
    for i in range(0,4):
        line = ""
        for j in range(0,4):
            line += "|" + ("R" if coords == [3-i,j] else "#")
        print(line+"|")
    print("+-------+")
    print((str)(coords[0])+" "+(str)(coords[1])+" " + ("NORTH" if angle==Directions.NORTH else "SOUTH" if angle==Directions.SOUTH else "EAST" if angle==Directions.EAST else "WEST"))
    print(" ")
    return

def updateCoords():
    if(angle == Directions.NORTH or angle == Directions.SOUTH):
        coords[0] += (int)(min(max(math.sin(angle.value),0),3))
    else:
        coords[1] += (int)(min(max(math.cos(angle.value),0),3))

def rotateTo(direction):
    global angle
    rotate(direction.value-angle.value)
            #rotate(1)
    angle = direction

def rotate(i):
    mL.run_to_rel_pos(position_sp= -i*math.pi*51.5, speed_sp = 250)
    mR.run_to_rel_pos(position_sp=  i*math.pi*51.5, speed_sp = 250) #these numbers work lol, don't question it
    mL.wait_while('running')
    mR.wait_while('running')

crossed = 0 #counts how many lines it's crossed since last rotation
passedLine = True #ensures it only counts a line once
while(1==1):
    #for j in range(0,4):
       # print("|" + ("R" if coords == [0,j] else " "))
    printBoard()
    #print("c1:"+(str)(c1.value()))
    #print("c2:"+(str)(c2.value()))
    if((c1.value()-c2.value())>6): #happens when left sensor over white
        print("left")
    elif((c2.value()-c1.value())>6): #when right sensor over white
        print("right")
    else:
        if(passedLine and c1.value()>20): #hit a line
            updateCoords()
            crossed += 1
            passedLine = False
        else:
            passedLine = True
    mL.run_to_rel_pos(position_sp = 100, speed_sp = 100)
    mR.run_to_rel_pos(position_sp = 100, speed_sp = 100)

    if(crossed > 2 and (coords == [0,0] or coords == [0,3] or coords == [3,0] or coords == [3,3])):
        crossed = 0
        mL.run_to_rel_pos(position_sp = 70, speed_sp = 250)
        mR.run_to_rel_pos(position_sp = 70, speed_sp = 250)
        rotateTo(Directions.EAST if angle.value+math.pi*.5 >= 2*math.pi else Directions(angle.value+math.pi*.5))

# while(c1.value()>c2.value() and c1.value() < 30):
#     #Sound.speak(ColorSensor().value()).wait()
#     mL.run_to_rel_pos(position_sp= 500, speed_sp = 300)
#     mR.run_to_rel_pos(position_sp= 500, speed_sp = 300)
#     # mL.wait_while('running')
#     # mR.wait_while('running')
# mL.stop()
# mR.stop()
# Sound.speak("Found it!").wait()
#    if c1.value()==c2.value():
#         if colors[c1.value()]=="black":
#             print("We are on a grid space")
#         elif colors[c1.value()]=="white":
#             print("We are crossing spaces")
#         else:
#             print("I'm a little lost here...")
#     else:
#         print("My right half and my left half are in two different realms!")


