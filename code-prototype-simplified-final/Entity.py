import random

class EntityInstance: # use OOP paradigm for each entity type
    def __init__(self, etType, etDPS, etDist, pr, etHealth, etUCT):
        # Entity stats
        self.uniqueRef = random.randint(0, 1024)
        self.entityType = etType
        self.entityType = self.entityType.strip().upper()
        self.entityDist = etDist
        self.PlayerRef = pr
        self.entityDPS = 1
        self.entityTTK = self.PlayerRef.health / self.entityDPS
        self.fuelAmount = 1000 # for fuel - available runtime in seconds
        self.ammoAmount = 90 # for weapons
        #self.entityETA = None
        self.entityUCT = 0
        self.entityHealth = etHealth

        # Entity type check - logic should be executed in separate classes instead.
        if self.entityDPS is not 0: # prevent divide by zero with fauna or hazardous flora
            self.entityDPS = etDPS
        else:
            self.entityDPS = 0.01

        if self.entityType == "FLORA" or self.entityType == "ITEM":
            self.entityHealth = etHealth
            self.entityUCT = etUCT
            self.PlayerRef.energyCost = 0.4 # player has to "wrangle" animal

        if  self.entityType == "FAUNA":
            self.entityHealth = etHealth
            self.entityUCT = self.entityTTK

        if self.entityType == "ITEM":
            self.entityDPS = etDPS

        print("Stats for " + str(self.entityType) + " " + str(self.uniqueRef) + ": ")
        print("Distance from player (metres): " + str(self.entityDist))

        if self.entityType == "FAUNA":
            print("Entity TTK: " + str(self.entityTTK))
        elif self.entityType == "FLORA" or self.entityType == "ITEM":
            print("Entity DPS: " + str(self.entityDPS))
        print("\n")
        