import PlayerChar, Entity, random

player1 = PlayerChar.Playerchar()

randDmg = [round(random.uniform(-0.5, 1), 2), round(random.uniform(-0.5, 1), 2), round(random.uniform(-0.5, 1), 2)]
randDist = [round(random.uniform(1, 250), 2), round(random.uniform(1, 250), 2), round(random.uniform(1, 250), 2)]
randHealth = [round(random.uniform(0, 1), 2), round(random.uniform(0, 1), 2), round(random.uniform(0, 1), 2)]
randUCT = [round(random.uniform(0, 10), 2), round(random.uniform(0, 10), 2), round(random.uniform(0, 10), 2)]

et1 = Entity.EntityInstance("FLORA", randDmg[0], randDist[0], player1, randHealth[0], randUCT[0])
et2 = Entity.EntityInstance("FAUNA", randDmg[1], randDist[1], player1, randHealth[1], randUCT[1])
et3 = Entity.EntityInstance("ITEM", randDmg[2], randDist[2], player1, randHealth[2], randUCT[2])
entities = [et1, et2, et3]
player1.ScanEnv(entities)