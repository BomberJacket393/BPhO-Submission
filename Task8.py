import math
import numpy as np
import os
import sys
sys.path.append(os.path.abspath("C:\\...\\MiscMath1"))
sys.path.append(os.path.abspath("C:\\...\\Verlets"))
from MiscMath1 import *
from Verlets import *

class Challenge8Particles:
        ##Basic idea
    def __init__(self, velocity, launchAngle, gravity,launchHeight=0,numberOfPoints=500, timestep=0.005, numberOfBounces = 5, cor = 0.7,GUI=None):
        self.GUI = GUI
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
        self.pointCount = numberOfPoints
        ##Coefficient of restitution 
        self.time=0
        self.step = timestep
        self.intersectionPoints = []
        self.COR = cor
        self.velVector=[]
        self.accVector=[]
        

    ##--SIMULATION RUNNING-------------------------------------------
    def simulationRefresh(self):
        self.step = self.GUI.verletStepValue
        self.bounceLimit=self.GUI.verletBounceValue
        ##Stretch Canvas to fit whole graphA
        if self.launchHeight==0: self.intersectionPoints.append(0)
        self.velVector = [self.velocity*math.cos(self.inputAngle),
                     self.velocity*math.sin(self.inputAngle)]
        self.accVector = [0,self.gravity]
        
        ##self.totalFlightTime = self.totalTime(self.launchHeight)
        ##self.totalDisplacement = self.getTotalDisplacement(self.totalFlightTime)
        ##print(self.totalDisplacement)
        ##print(f"Displacement Sum: {self.displacementSum}")
        
        self.point = (0,self.launchHeight)

    ##--PLOTTING DATA--------------------------------------------------------
        ##Get points holds all of the graph data, inclduing colour, points, name and display messages
    def getPoints(self):
        graphPointList = []
        yPoints = []
        self.simulationRefresh()
        
        graphPointList = self.getPlots()
        self.setAllMessages()
        return graphPointList

        ##Get plots feeds into get points
    def getPlots(self):
        plots=[]
        self.verletMethod()
        self.setIntervalPoints()
        plots.append((self.xPoints,self.yPoints,"Bouncing Ball","red","o-"))
        return plots

    def getDots(self):
        dots = []

        return dots

    ##--LABELS--------------------------------------------
    def setAllMessages(self):
        self.setParticleText()
        self.displayMessages = [("| General Data |",f"Initial Y displacement: {self.launchHeight}m",  
                                f"Time Step: {self.step}s",
                                f"Vertices: {len(self.xPoints)}\n"
                                f"g: {abs(self.gravity)}ms⁻²",
                                f"v: {MiscMath1.sf(self.velocity)}ms⁻¹",
                                f"θ: {MiscMath1.sf(math.degrees(self.inputAngle))}°",
                                f"Displacement: {MiscMath1.sf(self.totalDisplacement)}m",
                                f"Flight Time: {MiscMath1.sf(self.time)}s",     
                                f"Bounces: {self.bounceLimit}")]

    def setParticleText(self):
        ##Write all text as a tuple, each value corresponding to a parabola attribute
        pass

    ##--THE METHOD--------------------------
    def verletMethod(self):
        #velVector = [v*math.cos(angle),v*math.sin(angle)]
        #accVector = [0,self.gravity]
        self.graphLimitY = MiscMath1.roundUp(self.greatestTurningPoint(self.launchHeight))+5
        ##self.bounceTime(self.velVector,accVector)
        self.xPoints=[self.point[0]]
        self.yPoints=[self.point[1]]
        self.time=0
        for parabolaIndex in range(self.bounceLimit+1):
            while True:              
                self.verlet = Verlet.getParticle(self.point,self.velVector,self.accVector,self.step)
                if self.verlet[0][1]>0:
                    self.time+=self.step
                    self.point=self.verlet[0]
                    self.velVector=self.verlet[1]
                    self.accVector=self.verlet[2]
                    self.xPoints.append(self.verlet[0][0])
                    self.yPoints.append(self.verlet[0][1])
                else:
                    break
            self.bounceVelocity()
        self.totalDisplacement = self.getTotalDisplacement(self.time)
        ##print(self.totalDisplacement)
        self.graphLimitX = MiscMath1.roundUp(self.totalDisplacement)+5

        ##Bounce
    def bounceVelocity(self):
        self.velVector[1]=-self.velVector[1]*self.COR

    ##--TIME AND DISPLACEMENT------------------------------
    def greatestTurningPoint(self,h=0):
        return ((-(self.velVector[1]**2))/(2*self.accVector[1]))+h

    def bounceTime(self,h=0):
        coeffs = [0.5*self.accVector[1],self.velVector[1],h]
        for root in np.roots(coeffs):
            if root>0: 
                return root
            else: return root

    def totalTime(self, h):
        total=self.bounceTime(h)
        for i in range(self.bounceLimit):
            self.velVector[1]*=self.COR
            total+=self.bounceTime()
            #print(self.bounceTime(self.velVector,accVector))
        #
        return total

        ##Finds the point of the bounce (x-intersect)
        ##Differs from previous as it uses vector
    def bounceDisplacement(self,h=0):
        velocity = pythag(self.velVector)
        angle = math.atan(self.velVector[1]/self.velVector[0])
        ##THIS FORMULA IS WRONG!!!!!!!!
        a = (self.accVector[1]*(1+(math.tan(angle)**2)))/(2*(velocity**2))
        b = math.tan(angle)
        c = h
        coeff = [a,b,c]     
        for root in np.roots(coeff):
            if root>0: return root

    def getTotalDisplacement(self,totalTime):
        return self.velVector[0]*totalTime

    ##--POINT SPACING---------------------------------------

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
