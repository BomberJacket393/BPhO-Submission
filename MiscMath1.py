import math

class MiscMath1:
    def pythag(x,y): return ((x**2)+(y**2))**0.5
    def pythag(vector): return ((vector[0]**2)+(vector[1]**2))**0.5
    def sf(x): return round(x,2)
    def roundUp(x): return int(math.ceil(x/5)*5)
    def ln(x): 
        if x==0: return 0
        return math.log(abs(x))
