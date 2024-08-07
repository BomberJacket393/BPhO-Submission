import math
import numpy as np
import sys
import os
sys.path.append(os.path.abspath("C\\...\\Verlets"))
from MiscMath1 import *
from Verlets import *

class ExChallenge1Particles:
        ##Basic idea
    def __init__(self, velocity, launchAngle, gravity,launchHeight=0,numberOfPoints=1000, timestep=0.005, numberOfBounces = 0, cor = 0.7):
        self.launchHeight = launchHeight
        self.inputAngle = math.radians(launchAngle)
        self.velocity = velocity
        self.gravity = gravity
        self.pointCount = numberOfPoints
        self.displayMessages = []
        self.graphLimitX = 105
        self.graphLimitY = 105   
        self.xLabel = "Displacement X: x (m)"
        self.yLabel = "Displacement Y: y (m)"
        self.bounceLimit = numberOfBounces
        ##Coefficient of restitution 
        self.time=0
        self.step = timestep
        self.intersectionPoints = []
        self.COR = cor
        self.velVector=[0,0]
        self.accVector=[0,0]

        self.pointCount = numberOfPoints
       
        self.dragCoefficient = 0.3
        self.crossArea = 0.002
        self.fluidDensity = 1
        self.mass = 0.01
        self.baseK = (self.crossArea*self.dragCoefficient)/(2*self.mass)
        self.k=self.baseK*self.fluidDensity

    ##--SIMULATION RUNNING-------------------------------------------
    def simulationRefresh(self):
        self.time=0
        self.xPoints,self.yPoints=[],[]
        self.totalDisplacement = 0
        self.totalFlightTime = 0
        ##Stretch Canvas to fit whole graphA
        if self.launchHeight==0: self.intersectionPoints.append(0)
        self.velVector = [self.velocity*math.cos(self.inputAngle),
                          self.velocity*math.sin(self.inputAngle)]
        self.setFluidAcceleration()
        
        
        ##self.totalFlightTime.append(self.totalTime(self.launchHeight))
        ##self.totalDisplacement.append(self.getTotalDisplacement(self.totalFlightTime))
        
    ##--PLOTTING DATA--------------------------------------------------------
        ##Get points holds all of the graph data, inclduing colour, points, name and display messages
    def getPoints(self):
        graphPointList = []
        yPoints = []
        self.simulationRefresh()
        
        graphPointList = self.getPlots()
        return graphPointList

        ##Get plots feeds into get points
    def getPlots(self):
        self.verletMethod()
        self.setIntervalPoints()
        return [(self.xPoints,self.yPoints,"Non-linear resistance",(0.5,0.5,0),"--"),]

    def getDots(self):
        return []

    ##Split points from time step into number of points set in init parameter
    def setIntervalPoints(self):
        tValues = len(self.xPoints)
        interval = tValues//self.pointCount
        if interval<=0: interval=1
        points = [self.xPoints,self.yPoints]
        for index in range(2):
            self.tempPoints = []
            for i in range(0,tValues,interval):
                self.tempPoints.append(points[index][i])
            self.tempPoints.append(points[index][-1])
            points[index]=self.tempPoints
        self.xPoints,self.yPoints = points[0],points[1]
        
    ##--THE METHOD--------------------------
    def verletMethod(self):
        self.point = [0,self.launchHeight]
        self.graphLimitY = MiscMath1.roundUp(self.greatestTurningPoint(self.launchHeight))+5
        self.xPoints.append(0)
        self.yPoints.append(self.launchHeight)

        self.yDisplacementMax=0

        ##Both figures have same starting point
        while self.point[1]>=0:      
            self.verlet = ResistanceVerlet.getParticle(self.point,self.velVector,self.accVector,self.step)
            self.point=self.verlet[0]
            self.k=self.getResistanceCoefficient()
            self.accVector=self.setFluidAcceleration()
            self.velVector=self.verlet[1]
            self.xPoints.append(self.point[0])
            self.yPoints.append(self.point[1])
            if self.yPoints[-2]>self.yPoints[-1] and self.yDisplacementMax==0: self.yDisplacementMax=self.yPoints[-2]
            self.time+=self.step
        self.totalDisplacement=self.xPoints[-1]
        ##self.totalDisplacement)
        self.graphLimitX = MiscMath1.roundUp(self.totalDisplacement)+5
        self.graphLimitY = MiscMath1.roundUp(self.yDisplacementMax)+5

    def setFluidAcceleration(self): 
        return (-self.velVector[0]*MiscMath1.pythag(self.velVector)*self.k,self.gravity-self.velVector[1]*MiscMath1.pythag(self.velVector)*self.k)

        ##Bounce
    def bounceVelocity(self):
        self.velVector[1]=self.velVector[1]*-self.COR

    ##--TIME AND DISPLACEMENT------------------------------
    def greatestTurningPoint(self,h=0):
        return ((-(self.velVector[1]**2))/(2*self.gravity))+h

    def getTotalDisplacement(self,totalTime):
        return self.velVector[0]*totalTime
    
    def getResistanceCoefficient(self):
        self.setFluidDensity()
        return self.baseK*self.fluidDensity
        
    def setFluidDensity(self):
        ##Function ripped from http://spiff.rit.edu/classes/phys317/lectures/multiple_funcs/temp_profile.html
        ##self.point[1] is the current y value
        ##Starts at 1
        ##(math.exp(-self.point[1]/8000))
        self.fluidDensity= 1.21*(math.exp(-self.point[1]/8000))

