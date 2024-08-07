import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
from matplotlib import pyplot as plt, animation
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from mpl_toolkits.mplot3d import axes3d, Axes3D
import PIL
import math
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
import time


class earthParticle:

    def __init__(self,longAndLat,velocity=100,verAngle=90,horAngle=0,acceleration=(0,0,0),g=-9.81):
        x,y,z = self.longLatToCart(longAndLat)
        self.position = np.array([x,y,z])
        perVector = self.perpendicularVector(self.position)
        self.velocity = self.velocityFromTangent(self.position,perVector,verAngle,horAngle,velocity)
        ##self.velocity = np.array(velocity)
        self.acceleration = np.array(acceleration)
        self.initialPos = self.position
        self.finalPos = None
        self.g=g
        self.xpoints = []
        self.ypoints = []
        self.zpoints = []
        self.xSprintPoints = []
        self.ySprintPoints = []
        self.zSprintPoints = []
        self.apogeeVector = (x,y,z)
        self.sprintCount = 0
        self.pointID = 0
        self.collision = False
        self.anim = animation.FuncAnimation(fig,self.update,interval=50,cache_frame_data=False)
        self.pause = False
        self.interface = None
        self.resetFirstFrame = True
        ##print(f"Directional: {self.position}\nPerpendicular: {perVector}\nVelocity: {self.velocity}")

    def update(self,frame=None):
        self.getInterface()
        if self.pause==False:
            ax.set_xlabel('x (m*10^3)')
            ax.set_ylabel('y (m*10^3)')
            ax.set_zlabel('z (m*10^3)')
            ##print(f"\nSprint Points X: {len(self.xSprintPoints)}")
            ##print(self.xSprintPoints)
            ##print("\n")
            if self.sprintCount<=0 and self.collision==False:
                print("Sprint")
                self.resetFirstFrame=False
                for i in range(5000):             
                    self.xSprintPoints.append(self.position[0])
                    self.ySprintPoints.append(self.position[1])
                    self.zSprintPoints.append(self.position[2])
                    self.position, self.velocity, self.acceleration = VerletMethod.getParticle(self.position,self.velocity,self.acceleration,0.2,g=self.g)
                    self.sprintCount+=1
                    #if self.vectorMag(self.position)>self.vectorMag(self.apogeeVector):
                    #    self.apogeeVector = self.position
                    if self.withinPlanet(): 
                        ##print("Planet Collision: ",end="")
                        self.collision = True
                        self.finalPos=(self.position[0],self.position[1],self.position[2])
                        self.finalLongLat=self.cartToLongLat(self.finalPos)
                        self.interface.updateModelInfo()
                        break
                ##print("Sprint Finished")
            if self.resetFirstFrame==False:
                for i in range(50):
                    try:
                        self.xpoints.append(self.xSprintPoints[self.pointID])
                        self.ypoints.append(self.ySprintPoints[self.pointID])
                        self.zpoints.append(self.zSprintPoints[self.pointID])
                        self.sprintCount-=1
                        self.pointID+=1
                    except: 
                        break
            ax.clear()
            ax.plot(self.xpoints,self.ypoints,self.zpoints)
            self.plotSigPoints()
            plotPlanet()
            ax.axes.set_xlim3d(left=-radius*2, right=radius*2) 
            ax.axes.set_ylim3d(bottom=-radius*2, top=radius*2) 
            ax.axes.set_zlim3d(bottom=-radius*2, top=radius*2)    
        fig.canvas.draw()

    def withinPlanet(self):
        return self.posVectorMag()<(radius-1)

    def posVectorMag(self):
        return (np.sum(np.square(self.position))**0.5)

    def vectorMag(self,vector):
        return (np.sum(np.square(vector))**0.5)

    def plotSigPoints(self):
        ax.scatter(self.initialPos[0],self.initialPos[1],self.initialPos[2],s=75,marker='o')
        if self.finalPos!=None:
            ax.scatter(self.finalPos[0],self.finalPos[1],self.finalPos[2],s=75,marker='o',c="#ff7f0e")

    def dirVector(self,vector):
        mag = self.vectorMag(vector)
        for i,point in enumerate(vector):
            vector[i]/=mag
        return np.array(vector)

    def longLatToCart(self,coords):
        print(coords)
        x = radius*math.cos(math.radians(coords[1]))*math.cos(math.radians(coords[0]))
        y = radius*math.cos(math.radians(coords[1]))*math.sin(math.radians(coords[0]))
        z = radius*math.sin(math.radians(coords[1]))
        return x,y,z

    def cartToLongLat(self,position):
        lat = math.degrees(math.asin(position[2]/radius))
        lon = math.degrees(math.atan2(position[1], position[0]))
        ##print("Called")
        return lat,lon

    def getInterface(self):
        self.interface = getInterface()

    def reset(self, longAndLat,vel,verAngle,horAngle,g):
        ax.clear()
        x,y,z = self.longLatToCart(longAndLat)
        self.position = np.array([x,y,z])
        self.initialPos = self.position
        perVector = self.perpendicularVector(self.position)
        self.velocity = self.velocityFromTangent(self.position,perVector,verAngle,horAngle,vel)
        ##self.velocity = np.array(vel)
        self.finalPos = None
        self.g=g
        self.xpoints = []
        self.ypoints = []
        self.zpoints = []
        self.xSprintPoints = []
        self.ySprintPoints = []
        self.zSprintPoints = []
        self.sprintCount = 0
        self.pointID = 0
        self.collision = False
        ##print(f"Directional: {self.position}\nPerp-Directoinal: {dirVector}")

    def perpendicularVector(self, vector):
        if vector[0] == -1 and vector[1] == 1:
            return np.array([vector[0]-vector[1],vector[2],vector[2]])
        return np.array([vector[2],vector[2],vector[0]-vector[1]])

    def perpendicularVector2(self, vector):
        print(f"Pre-transform vector: {vector}")
        return np.array([vector[0],vector[1]-vector[2],vector[0]])

    def idle(self,t=3):
        pass
        ##plt.pause(t)

    def velocityFromTangent(self, tangentPosVector, perVector,verAngle,horAngle,velocity):
        tangentMag = self.vectorMag(tangentPosVector)
        perVectorMag = self.vectorMag(perVector)
        ratio = math.tan(math.radians(verAngle))*(perVectorMag)/tangentMag
        velVerDirection = perVector+(tangentPosVector*ratio)
        velVector = self.dirVector(velVerDirection)*velocity
        return velVector
        

class VerletMethod:
    ##F = acting forces
    ##All motion variables are 3D vectors
    def getParticle(pos,v,a,h,g):
        deltaSquareT = h*h
        pos1=VerletMethod.updatePosition(pos,v,a,h,deltaSquareT)
        v1=VerletMethod.updateVelocity(v,a,h)
        a1=VerletMethod.updateAcceleration(pos,g)
        #print("\n----------------------------------------------\n")
        #print(f"Position Vector: {pos1}")
        #print(f"Velocity Vector: {v1}")
        #print(f"Acceleration Vector: {a1}")
        #print("\n----------------------------------------------\n")
        return np.array(pos1),np.array(v1),np.array(a1)

    def updatePosition(pos,v,a,h,dt2):
        pos1 = []
        for index in range(len(pos)):
            pos1.append(pos[index]+(v[index]*h)+(0.5*a[index]*h*h))
        return pos1
    
    ##dt2 = Change in time squared
    def updateVelocity(v,a,h):
        v1=[]
        for index,pointVelocity in enumerate(v):
            v1.append(pointVelocity+a[index]*h)
        return v1

    def updateAcceleration(pos,g):
        sqSum = 0
        for axis in pos:
            sqSum+=axis**2
        mag=sqSum**0.5
        dirVec = []
        for axis in pos:
            if axis==0: dirVec.append(0)
            else:
                #6371008
                #9.80665 m/s
                ##acceleration = g*(6*(10**23))/(particle.posVectorMag()**2)
                ##acceleration = g*((radius/(radius+particle.posVectorMag())**2))
                acceleration=g
                dirVec.append(axis/mag*acceleration)
        return dirVec

def plotPlanet():
    ax.plot_surface(x,y,z, rstride=4, cstride=4, facecolors = bm)

class Interface:

    def __init__(self,particle):
        self.particle = particle

        self.inputTabMaster= ctk.CTkTabview(window,width=700,height=1000,command=self.updateModelInfo)
        self.inputTabMaster.pack(side=ctk.LEFT,padx=20,pady=10,anchor="nw")
        self.inputTabMaster.add("Model Controls")
        self.infoTabMaster= ctk.CTkTabview(window,width=700,height=1000,command=self.updateModelInfo)
        self.infoTabMaster.pack(side=ctk.RIGHT,padx=20,pady=10,anchor="nw")
        self.infoTabMaster.add("Model Info")

        self.latHolder = ctk.CTkFrame(self.inputTabMaster.tab("Model Controls"),width=200,height=30)
        self.latHolder.pack(side=ctk.TOP,padx=5,pady=5)
        self.latLabel=ctk.CTkLabel(self.latHolder,text=f"Latitude (°): {0}",font=("Roboto",20))
        self.latLabel.pack(side=ctk.LEFT,padx=5,pady=5)
        self.latSlider = ctk.CTkSlider(master=self.latHolder, from_=-180, to=180, command=self.updateInputs)
        self.latSlider.pack(side=ctk.RIGHT,padx=5,pady=5)

        self.longHolder = ctk.CTkFrame(self.inputTabMaster.tab("Model Controls"),width=200,height=20)
        self.longHolder.pack(side=ctk.TOP,padx=5,pady=5)
        self.longLabel=ctk.CTkLabel(self.longHolder,text=f"Longtitude (°): {0}",font=("Roboto",20))
        self.longLabel.pack(side=ctk.LEFT,padx=5,pady=5)
        self.longSlider = ctk.CTkSlider(master=self.longHolder, from_=-90, to=90, command=self.updateInputs)
        self.longSlider.pack(side=ctk.RIGHT,padx=5,pady=5)

        self.gravHolder = ctk.CTkFrame(self.inputTabMaster.tab("Model Controls"),width=500,height=20)
        self.gravHolder.pack(side=ctk.TOP,padx=5,pady=5)
        self.gravLabel=ctk.CTkLabel(self.gravHolder,text=f"G (ms⁻²): {3.7}",font=("Roboto",20))
        self.gravLabel.pack(side=ctk.LEFT,padx=5,pady=5)
        self.gravSlider = ctk.CTkSlider(master=self.gravHolder, from_=0.1, to=20, command=self.updateInputs,number_of_steps=100)
        self.gravSlider.pack(side=ctk.RIGHT,padx=5,pady=5)
        self.gravSlider.set(3.72)


        self.velHolder = ctk.CTkFrame(self.inputTabMaster.tab("Model Controls"),width=500,height=20)
        self.velHolder.pack(side=ctk.TOP,padx=5,pady=5)
        self.velLabel=ctk.CTkLabel(self.velHolder,text=f"Velocity (kms⁻¹): ",font=("Roboto",20))
        self.velLabel.pack(side=ctk.LEFT,padx=5,pady=5)
        self.velEntry = ctk.CTkEntry(master=self.velHolder,placeholder_text="100")
        self.velEntry.pack(side=ctk.RIGHT,padx=5,pady=5)

        self.tangentAngleHolder = ctk.CTkFrame(self.inputTabMaster.tab("Model Controls"),width=500,height=20)
        self.tangentAngleHolder.pack(side=ctk.TOP,padx=5,pady=5)
        self.tangentAngleLabel=ctk.CTkLabel(self.tangentAngleHolder,text=f"Ver. Launch Angle (°): {30}",font=("Roboto",20))
        self.tangentAngleLabel.pack(side=ctk.LEFT,padx=5,pady=5)
        self.tangentAngleSlider = ctk.CTkSlider(master=self.tangentAngleHolder, from_=0, to=90, command=self.updateInputs,number_of_steps=180)
        self.tangentAngleSlider.pack(side=ctk.RIGHT,padx=5,pady=5)
        self.tangentAngleSlider.set(90)

        self.horAngleHolder = ctk.CTkFrame(self.inputTabMaster.tab("Model Controls"),width=500,height=20)
        self.horAngleHolder.pack(side=ctk.TOP,padx=5,pady=5)
        self.horAngleLabel=ctk.CTkLabel(self.horAngleHolder,text=f"Hor. Launch Angle (°): {0}",font=("Roboto",20))
        self.horAngleLabel.pack(side=ctk.LEFT,padx=5,pady=5)
        self.horAngleSlider = ctk.CTkSlider(master=self.horAngleHolder, from_=-180, to=180, command=self.updateInputs,number_of_steps=720)
        self.horAngleSlider.pack(side=ctk.RIGHT,padx=5,pady=5)
        self.horAngleSlider.set(0)


        self.initialLongLatInfoHolder = ctk.CTkFrame(self.infoTabMaster.tab("Model Info"),fg_color="#333333")
        self.initialLongLatInfoHolder.pack(side=ctk.TOP,padx=10,pady=10)

        self.initialLongLatInfoLabel=ctk.CTkLabel(self.initialLongLatInfoHolder,text=f"Initial Coordinates",font=("Roboto",25,'bold'))
        self.initialLongLatInfoLabel.pack(side=ctk.TOP,padx=5,pady=5)

        self.initialLatInfoHolder = ctk.CTkFrame(self.initialLongLatInfoHolder,width=200,height=30,fg_color="#1F1F29")
        self.initialLatInfoHolder.pack(side=ctk.TOP,padx=5,pady=5)
        self.initialLatInfoLabel=ctk.CTkLabel(self.initialLatInfoHolder,text=f"Latitude (°): 0",font=("Roboto",20))
        self.initialLatInfoLabel.pack(side=ctk.LEFT,padx=5,pady=5)

        self.initialLongInfoHolder = ctk.CTkFrame(self.initialLongLatInfoHolder,width=200,height=30,fg_color="#1F1F29")
        self.initialLongInfoHolder.pack(side=ctk.TOP,padx=5,pady=5)
        self.initialLongInfoLabel=ctk.CTkLabel(self.initialLongInfoHolder,text=f"Longtitude (°): 0",font=("Roboto",20))
        self.initialLongInfoLabel.pack(side=ctk.LEFT,padx=5,pady=5)

        self.finalLongLatInfoHolder = ctk.CTkFrame(self.infoTabMaster.tab("Model Info"),fg_color="#333333")
        self.finalLongLatInfoHolder.pack(side=ctk.TOP,padx=10,pady=10)

        self.finalLongLatInfoLabel=ctk.CTkLabel(self.finalLongLatInfoHolder,text=f"final Coordinates",font=("Roboto",25,'bold'))
        self.finalLongLatInfoLabel.pack(side=ctk.TOP,padx=5,pady=5)

        self.finalLatInfoHolder = ctk.CTkFrame(self.finalLongLatInfoHolder,width=200,height=30,fg_color="#1F1F29")
        self.finalLatInfoHolder.pack(side=ctk.TOP,padx=5,pady=5)
        self.finalLatInfoLabel=ctk.CTkLabel(self.finalLatInfoHolder,text=f"Latitude (°): 0",font=("Roboto",20))
        self.finalLatInfoLabel.pack(side=ctk.LEFT,padx=5,pady=5)

        self.finalLongInfoHolder = ctk.CTkFrame(self.finalLongLatInfoHolder,width=200,height=30,fg_color="#1F1F29")
        self.finalLongInfoHolder.pack(side=ctk.TOP,padx=5,pady=5)
        self.finalLongInfoLabel=ctk.CTkLabel(self.finalLongInfoHolder,text=f"Longtitude (°): 0",font=("Roboto",20))
        self.finalLongInfoLabel.pack(side=ctk.LEFT,padx=5,pady=5)


        self.replayAnimationButton = ctk.CTkButton(self.inputTabMaster.tab("Model Controls"),text="Reset Model",
                                            font=("Roboto",25),
                                            command=self.resetAnimation,
                                            hover=True)
        self.replayAnimationButton.pack(side=ctk.TOP,padx=10,pady=1)

        self.pauseAnimationButton = ctk.CTkButton(self.inputTabMaster.tab("Model Controls"),text="Pause",
                                            font=("Roboto",25),
                                            command=self.pauseAnimation,
                                            hover=True)
        self.pauseAnimationButton.pack(side=ctk.TOP,padx=10,pady=1)

    def updateModelInfo(self):
        self.finalLatInfoLabel.configure(text=f"Latitude (°): {int(particle.finalLongLat[1])}")
        self.finalLongInfoLabel.configure(text=f"Longtitude (°): {int(particle.finalLongLat[0])}")
    
    def updateInputs(self,value=None):
        particle.idle(0.2)
        self.latLabel.configure(text=f"Latitude (°): {int(self.latSlider.get())}")
        self.longLabel.configure(text=f"Longtitude (°): {int(self.longSlider.get())}")
        self.gravLabel.configure(text=f"Gravity (ms⁻²): {sf(self.gravSlider.get())}")
        self.tangentAngleLabel.configure(text=f"Ver. Launch Angle (°): {int(self.tangentAngleSlider.get())}")
        self.horAngleLabel.configure(text=f"Hor. Launch Angle (°): 0")

    def resetAnimation(self):
        particle.idle(0.2)
        long = self.longSlider.get()
        lat = self.latSlider.get()
        g = self.gravSlider.get()
        try:
            velocity = int(self.velEntry.get())
        except:
            velocity = 100
        tangentAngle = self.tangentAngleSlider.get()
        horAngle = self.horAngleSlider.get()
        particle.reset((lat,long),velocity,tangentAngle,horAngle,-g)
        self.initialLatInfoLabel.configure(text=f"Latitude (°): {int(self.latSlider.get())}°")
        self.initialLongInfoLabel.configure(text=f"Longtitude (°): {int(self.longSlider.get())}°")
        self.finalLatInfoLabel.configure(text=f"Latitude (°): N/A")
        self.finalLongInfoLabel.configure(text=f"Longtitude (°): N/A")

    def pauseAnimation(self):
        particle.pause = not particle.pause

    def retrieveKeyInputs(self,event):
        if event.key=="p": self.pauseAnimation()

def sf(x): return round(x,2)

def getInterface():
    return GUI

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.set_aspect('equal')
radius = 33895
ax.axes.set_xlim3d(left=-radius*4, right=radius*4) 
ax.axes.set_ylim3d(bottom=-radius*4, top=radius*4) 
ax.axes.set_zlim3d(bottom=-radius*4, top=radius*4) 

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

# Make data
bm = PIL.Image.open('Mars.jpg')
bm = np.array(bm.resize([d for d in bm.size]))/256
#print(bm.shape)
#lons = np.linspace(-180, 180, bm.shape[1]) * np.pi/180 
#lats = np.linspace(-90, 90, bm.shape[0])[::-1] * np.pi/180

#x = np.outer(np.cos(lons), np.cos(lats)).T
#y = np.outer(np.sin(lons), np.cos(lats)).T
#z = np.outer(np.ones(np.size(lons)), np.sin(lats)).T

u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x = radius * np.outer(np.cos(u), np.sin(v))
y = radius * np.outer(np.sin(u), np.sin(v))
z = radius * np.outer(np.ones(np.size(u)), np.cos(v))

particle = earthParticle((0,0),500,verAngle = 30,g=-3.72)

ax.plot(particle.xpoints,particle.ypoints,particle.zpoints)
##ax.scatter((particle.initialPos[0],particle.finalPos[0]),(particle.initialPos[1],particle.finalPos[1]),(particle.initialPos[2],particle.finalPos[2]),s=40)

window = ctk.CTk()
window.wm_title("BPhO 2024")
ctk.set_appearance_mode("Dark")
canvas = FigureCanvasTkAgg(fig, master=window)


##fig.canvas.mpl_connect('key_press_event', graph.retreivekeyInputs)

toolbar = NavigationToolbar2Tk(canvas, window, pack_toolbar=False)
toolbar.update()

toolbar.pack(side=ctk.BOTTOM, fill=ctk.X)
canvas.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=1)


GUI = Interface(particle)

fig.canvas.mpl_connect('key_press_event', GUI.retrieveKeyInputs)
canvas.draw()
window.update()
window.mainloop()
