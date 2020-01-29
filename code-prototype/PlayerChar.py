class Playerchar:
    
    def __init__(self):
        # Constant values, in seconds       # Notes
        self.MAXTIMESTARVE = 1600
        self.TIMEHEALTHRECOVER = 250        # if at least 75 and timeStarve > 0
        self.STARVATIONDPS = 0.01
        self.MAXTIMETODIE = 500

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
        self.currentState = {"Health": self.health, "OtherEntity": self.otherEntity, "Wakefulness": self.wakefulness, "DPS": self.damagePerSecond}
        self.currentAction = None           # for instance, if asleep, attacking, gathering, etc. Maybe use ScanEnv()?
        #self.predictedState                # same as in currentState, but values are calculation from nextAction
        #self.nextAction
        #self.actionItems = {}

    def CalculateStateValues(self):
        return None

    def CalculateReward(self, et):
        #self.proximityReward = 1 / (0.01 * et.entityDist)
        # calculate reward by add time to arrive and time to complete action
        self.timeToKillTarget = et.entityHealth / self.damagePerSecond
        print("Player time to kill target: " + str(self.timeToKillTarget))
        print("Entity time to kill player: " + str(et.entityTTK))
        if et.entityTTK <= self.timeToKillTarget and et.entityTTK > -0.01:
            print("Do not engage " + et.entityType + " " + str(et.uniqueRef) + ". It is highly dangerous!")
            self.negativeReward = self.MAXTIMESTARVE + self.MAXTIMETODIE + (self.STARVATIONDPS * 50)
            print(self.negativeReward)
        elif et.entityTTK < -0.01:
            print("This will heal the player.")
        else:
            # deduct health by how much entity damage player times how long entity stayed alive.
            self.health -= et.entityDPS * self.timeToKillTarget # only do this if RLBrain chooses to go forward with this action.
            self.negativeReward = 0
        
        # if item is deadly and/or will cause damage to player, also consider for deduction. Calculate with number of hits
        # if action is interrupted, only take damage.
        # if entity DPS is low, still take damage.
        # if item will boost player's base damage stat, add to ETA reward

        # if item needs fuel (and hence refueling if necessary), deduct from ETA reward in a similar way to et.entityTTK <= - search for this first before using tool?
        # Deduct reward significantly if tool not have fuel - require time to refuel.
        # Undo reward deduction if player has fuel equipped or fuel is in inventory
        # Mark state as terminal if fuel prerequisites met
        
        # Prefer player to harvest water with an item that can hold liquids - similar logic above? Consult its inventory
        # if item is holding water (i.e. liquidType is potableWater and liquidVolume > 0), allow player to drink from it
        # Mark state as terminal if water made potable

        # calculate reward based on player's remaining time to die
        # check entity type here
        # if player is at procGenEnv and is feeling sleepy, and not nearby dangerous fauna, then sleep.
        
        self.etaReward = (self.timeDie) - ((et.entityDist / self.movementSpeed) + et.entityUCT + self.negativeReward)
        print("Reward: " + str(self.etaReward))

    def ScanEnv(self, ets):
        for i in range (0, len(ets)):
            print(str(ets[i].entityType) + " " + str(ets[i].uniqueRef) + ":\tDistance: " + str(ets[i].entityDist) + "\tDamage: " + str(ets[i].entityDPS) + "\tUCT: " + str(ets[i].entityUCT) + "\tHealth: " + str(ets[i].entityHealth))
            self.CalculateReward(ets[i])
            print("")
        print("Scanning environment")
        return None                         # return array of entites as Actions