import random
class Playerchar:
    
    def __init__(self, ch, ce):
        # Constant values, in seconds       # Notes
        self.MAXTIMESTARVE = 1600
        self.TIMEHEALTHRECOVER = 250        # if at least 75 and timeStarve > 0
        self.STARVATIONDPS = 0.01
        self.MAXTIMETODIE = 500
        self.MAXENERGY = 1.0                # maximum energy

        # current stats
        self.currentHealth = ch             # player's current health, will change.
        self.health = self.currentHealth         # player's current health, used for prediction
        self.otherEntity = None             # other entity can be unequipped item, flora, fauna. If item equipped, let this affect player accordingly
        self.timeStarve = 1600              # starvation value
        self.damagePerSecond = 0.25         # damage player can deal - can change with picked up weapon
        self.timeDie = self.MAXTIMETODIE
        self.timeToKillTarget = None        # need to consider variety in Entity class
        self.calculatedReward = None
        self.movementSpeed = 3              # used for calculating distance, ETA and related reward values
        self.negativeReward = 0
        self.nextState = None
        self.currentAction = None           # for instance, if asleep, attacking, gathering, etc. Maybe use ScanEnv()?
        self.nextAction = None
        self.futureActions = []
        self.futureStates = []
        self.policyItem = None              # entities?
        self.policyItems = []               # make list
        self.currentEnergy = ce             # current energy - will regenerate after a few seconds.
        self.energy = self.currentEnergy    # use for prediction.
        self.energyCost = 0                 # energy cost to complete an action. For instance, killing an animal costs more energy than foraging.
        self.currentState = {"Health": self.health, "Energy": self.energy}
        self.chosenAction = None
        #self.minDistToEntity = 0

    def CalcReward(self, et, minDist):
        self.timeToKillTarget = et.entityHealth / self.damagePerSecond

        print("Player time to kill target: " + str(self.timeToKillTarget))
        print("Entity time to kill player: " + str(et.entityTTK))

        # calculate DPS and reward
        # deduct health by how much entity damage player times how long entity stayed alive.
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
            self.negativeReward += 0
            pass
        self.health -= et.entityDPS * self.timeToKillTarget # only do this if RLBrain chooses to go forward with this action.

        # clamp health values
        if self.health <= 0:
            self.health = 0
        elif self.health >= 1:
            self.health = 1
        else:
            self.health -= et.entityDPS * self.timeToKillTarget # only do this if RLBrain chooses to go forward with this action.

        # calculate energy cost
        if et.entityType == "FAUNA":
            self.energyCost = et.entityTTK*0.2 # player has to "wrangle" animal
        else:
            self.energyCost = et.entityUCT*0.05 # entityTTK = entityUCT
        if self.energyCost > 1:
            self.energyCost = 1
        elif self.energyCost < 0:
            self.energyCost = self.energyCost * -1

        self.energy -= self.energyCost
        print("Energy cost: " + str(self.energyCost))

        # calculate reward based on player's remaining time to die
        # check entity type here
        # reward with time to die minus time to arrive to location plus time to kill enemy/complete action plus negative reward plus 100 times energy cost
        if et.entityDist <= minDist:
            print("Using " + str(et.entityType) + " as active state...")
            self.etaReward = 0
            #print("Reward: " + str(self.etaReward))
            self.currentAction = et
        else:
            self.etaReward = (self.timeDie) - ((et.entityDist / self.movementSpeed) + et.entityUCT + self.negativeReward + (self.energyCost * 100))
            #print("Reward: " + str(self.etaReward))
            self.nextState = {"Health": self.health, "Energy": self.energy}
            self.nextAction = et
            self.futureStates.append(self.nextState)
            self.futureActions.append(self.nextAction)
            print("Next state: " + str(self.nextState))

        # reset values for prediction
        self.health = self.currentHealth
        self.energy = self.currentEnergy
        rewardVal = self.etaReward
        return rewardVal
    
    def ScanEnv(self, ets):
        print("------------SCANNING ENVIRONMENT------------")
        smallestDistance = 25000
        for i in range (0, len(ets)):
            if i > 0 and ets[i].entityDist < smallestDistance: # try to set current state for player's current location
                smallestDistance = ets[i].entityDist
                #self.currentAction = ets[i]
                #ets[i].isCurrentAction = True
            print("Shortest distance: " + str(smallestDistance))
            # do not excute anything else at this point - more than one entity will be assigned the current state otherwise!

        # run loop again, as smallest distance has been finalized.
        for i in range (0, len(ets)):
            print(str(ets[i].entityType) + " " + str(ets[i].uniqueRef) + ":\tDistance: " + str(ets[i].entityDist) + "\tDamage: " + str(ets[i].entityDPS) + "\tUCT: " + str(ets[i].entityUCT) + "\tHealth: " + str(ets[i].entityHealth) + "\tReward: " + str(ets[i].rewardValue))
            #self.CalculateReward(ets[i], smallestDistance)
            ets[i].rewardValue = self.CalcReward(ets[i], smallestDistance)
            print("Reward: " + str(ets[i].rewardValue))
            if ets[i].rewardValue > 0:
                ets[i].isTerminal = True
            else:
                ets[i].isTerminal = False
            print("\n")
        #self.minDistToEntity = smallestDistance
        return None                         # return array of entites as Actions