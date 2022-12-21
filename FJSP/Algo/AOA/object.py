from numpy import random
import enum
class Object:
    def __init__(self,position,acc):
        self.position = position
        self.density = random.rand()
        self.volume = random.rand()
        self.acceleration = acc
        self.fitness = 0

    def setDensity(self,density):
        self.density = density

    def setVolume(self,volume):
        self.volume = volume

    def setScore(self,fitness):
        self.fitness = fitness


class Limit:
    def __init__(self,lowerBound,upperBound):
        self.lowerBound = lowerBound
        self.upperBound = upperBound

class Fitness(enum.Enum):
    Single_obj = True
    Multi_obj = False
