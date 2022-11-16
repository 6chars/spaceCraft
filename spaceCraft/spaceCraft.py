import pygame
import random
from playsound import playsound
pygame.init()
global shipDcelltime
global shipDcellspeed
global rotate
global x
global y
global shiphealth
global shipfuel
global fueldrain
global hitdelay
global section
k = 0
i = 0
x = 500
y = 500
#  use camelcase reasonably
rotate = 0.0
screen = pygame.display.set_mode((1800,1000))
shipLoad = pygame.image.load('placeholder.png')
ship = pygame.transform.rotate(shipLoad, rotate)
enemy = pygame.image.load('Enemy.png')
plasma = pygame.image.load('plasma.png')
bolt = pygame.image.load('bolt.png')
smallexplosion = pygame.image.load('Small_explosion.png')
text = pygame.font.SysFont("Consolas", 20)
shipPos = [500,500]
squaresX = []
squaresY = []
starStatus = []
terrains = []
fired = []
delay10 = 10
seekerdelay = []
enemyX = []
enemyY = []
for i in range(20):
    enemyX.append(1000+i)
    enemyY.append(500)
    i+= 200
randMovX = []
randMovY = []
cruiseRepeat = 0
shipbinaries = [0,0,1] # Throttling, engineOn, starmap
engineheat = 0
shipDcelltime = 0
shipDcellspeed = -1
shiphealth = 3
shipfuel = 10000
fueldrain = 3
hitdelay = 10
for i in range(enemyX.__len__()):
    randMovX.append(0)
    randMovY.append(0)
    seekerdelay.append(random.randrange(0,50))
shipHealth = 1
shipWeapon = False
for i in range(400):
    squaresX.append(random.randrange(-50000,50000))
    squaresY.append(random.randrange(-50000,50000))
    starStatus.append('white')
    terrains.append([[],[],[],[],[]])

while True:
    for i in [pygame.time.delay(10)]:
        screen.fill('black')
        if shipbinaries[1] == 1:
            if shipbinaries[0] == 1 and engineheat == 1:
                playsound('shipacc.wav', False)
            elif shipbinaries[0] == 1 and engineheat > 80 and cruiseRepeat == 0:
                playsound('shipcruise.wav', False)
                cruiseRepeat += 1
                shipbinaries[0] = 0
            engineheat += 1
            if cruiseRepeat == 50:
                cruiseRepeat = 0
            if cruiseRepeat != 0:
                cruiseRepeat += 1
        if shipbinaries[1] == 1 and shipbinaries[0] == 0:
            x += point[0] + shipDcellspeed
            y += point[1] + shipDcellspeed
            shipDcelltime += 1
            match shipDcelltime:
                case 1:
                    playsound('shipDcell.wav', False)
                case 40:
                    shipDcellspeed -= 1
                case 80:
                    shipDcellspeed -= 1
                case 100:
                    shipDcellspeed -= 1
                case 120:
                    shipDcellspeed = -1
                    shipDcelltime = 0
                    shipbinaries[1] = 0
                    engineheat = 0
        healthDisplay = screen.blit(text.render('Ship Health: '+ str(shiphealth),True,'White'),(800,900))
        fuelDisplay = screen.blit(text.render('Fuel: '+ str(shipfuel),True,'White'),(800,950))#         <---------------- ^Ship state measurement and handling^ ----------------
        if rotate >= 360:
            rotate = 0
        elif rotate <= 0:
            rotate = 360
        pygame.event.get()
        key = pygame.key.get_pressed()
        if key[pygame.K_d]:
            rotate -= 4
        if key[pygame.K_a]:
            rotate += 4
        if key[pygame.K_w]:
            shipbinaries[0] = 1
            shipbinaries[1] = 1
            point = [x,y]
            if rotate >= 270:
                y -= (rotate - 270) / 10
                x += abs(rotate - 360) / 10
            elif rotate >= 180:
                y += abs(rotate - 270) / 10
                x += (rotate - 180) / 10
            elif rotate >= 90:
                y += (rotate - 90) / 10
                x -= abs(rotate - 180) / 10
            elif rotate >= 0:
                y -= abs(rotate - 90) / 10
                x -= rotate / 10
            point[0] = x-point[0]
            point[1] = y-point[1]
            shipfuel -= fueldrain
        else:
            shipbinaries[0] = 0
        if key[pygame.K_m]:
            if delay10 == 10:
                if shipbinaries[2]:
                    shipbinaries[2] = False
                else:
                    shipbinaries[2] = True
                delay10 = 0
            else:
                delay10 += 1
        if key[pygame.K_KP7]:
            if delay10 == 0:
                fired.append([x,y,point[0],point[1],'plasma'])
                delay10 = 10
            else:
                delay10 -= 1#                                  <------^Ship input^------
        ship = pygame.transform.rotate(shipLoad, rotate)
        shipPos = ship.get_rect(center = (900,500))
        screen.blit(ship,(shipPos))
        if fired.__len__() > 30:
            fired.pop(0)
        for i in range(fired.__len__()):
            match fired[i][4]:
                case 'plasma':
                    shipWepPos = plasma.get_rect(center = (fired[i][0]-x+900,fired[i][1]-y+500))
                    screen.blit(plasma,(shipWepPos))
                    shipWeapon = True
                case 'bolt':
                    boltPos = bolt.get_rect(center = (fired[i][0]-x,fired[i][1]-y))
                    screen.blit(bolt,(boltPos))
                    damage = 1
                    shipWeapon = False
            if shipWeapon:
                for k in range(enemyX.__len__()):
                    if abs(shipWepPos.center[0]) > abs(enemyX[k]-x-20) and abs(shipWepPos.center[0]) < abs(enemyX[k]-x+20) and abs(shipWepPos.center[1]) > abs(enemyY[k]-y-20) and abs(shipWepPos.center[1]) < abs(enemyY[k]-y+20):        
                        enemyX.pop(k)
                        enemyY.pop(k)
                        fired[i][4] = 'hit'
                        break
                    k+=1
            else:
                if abs(fired[i][0]-x) > 885 and abs(fired[i][0]-x) < 910 and abs(fired[i][1]-y) > 480 and abs(fired[i][1]-y) < 515:
                    screen.fill('Green',(fired[i][0]-x,fired[i][1]-y,10,10))
                    playsound('damage.wav', False)
                    shiphealth -= damage
                    fired[i][1] += 9000
            fired[i][0] += fired[i][2]*2
            fired[i][1] += fired[i][3]*2
            i+=1#                                                   <------^projectiles^------
        for i in range(enemyX.__len__()):
            if enemyX[i]-x < 1800 and enemyY[i]-y < 1000 and enemyX[i]-x > 0 and enemyY[i]-y > 0:
                if enemyX[i]-x > 900:
                    enemyX[i] -= 2
                    boltXadd = -1            
                elif enemyX[i]-x < 900:
                    enemyX[i] += 2
                    boltXadd = 1
                if enemyY[i]-y > 500:
                    enemyY[i] -= 2
                    boltYadd = -1
                elif enemyY[i]-y < 500:
                    enemyY[i] += 2
                    boltYadd = 1
                if seekerdelay[i] == 50:
                    boltXadd *= random.randrange(0,10)
                    boltYadd *= (10 - abs(boltXadd))
                    fired.append([enemyX[i],enemyY[i],boltXadd,boltYadd,'bolt'])
                    randMovX[i] = random.randrange(-3,3)
                    randMovY[i] = random.randrange(-3,3)
                    seekerdelay[i] = 0
                seekerdelay[i] += 1
                enemyX[i] += randMovX[i]
                enemyY[i] += randMovY[i]
                screen.blit(enemy,(enemyX[i]-x,enemyY[i]-y))
            i+=1#                                                      <------^Enemy^------
        for i in range(squaresX.__len__()):
            if shipbinaries[2]: 
                if (squaresX[i]/10)-x/10 < 1800 and (squaresY[i]/10)-y/10 < 1000:
                    screen.fill(starStatus[i],(((squaresX[i]/10)-x/10)+800,((squaresY[i]/10)-y/10)+500,2,2))                
            if squaresX[i]-x < 1800 and squaresY[i]-y < 1000 and squaresX[i]-x > 0 and squaresY[i]-y > 0:
                if abs(squaresX[i]-x) < 25 and abs(squaresY[i]-y) < 25:
                    global xp
                    xp = 0
                    section += 20
                    while True:
                        for i in [pygame.time.delay(1)]:
                            screen.fill('black')
                            pygame.event.get()
                            key = pygame.key.get_pressed()
                            if key[pygame.K_a]:
                                xp -= 1
                            if key[pygame.K_d]:
                                xp += 1
                            for p in range(200):
                                if terrains[i][4][p] == True:
                                    screen.fill('grey',(i*50-xp,950,50,50))   
                                if terrains[i][3][p] == True:
                                    screen.fill('grey',(i*50-xp,900,50,50))          
                                if terrains[i][2][p] == True:
                                    screen.fill('grey',(i*50-xp,850,50,50))    
                                if terrains[i][1][p] == True:
                                    screen.fill('grey',(i*50-xp,800,50,50))  
                                if terrains[i][0][p] == True:
                                    screen.fill('grey',(i*50-xp,750,50,50)) 
                else:
                    screen.fill('blue',(squaresX[i]-x,squaresY[i]-y,20,20))
                    if starStatus == 'white':
                        section = 0
                        for i in range(200):
                            terrains[i][0].append(False) #a
                            terrains[i][1].append(False) #b
                            terrains[i][2].append(False) #c
                            terrains[i][3].append(False) #d
                            terrains[i][4].append(True) #e
                        for i in range(10):
                            dPush = random.randrange(0,6)
                            dWide = random.randrange(0,16)
                            for i in range(dWide):
                                terrains[i][3][dPush+i+section] = True
                                if random.randrange(0,6) > 2:
                                    terrains[i][2][dPush+i+section] = True
                                    if random.randrange(0,6) > 2:
                                        terrains[i][1][dPush+i+section] = True
                                        if random.randrange(0,6) > 2:
                                            terrains[i][0][dPush+i+section] = True
                        starStatus[i] = 'green'
            i+=1#                                                       <------^astral rendering^------
        pygame.display.update()
#features: Hitpoints, first unlock, capacities,  destructible or physical objects, upgradeable unlocks, better sprites, particles, sounds, trading posts & credits
#bugs: point not defined on start and turn, 30 projectiles simulated indefinately, static projectile image
#unlocks: terrain scanner, energy capacity, map unlock, rechargeable shield, timed explosive, plasma beam, warp drive, limited missiles,
