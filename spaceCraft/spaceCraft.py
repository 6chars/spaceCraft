import pygame
import random
from playsound import playsound
pygame.init()
global shipDcelltime
global shipDcellspeed
global rotate
global x
global y
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
shipPos = [500,500]
squaresX = []
squaresY = []
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
for i in range(enemyX.__len__()):
    randMovX.append(0)
    randMovY.append(0)
    seekerdelay.append(random.randrange(0,50))
shipHealth = 1
shipWeapon = False
for i in range(400):
    squaresX.append(random.randrange(-50000,50000))
    squaresY.append(random.randrange(-50000,50000))
while True:
    for i in [pygame.time.delay(10)]:
        screen.fill('black')
        if shipbinaries[1] == 1:
            if shipbinaries[0] == 1 and engineheat == 0:
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
            print(shipDcelltime)
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
                    engineheat = 0#         <---------------- ^Ship state measurement and handling^ ----------------
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
            if shipWeapon:
                for k in range(enemyX.__len__()):
                    if abs(shipWepPos.center[0]) > abs(enemyX[k]-x-20) and abs(shipWepPos.center[0]) < abs(enemyX[k]-x+20) and abs(shipWepPos.center[1]) > abs(enemyY[k]-y-20) and abs(shipWepPos.center[1]) < abs(enemyY[k]-y+20):        
                        print(abs(shipWepPos.center[0]), abs(enemyX[k]-100))
                        enemyX.pop(k)
                        enemyY.pop(k)
                        break
                    k+=1
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
                    boltYadd *= 10-boltXadd
                    fired.append([enemyX[i],enemyY[i],boltXadd,boltYadd,'bolt'])
                    randMovX[i] = random.randrange(-3,3)
                    randMovY[i] = random.randrange(-3,3)
                    seekerdelay[i] = 0
                seekerdelay[i] += 1
                enemyX[i] += randMovX[i]
                enemyY[i] += randMovY[i]
                screen.blit(enemy,(enemyX[i]-x,enemyY[i]-y))
            i+=1
        for i in range(squaresX.__len__()):
            if shipbinaries[2]: 
                if (squaresX[i]/10)-x/10 < 1800 and (squaresY[i]/10)-y/10 < 1000:
                    screen.fill('white',(((squaresX[i]/10)-x/10)+800,((squaresY[i]/10)-y/10)+500,2,2))                
            if squaresX[i]-x < 1800 and squaresY[i]-y < 1000 and squaresX[i]-x > 0 and squaresY[i]-y > 0:              
                screen.fill('blue',(squaresX[i]-x,squaresY[i]-y,20,20))
            i+=1
        pygame.display.update()
#features: Hitpoints, first unlock, capacities,  destructible or physical objects, upgradeable unlocks, better sprites, particles, sounds, trading posts & credits
#bugs: point not defined on start and turn, 30 projectiles simulated indefinately, static projectile image
#unlocks: energy capacity, map unlock, rechargeable shield, timed explosive, plasma beam, warp drive, limited missiles,