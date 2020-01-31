class Playerchar:
    
    def __init__(self):
        # Constant values, in seconds       # Notes
        self.MAXTIMESTARVE = 1600
        self.TIMEHEALTHRECOVER = 250        # if at least 75 and timeStarve > 0
        self.STARVATIONDPS = 0.01
        self.MAXTIMETODIE = 500
        self.MAXENERGY = 1.0                # maximum energy

        # current stats
        self.health = 1.0                   # player's current health
        self.otherEntity = None             # other entity can be unequipped item, flora, fauna. If item equipped, let this affect player accordingly
        self.timeStarve = 1600              # starvation value
        self.damagePerSecond = 0.25         # damage player can deal - can change with picked up weapon
        self.timeDie = self.MAXTIMETODIE
        self.timeToKillTarget = None        # need to consider variety in Entity class
        self.useCompletionTime = None
        #self.scannedEntities[] = None
        self.calculatedReward = None
        self.movementSpeed = 3              # used for calculating distance, ETA and related reward values
        self.negativeReward = 0
        self.wakefulness = 500
        self.nextState = None
        self.currentAction = None           # for instance, if asleep, attacking, gathering, etc. Maybe use ScanEnv()?
        #self.predictedState                # same as in currentState, but values are calculation from nextAction
        self.nextAction = None
        #self.nextAction
        #self.actionItems = {}
        self.futureStates = []
        self.policyItem = None              # entities?
        self.policyItems = []               # make list
        self.currentEnergy = self.MAXENERGY # current energy - will regenerate after a few seconds.
        self.energyCost = 0                 # energy cost to complete an action. For instance, killing an animal costs more energy than foraging.
        self.currentState = {"Health": self.health, "Wakefulness": self.wakefulness, "Energy": self.currentEnergy}

    def CalculateStateValues(self):
        return None

    def CalculateReward(self, et):
        #self.proximityReward = 1 / (0.01 * et.entityDist)
        # calculate reward by add time to arrive and time to complete action
        self.timeToKillTarget = et.entityHealth / self.damagePerSecond
        
        print("Player time to kill target: " + str(self.timeToKillTarget))
        print("Entity time to kill player: " + str(et.entityTTK))

        if et.entityDPS < 0:
            et.entityTTK = et.entityTTK*-1 # prevent negative reward

        elif et.entityTTK <= self.timeToKillTarget and et.entityTTK > -0.01:
            print("Do not engage " + et.entityType + " " + str(et.uniqueRef) + ". It is highly dangerous!")
            self.negativeReward = self.MAXTIMESTARVE + self.MAXTIMETODIE + (self.STARVATIONDPS * 50)
            print(self.negativeReward)
            
        elif et.entityTTK < -0.01:
            #self.negativeReward -= et.entityTTK*100 # boost reward if entity can heal
            print("This will heal the player.")

        else:
            # deduct health by how much entity damage player times how long entity stayed alive.
            self.health -= et.entityDPS * self.timeToKillTarget # only do this if RLBrain chooses to go forward with this action.
            self.negativeReward += 0

        # calculate energy cost
        if et.entityType == "FAUNA":
            self.energyCost = et.entityTTK*0.2 # player has to "wrangle" animal
        else:
            self.energyCost = et.entityUCT*0.05 # entityTTK = entityUCT
        if self.energyCost > 1:
            self.energyCost = 1
        elif self.energyCost < 0:
            self.energyCost = self.energyCost * -1

        self.currentEnergy -= self.energyCost
        print("Energy cost: " + str(self.energyCost))

        # if item is deadly and/or will cause damage to player, also consider for deduction. Calculate with number of hits
        # if action is interrupted, only take damage.
        # if entity DPS is low, still take damage.
        # if item will boost player's base damage stat, add to ETA reward

        # calculate reward based on player's remaining time to die
        # check entity type here
        # if player is at procGenEnv and is feeling sleepy, and not nearby dangerous fauna, then sleep.
        # reward with time to die minus time to arrive to location plus time to kill enemy/complete action plus negative reward plus 100 times energy cost

        self.etaReward = (self.timeDie) - ((et.entityDist / self.movementSpeed) + et.entityUCT + self.negativeReward + (self.energyCost * 100))
        print("Reward: " + str(self.etaReward))
        self.nextState = {"Health": self.health, "Wakefulness": self.wakefulness, "Energy": self.currentEnergy}
        print(self.nextState)
        self.futureStates.append(self.nextState)
        
        # reset values for prediction
        self.health = 1.0
        self.currentEnergy = self.MAXENERGY
    def ScanEnv(self, ets):
        print("------------SCANNING ENVIRONMENT------------")
        smallestDistance = 25000
        for i in range (0, len(ets)):
            if i > 0 and ets[i].entityDist < smallestDistance: # try to set current state for player's current location
                smallestDistance = ets[i].entityDist
                self.currentAction = ets[i]
                #ets[i].isCurrentAction = True
            print(str(ets[i].entityType) + " " + str(ets[i].uniqueRef) + ":\tDistance: " + str(ets[i].entityDist) + "\tDamage: " + str(ets[i].entityDPS) + "\tUCT: " + str(ets[i].entityUCT) + "\tHealth: " + str(ets[i].entityHealth))
            print("Shortest distance: " + str(smallestDistance))
            self.CalculateReward(ets[i])
            print("")
        return None                         # return array of entites as Actions

    def RLBrain(self, cs):
        # code based on that of MorvanZhou's on Github: https://github.com/MorvanZhou/Reinforcement-learning-with-tensorflow
        print("Current state: " + str(cs))
        print("Current action: " + str(self.currentAction.entityType) + "\n")
        for i in range (0, len(self.futureStates)):
            print("Candidate state: " + str(self.futureStates[i]) + "\n")
        return None