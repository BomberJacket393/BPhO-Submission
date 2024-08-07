import math
import numpy as np
import os
import sys
sys.path.append(os.path.abspath("C:\\...\\MiscMath1"))
from MiscMath1 import *

class Challenge7Particles:
    def __init__(self, velocity, launchAngle, gravity,launchHeight=0,numberOfPoints=10):
        self.launchHeight = launchHeight
        self.inputAngle = math.radians(launchAngle)
        self.velocity = velocity
        self.gravity = gravity
        self.pointCount = numberOfPoints
        self.graphLimitX = 5
        self.graphLimitY = 5
        self.inputAngle = launchAngle
        self.xLabel = "Time: t (s)"
        self.yLabel = "Range: r (m)"

        self.angleValues = [(15,"θ=15°","red"),
                            (30,"θ=30°",(0,0,1)),
                            (45,"θ=45°",(0.5,0,1)),
                            (60,"θ=60°",(1,0.5,1)),
                            (70.529,"θ≈70.5°",(0,0.5,1)),
                            (78,"θ=78°",(0.3,0,1)),
                            (85,"θ=85°","Pink"),
                            [int((self.inputAngle)),f"θ={int((self.inputAngle))}°","Black"]]

    ##--SIMULATION RUNNING-------------------------------------------
    def simulationRefresh(self): 
        ##Changes the input angle
        self.angleValues[-1]=[int(math.degrees(self.inputAngle)),f"θ={int(math.degrees(self.inputAngle))}°","Black"]
        ##Stretch Canvas to fit whole graph
        ##tps = Turning Points
        tps = self.findMinMaxima(self.velocity,self.gravity,80)
        ##(tps)
        mxtps = MiscMath1.roundUp(max(tps[0],tps[1]))
        ytps = MiscMath1.roundUp(self.tRange(self.velocity,self.gravity,80,mxtps))
        self.graphLimitX = mxtps##roundUp(self.getMaxAirTime(self.velocity))+1
        self.graphLimitY = ytps##roundUp(self.maxDisplacementY(self.velocity,-self.gravity))+5

        ##(self.tRange(self.velocity,self.gravity,math.radians(30),2))

    ##--PLOTTING DATA--------------------------------------------------------

        ##Get points holds all of the graph data, inclduing colour, points, name and display messages
    def getPoints(self):
        self.simulationRefresh()
        self.graphPointList = self.getRangePlots(self.velocity,self.angleValues)
        ##(self.graphPointList)
        self.setAllMessages()
        return self.graphPointList

    def getRangePlots(self,v,angles):
        
        self.minMaximaPoints=[]
        self.rangePlots=[] 
        xPoints = self.tPointSpacing(v)
        self.rangeParticleInfo=[]
        ##ANGLE NOT JUST ANGLE! ALSO CONTAINS COLOR AND LABEL OF THAT ANGLE PLOT
        print(angles)
        for angle in angles:
            yPoints = []
            self.rangeParticle=[angle[0]]
            for point in xPoints:
                yPoints.append(self.tRange(self.velocity,self.gravity,math.radians(angle[0]),point))
                ##Finds the t value of the min max point
            minMaxT = self.findMinMaxima(self.velocity,-self.gravity,math.radians(angle[0]))
                ##if one value is complex, both values are
            if not np.iscomplex(minMaxT[0]) or (minMaxT[0]==0 or minMaxT[1]==0):
                tps=[]
                for t in minMaxT:
                    minMaxPoint = [t,self.tRange(self.velocity,self.gravity,math.radians(angle[0]),t),"red"]
                    self.minMaximaPoints.append(minMaxPoint)
                    tps.append(minMaxPoint[:-1])
                    ##print(minMaxPoint[:-1])
                    ##FIXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
                    ##FIX
                    ##FIX
                    ##yPoints[-1]+=(self.tRange(self.velocity,self.gravity,math.radians(angle[0]),minMaxT))
                self.rangeParticle.append(tps)
            else: self.minMaximaPoints.append(None)
            self.rangeParticleInfo.append(self.rangeParticle)
            self.rangePlots.append((xPoints,yPoints,angle[1],angle[2],"o-"))
        return self.rangePlots

    def getDots(self):
        return self.minMaximaPoints

    ##--LABELS--------------------------------------------
    def setAllMessages(self):
        ##self.setParticleText()
        self.displayMessages = [("| General Data |",f"Initial Y displacement: {self.launchHeight}m",
                                f"Vertices: {self.pointCount}",
                                f"g: {abs(self.gravity)}ms⁻²")]

    #--GET MIN AND MAXIMUM VALUES-----------------------------------
        ##Angle not needed, particle shot up at 90 degrees, therefore sin(theta)=1
    def getMaxAirTime(self,v):
        coeffs=[self.gravity,v,self.launchHeight]
        roots = np.roots(coeffs)
        if roots[0]>0: return roots[0]
        else: return roots[1]

    ##Find location of minimum and maximum points
    def findMinMaxima(self,v,g,angle):
        a=1
        b=-(3*v)*math.sin(angle)/g
        c=(2*(v**2))/(g**2)
        coeffs = [a,b,c]
        roots = np.roots(coeffs)
        return roots

    def maxDisplacementY(self, velocity, gravity): return (velocity**2)/(2*gravity)

    ##--POINT SPACING---------------------------------------

        ##Used for the range time graph
    def tPointSpacing(self,velocity):
        tPoints=[]
        max = self.graphLimitX
        for point in range(self.pointCount+1):
            tPoints.append((max/self.pointCount)*point)
        return tPoints
   

    ##--FUNCTIONS FOR FINDING Y POINTS-------------------------------------

        ##X range at time T
    def tRange(self, v, g, angle, t):
        a = v**2
        b = -g*t*v*math.sin(angle)
        c = 0.25*(g**2)*(t**2)
        return ((a-b+c)**0.5)*t

    ##--GENERAL PARTICLE FUNCTIONS--------------------------
    def distanceTravelled(self,velocity, gravity, angle, xPoint):
        #print("Xpoint: ",xPoint)
        coeffPartA = (velocity**2)/(2*gravity)
        coeffPartB = (1+(math.tan(angle)**2))
        coeff = coeffPartA/coeffPartB
        #print("Coeff: ", coeff)
        upperBound = math.tan(angle)
        lowerBoundA = (gravity*xPoint)/(velocity**2)
        lowerBoundB = (1+(math.tan(angle)**2))
        lowerBound = math.tan(angle)-(lowerBoundA*lowerBoundB)
        #print(f"Upper: {upperBound}\nLower: {lowerBound}")
        bounds = [upperBound,lowerBound]
        integrals=[]
        ##CB = Current Bound
        for CB in bounds:
            part1a = ((CB**2)+1)**0.5
            part1b = ln(abs(part1a+(CB)))
            part2 = CB*(part1a)
            integrals.append(part1b+part2)
        #print(f"Integral One: {integrals[0]}\nIntergral Two: {integrals[1]}")
        distanceTravelled = (integrals[0]-integrals[1])*coeff
        return distanceTravelled      
