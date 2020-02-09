import PlayerChar, Entity, random, os
os.system("cls")
player1 = PlayerChar.Playerchar(round(random.uniform(0.1, 1), 2), round(random.uniform(0.1, 1), 2))

# find a way to prevent generation of zero before assigning values to variables
randDmg = [round(random.uniform(-0.5, 1), 2), round(random.uniform(-0.5, 1), 2), round(random.uniform(-0.5, 1), 2), 0.01]
randDist = [round(random.uniform(1, 250), 2), round(random.uniform(1, 250), 2), round(random.uniform(1, 250), 2), 0]
randHealth = [round(random.uniform(0, 1), 2), round(random.uniform(0, 1), 2), round(random.uniform(0, 1), 2), 0]
randUCT = [round(random.uniform(0, 10), 2), round(random.uniform(0, 10), 2), round(random.uniform(0, 10), 2), 0]

et1 = Entity.EntityInstance("FLORA", randDmg[0], randDist[0], player1, randHealth[0], randUCT[0])
et2 = Entity.EntityInstance("FAUNA", randDmg[1], randDist[1], player1, randHealth[1], randUCT[1])
et3 = Entity.EntityInstance("ITEM", randDmg[2], randDist[2], player1, randHealth[2], randUCT[2])
et4 = Entity.EntityInstance("PROCGENENV", randDmg[3], randDist[3], player1, randHealth[3], randUCT[3])
entities = [et1, et2, et3, et4]
player1.ScanEnv(entities)