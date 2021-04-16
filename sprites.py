import pygame as py
from os import path
from settings import *
from tilemap import *
import random,time
vec=py.math.Vector2

class Player(py.sprite.Sprite):
    def __init__(self,game,x,y):
        py.sprite.Sprite.__init__(self)
        self.game = game
        self.vel = vec(0,0)
        self.picture=0
        self.ttC=0
        self.type = 'Player'
        self.gunDrawn = False
        #image needs to change once image is made
        self.load_images()
        self.direction = 1
        self.image = self.walkingl[0]
        self.rect=self.image.get_rect()
        self.rect.inflate_ip(-36,-20)
        self.standingRect = self.rect
        self.wallJump = False
        self.rect.topleft = (x,y)
        self.knockback = False
        self.knockbackDone = 30
        self.knockbackTimer = 0
        self.hitting = False
        self.speed = SPEED
        self.animate()#run throught animation frames, to get starting image
        self.gActivated = True
        self.climb = False
        self.speed = SPEED
        self.gunHeight = 16
        self.wallJumpTimer = 0
        self.acc = vec(0,0)
        self.wallJumpDirec = 0
        self.onGround = True
        self.hittingDirection = 0
        self.screenMovement = False
        self.canMove = True
        
    def collide(self, xDif, yDif, platform_list,door = 0):
        #players collision
        for i in platform_list:
            if door == 0:
                if py.sprite.collide_rect(self, i):
                    if xDif > 0:                       
                        self.rect.right = i.rect.left
                        self.wallJumpDirec = 0
                        self.vel.x = 0
                    elif xDif < 0:
                        self.rect.left = i.rect.right
                        self.wallJumpDirec = 0
                        self.vel.x = 0
                    if yDif > 0:
                        self.rect.bottom = i.rect.top
                        self.vel.y = 0
                        self.wallJumpDirec = 0
                        self.onGround = True
                        self.wallJump = False
                        self.game.doubleJumpAble = True
                    if yDif < 0:
                        self.rect.top = i.rect.bottom
                        self.vel.y = 0
                        self.wallJumpDirec = 0
            else:
                if py.sprite.collide_rect(self, i) and not i.opened and i.direction[0:4] !='back':
                    if xDif > 0:
                        self.rect.right = i.rect.left
                        self.wallJumpDirec = 0
                        self.vel.x = 0
                    elif xDif < 0:
                        self.rect.left = i.rect.right
                        self.wallJumpDirec = 0
                        self.vel.x = 0
                    if yDif > 0:
                        self.rect.bottom = i.rect.top
                        self.vel.y = 0
                        self.wallJumpDirec = 0
                        self.onGround = True
                        wallJump = False
                    if yDif < 0:
                        self.rect.top = i.rect.bottom
                        self.vel.y = 0
                        self.wallJumpDirec = 0
                        
    def update(self):
        if self.gActivated:
            self.vel.y += GRAVITY # Gravity
        for item in self.game.equipedItems:
            if item == self.game.steelPowerup:
                self.vel.y +=.2
        self.vel.y = min(self.vel.y, 20) # Terminal Velocity
        currentd = self.direction
        SPEED = self.speed*self.game.speedPercent
        if self.game.healthLeft <= self.game.hearts*1.4:
            for item in self.game.equipedItems:
                if item == self.game.speedPowerup:
                    if self.game.powerupLevel[1] == 0:
                        SPEED = SPEED*1.3
                    if self.game.powerupLevel[1] == 1:
                        SPEED = SPEED*1.5
                    if self.game.powerupLevel[1] == 2:
                        SPEED = SPEED*1.7
                    if self.game.powerupLevel[1] == 3 or self.game.powerupLevel[1] == 4:
                        SPEED = SPEED*2
                    
        if self.game.bulletLevel[5] == 10 and self.game.batteryCharging and self.game.batteryTimer>100:
            SPEED = SPEED*1.35
        #deal with how the player has to move in different ways depending factors
        if ((not self.knockback) and (not self.game.screenFade or self.game.fadeTimer >=36) and not self.wallJump and
            (not self.hitting or not self.onGround) and not self.screenMovement and self.canMove):
            keys = py.key.get_pressed()
            if keys[self.game.moveLeftKey] and keys[self.game.moveRightKey]:
                if self.wallJumpDirec == 0:
                    if self.vel.x>0:
                        self.vel.x-=1
                    if self.vel.x<0:
                        self.vel.x += 1
            elif keys[self.game.moveLeftKey]:
                if not self.hitting:
                    if self.vel.x > -SPEED:
                        self.vel.x += -1
                    if self.wallJumpDirec == 0 and self.vel.x < -SPEED:
                        self.vel.x +=1
                else:
                    if self.hittingDirection == -1:
                        if self.vel.x > -SPEED:
                            self.vel.x += -1
                        if self.wallJumpDirec == 0 and self.vel.x < -SPEED:
                            self.vel.x +=1
            elif keys[self.game.moveRightKey]:
                if not self.hitting:
                    if self.vel.x < SPEED:
                        self.vel.x += 1
                    if self.wallJumpDirec == 0 and self.vel.x > SPEED:
                        self.vel.x +=-1
                else:
                    if self.hittingDirection == 1:
                        if self.vel.x < SPEED:
                            self.vel.x += 1
                        if self.wallJumpDirec == 0 and self.vel.x > SPEED:
                            self.vel.x +=-1

            else:
                if self.wallJumpDirec == 0:
                    if self.vel.x>0:
                        self.vel.x-= 1
                    if self.vel.x<0:
                        self.vel.x += 1
            if abs(self.vel.x)<1:
                self.vel.x = 0
        #change players direction for animation
        if self.vel.x>0:
            self.direction = 1
        if self.vel.x<0:
            self.direction = -1
        if self.direction != currentd:
            self.ttC = 0

        if self.vel.y > GRAVITY+3 and self.onGround:
            self.onGround = False
            
        self.rect.left += self.vel.x  # X and Y positions are updated
        self.collide(self.vel.x, 0, self.game.floors)
        self.collide(self.vel.x,0,self.game.spikes)
        self.collide(self.vel.x, 0, self.game.doors,1)
        self.rect.top += self.vel.y
        self.collide(0, self.vel.y, self.game.floors)
        self.collide(0,self.vel.y,self.game.spikes)
        self.collide(0, self.vel.y, self.game.doors,1)
        SPEED = self.speed
        self.animate()

    def animate(self):
        oldimage = self.image
        pressedKey = py.key.get_pressed()
        if not self.hitting and not self.wallJump:
            if self.vel.x==0:
                if self.direction == 1:
                    if self.gunDrawn:
                        self.image = self.walkingrGun[0]
                    else:
                        self.image=self.standingr[0]
                if self.direction == -1: #standing idle
                    if self.gunDrawn:
                        self.image = self.walkinglGun[0]
                    else:
                        self.image=self.standingl[0]
                
            if self.vel.x>0:
                if self.ttC==0:#right walking animation
                    if self.gunDrawn:
                        self.image = self.walkingrGun[self.picture]
                    else:
                        self.image=self.walkingr[self.picture]
                    self.picture+=1
                    if self.picture>len(self.walkingr)-1:
                        self.picture=0
                self.ttC+=1
                if self.ttC>=6*(1/self.game.speedPercent):#6 frame delay
                    self.ttC=0
                    
            if self.vel.x<0:
                if self.ttC==0:#left walking animation
                    if self.gunDrawn:
                        self.image = self.walkinglGun[self.picture]
                    else:
                        self.image=self.walkingl[self.picture]
                    self.picture+=1
                    if self.picture>len(self.walkingl)-1:
                        self.picture=0
                self.ttC+=1#6 frame delay
                if self.ttC>=6*(1/self.game.speedPercent):
                    self.ttC=0
            
        if self.wallJump:
            if self.direction == 1:
                self.image = self.onWallR[1]
            else: self.image = self.onWallL[1]
            
        if self.hitting:#pistol whip animation
            self.ttC+=1
            if self.picture>=len(self.pistolWhipL):
                    self.picture = len(self.pistolWhipL)-1
            if self.direction == 1:
                self.image = self.pistolWhipR[self.picture]
            else: self.image = self.pistolWhipL[self.picture]
            if self.ttC >=3:
                self.ttC = 0
                self.picture+=1
        if not oldimage == self.image:
            self.image.set_colorkey((237,28,36))

        if self.game.batteryCharging and not self.game.skillActive:
            if self.vel.x==0:
                if self.direction == 1:
                        self.image = self.walkingrGun[0]
                if self.direction == -1:
                        self.image = self.walkinglGun[0]
            if self.vel.x>0:
                self.image = self.walkingrGun[self.picture]   
            if self.vel.x<0:
                self.image = self.walkinglGun[self.picture]
                    
            new_img = self.image.copy()  # Create copy of image
            if self.game.batteryTimer < 100:
                new_img.fill((self.game.batteryTimer,self.game.batteryTimer,0),special_flags = py.BLEND_RGB_ADD)
                if self.game.batteryTimer+237<= 255:
                    new_img.set_colorkey((237+self.game.batteryTimer,self.game.batteryTimer+28,36))
                elif self.game.batteryTimer+28<= 255:
                    new_img.set_colorkey((255,self.game.batteryTimer+28,36))
            else:
                new_img.fill((240,240,0),special_flags = py.BLEND_RGB_ADD)
                new_img.set_colorkey((255,255,36))
            self.image = new_img
            
        if self.game.skillActive:
            if not self.hitting and not self.wallJump:
                if self.vel.x==0:
                    if self.direction == 1:
                        if self.gunDrawn:
                            self.image = self.walkingrGun[0]
                        else:
                            self.image=self.standingr[0]
                    if self.direction == -1: #standing idle
                        if self.gunDrawn:
                            self.image = self.walkinglGun[0]
                        else:
                            self.image=self.standingl[0]
                if self.vel.x>0:
                    if self.gunDrawn:
                        self.image = self.walkingrGun[self.picture]
                    else:
                        self.image=self.walkingr[self.picture]
                if self.vel.x<0:
                    if self.gunDrawn:
                        self.image = self.walkinglGun[self.picture]
                    else:
                        self.image=self.walkingl[self.picture]
            if self.wallJump:
                if self.direction == 1:
                    self.image = self.onWallR[1]
                else: self.image = self.onWallL[1]
            if self.hitting:#pistol whip animation
                if self.picture>=len(self.pistolWhipL):
                        self.picture = len(self.pistolWhipL)-1
                if self.direction == 1:
                    self.image = self.pistolWhipR[self.picture]
                else: self.image = self.pistolWhipL[self.picture]

            new_img = self.image.copy()
            new_img.fill((0,255,150),special_flags = py.BLEND_RGB_ADD)
            new_img.set_colorkey((237,255,186))
            self.image = new_img
            
    def load_images(self):
        #loading all imagaes for the player sprite
        self.standingr=[]
        self.standingl=[]
        self.walkingr=[]
        self.walkingl=[]
        self.walkingrGun = []
        self.walkinglGun = []
        self.pistolWhipR = []
        self.pistolWhipL = []
        self.onWallR = [py.image.load(path.join(self.game.playerWallFold,'Walljump1.png')).convert(),
                        py.image.load(path.join(self.game.playerWallFold,'Walljump2.png')).convert()]
        self.onWallL = []
        for i in self.onWallR:
            self.onWallL.append(py.transform.flip(i,True,False))
        self.onWallR
        self.standingr.append(py.image.load(path.join(self.game.walkingr_fold, 'walkright1.png')).convert())
        self.standingl.append(py.image.load(path.join(self.game.walkingl_fold, 'walkleft1.png')).convert())
        for i in range(6):
            self.walkingr.append(py.image.load(path.join(self.game.walkingr_fold, 'walkright'+str(i+1)+'.png')).convert())
            self.walkingl.append(py.image.load(path.join(self.game.walkingl_fold, 'walkleft'+str(i+1)+'.png')).convert())
            self.walkingrGun.append(py.image.load(path.join(self.game.walkingrGunFold, 'GunRight'+str(i+1)+'.png')).convert())
            self.walkinglGun.append(py.image.load(path.join(self.game.walkinglGunFold, 'GunLeft'+str(i+1)+'.png')).convert())
        for i in range(5):
            self.pistolWhipR.append(py.image.load(path.join(self.game.gunWhipFold, 'P_Melee'+str(i+1)+'.png')).convert())
        for i in self.pistolWhipR:
            self.pistolWhipL.append(py.transform.flip(i,True,False))
            
        self.allPlayerImages = [self.standingr, self.standingl, self.walkingl,self.walkingr,
                                self.walkingrGun, self.walkinglGun, self.pistolWhipR, self.pistolWhipL,
                                self.onWallR,self.onWallL]

class Hitting(py.sprite.Sprite):#class for when the player/enemies are using melee attack
    def __init__(self,game,user):
        py.sprite.Sprite.__init__(self)
        self.game = game
        self.user = user
        self.timer =30
        if self.user.type == 'Player':#make sure it can only hit right person
            self.canHit = 1
            self.timer = 15
        else: self.canHit = 0
        self.image = py.Surface((32,48))
        self.rect = self.image.get_rect()
        if self.user.direction == 1:
            self.rect.midleft = self.user.rect.midright
        else: self.rect.midright = self.user.rect.midleft

    def update(self):
        self.timer -=1
        if self.user.direction == 1:#move with the user
            self.rect.midleft = self.user.rect.midright
        else: self.rect.midright = self.user.rect.midleft
        if self.timer == 0:#kill when timer runs out or if user takes kb
            self.user.hitting = False
            self.user.picture = 0
            self.kill()
        if self.user.knockback:
            self.user.hitting = False
            self.user.picture = 0
            self.kill()

                                    
class Enemy(py.sprite.Sprite):#enemy class
    def __init__(self,game,Etype,center,mode,keyReq,number,text):
        py.sprite.Sprite.__init__(self)
        self.game = game
        self.text = text
        self.type = Etype
        self.mode = mode
        self.keyReq = keyReq
        self.vel = vec(0,0)
        self.number = number
        self.activeMode = 'standard enemy, no active mode'
        #different stats for the enemies
        if Etype == 0:
            self.speed = 4
            self.health = 10
            self.gunner = False
        if Etype == 1:
            self.speed = 0
            self.health = 15
            self.gunner = True
        if Etype == 2:
            self.speed = 0
            self.health = 20
            self.gunner = True
        if Etype == 3:
            self.speed = 6
            self.health = 20
            self.gunner = False
        if Etype == 4:
            self.speed = 5
            self.health = 25
            self.gunner = False
        if Etype == 5:
            self.speed = 0
            self.health = 30
            self.gunner = True
        if Etype == 6:
            self.speed = 6
            self.health = 35
            self.gunner = False
            
        if Etype == 20:
            self.speed = 5
            self.health = 35
            self.gunner = False
        if Etype == 21:
            self.speed = 6
            self.health = 45
            self.gunner = False
        if Etype == 22:
            self.speed = 7
            self.health = 55
            self.gunner = False
        if Etype == 23:
            self.speed = 0
            self.health = 28
            self.gunner = True
        if Etype == 24:
            self.speed = 0
            self.health = 36
            self.gunner = True
        if Etype == 25:
            self.speed = 0
            self.health = 48
            self.gunner = True
            
        if Etype == 30:
            self.speed = 5
            self.health = 40
            self.gunner = False
        if Etype == 31:
            self.speed = 6
            self.health = 50
            self.gunner = False
        if Etype == 32:
            self.speed = 7
            self.health = 65
            self.gunner = False
        if Etype == 33:
            self.speed = 0
            self.health = 42
            self.gunner = True
        if Etype == 34:
            self.speed = 4
            self.health = 48
            self.gunner = True
        if Etype == 35:
            self.speed = 5
            self.health = 56
            self.gunner = True

        if Etype == 40:
            self.speed = 6
            self.health = 50
            self.gunner = False
        if Etype == 41:
            self.speed = 7
            self.health = 60
            self.gunner = False
        if Etype == 42:
            self.speed = 8
            self.health = 75
            self.gunner = False
        if Etype == 43:
            self.speed = 4
            self.health = 40
            self.gunner = True
        if Etype == 44:
            self.speed = 6
            self.health = 50
            self.gunner = True
        if Etype == 45:
            self.speed = 7
            self.health = 62
            self.gunner = True
        if Etype == 46:
            self.speed = 0
            self.health = 40
            self.gunner = True

        if Etype == 50:
            self.speed = 5
            self.health = 60
            self.gunner = False
        if Etype == 51:
            self.speed = 7
            self.health = 65
            self.gunner = False
        if Etype == 52:
            self.speed = 8
            self.health = 75
            self.gunner = False
        if Etype == 53:
            self.speed = 8
            self.health = 90
            self.gunner = True
        if Etype == 54:
            self.speed = 0
            self.health = 50
            self.gunner = True
        if Etype == 55:
            self.speed = 6
            self.health = 55
            self.gunner = True
        if Etype == 56:
            self.speed = 7
            self.health = 65
            self.gunner = True
        if Etype == 57:
            self.speed = 7
            self.health = 80
            self.gunner = True

        if Etype == 100:
            self.speed = 7
            self.health = 401
            self.modeTimer = 900
            self.allModes = ['hitting','shooting']
            self.activeMode = 'shooting'
            self.gunner = True
        if Etype == 101:
            self.speed = 8
            self.health = 1000
            self.modeTimer = 900
            self.allModes = ['hitting','shooting','summon']
            self.activeMode = 'shooting'
            self.gunner = True

        if self.game.mode == 'easy':
            if self.speed >=6:
                self.speed -=1
            if self.health >=30:
                self.health -=4
            if self.health >=50:
                self.health -=5
            
        self.maxHealth = self.health
        if Etype == 100: self.maxHealth = 402

        self.picture=0
        self.ttC=0
        self.alert = False
        self.newAlert = False
        self.newAlertTimer = 0
        #image needs to change once image is made
        self.direction = 1
        self.load_images()
        self.image = self.walkingl[0]
        self.rect=self.image.get_rect()
        self.rect.center = center
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.newCommand = 0
        self.boundTimer = 0
        self.boundDone = 60
        self.gunHeight = 38
        self.boundHit = False
        self.deadTimer = 0
        self.deadPicture = 0
        self.shotTimer = 0
        self.hitting = False
        self.hitSetup = -1
        self.damaged = False
        self.damagedTimer = 0
        self.fireDamage = False
        self.fireDamageTimer = 60
        self.knockback = False
        self.knockbackTimer = 0
        self.boundryTimer = 0
        self.flash = 10
        self.coldTimer = 0
        self.animate()#run throught animation frames, to get starting image
        self.wallDirection = 0
        self.quickHit = 0
        self.quickHitTimer = 0

    def collide(self, xDif, yDif, platform_list,door = 0):
        for i in platform_list:
            if door == 0:
                if py.sprite.collide_rect(self, i):
                    if xDif > 0:                         # And our x (horizontal) speed is greater than 0...
                        self.rect.right = i.rect.left
                        self.vel.x = -self.vel.x
                        self.direction = -self.direction
                    if xDif < 0:                          # So our right bounding box becomes equal to the left bounding box of all platforms and we don't collide    
                        self.rect.left = i.rect.right
                        self.vel.x = -self.vel.x
                        self.direction = -self.direction
                    if yDif > 0:
                        self.rect.bottom = i.rect.top
                        self.vel.y = 0
                    if yDif < 0:
                        self.rect.top = i.rect.bottom
                        self.vel.y = 0
            else:
                if py.sprite.collide_rect(self, i) and not i.opened and i.direction[0:4]!='back':
                    if xDif > 0:
                        self.rect.right = i.rect.left
                        self.vel.x = -self.vel.x
                        self.direction = -self.direction
                    if xDif < 0:
                        self.rect.left = i.rect.right
                        self.vel.x = -self.vel.x
                        self.direction = -self.direction
                    if yDif > 0:
                        self.rect.bottom = i.rect.top
                        self.vel.y = 0
                    if yDif < 0:
                        self.rect.top = i.rect.bottom
                        self.vel.y = 0
                    
    def update(self):
        if self.deadTimer == 0:
            self.vel.y += GRAVITY # Gravity
            self.vel.y = min(self.vel.y, 20) # Terminal Velocity


            self.quickHitTimer -=1
            if self.quickHitTimer <=0:
                self.quickHit = 0
            
            if self.mode == 'starting' or self.mode == 'standard':
                if ((self.game.player.rect.center[0]-self.rect.center[0])**2+(self.game.player.rect.center[1]-self.rect.center[1])**2)**(1/2)<6*64 and not self.alert and self.game.player.canMove:
                    if self.mode == 'starting':
                        if self.game.player.gunDrawn:
                            self.alert = True
                            self.newAlert = True
                            if not self.game.timerStart:
                                self.game.timeStart = time.time()
                                self.game.timerStart = True
                    else:
                        self.alert =True
                        self.newAlert = True
                        if not self.game.timerStart:
                            self.game.timeStart = time.time()
                            self.game.timerStart = True
                if (((self.game.player.rect.center[0]-self.rect.center[0])**2+(self.game.player.rect.center[1]-self.rect.center[1])**2)**(1/2)>10*64
                    and self.health == self.maxHealth):
                    self.alert = False
                    
                if not self.alert:
                    if self.newCommand == 0:
                        direction = random.randint(-1,1)
                        if direction !=0:
                            direction = random.randint(-1,1)
                        if direction !=0:
                            self.direction = direction
                        self.vel.x = direction*self.speed*(0.5)
                        self.newCommand = random.randint(60,80)
                #what happens when the enemys become alert
                if self.alert:
                    if self.rect.center[0]>self.game.player.rect.center[0]:
                        directionToPlayer = -1
                    else: directionToPlayer = 1
                    if self.type <100:
                        if self.newCommand == 0:
                            if self.gunner:
                                direction=random.randint(-1,1)
                                if direction!=directionToPlayer:
                                    direction = random.randint(-1,1)
                                if direction!=directionToPlayer:
                                    direction = random.randint(-1,1)
                                if direction != 0:
                                    self.direction = direction
                                self.collide(self.vel.x, 0, self.game.floors)
                                self.collide(self.vel.x,0,self.game.spikes)
                                self.collide(self.vel.x,0,self.game.doors,1)
                                atWall = False
                                for i in self.game.floors:
                                    if i.rect.left == self.rect.right or i.rect.right == self.rect.left and self.vel.x == 0:
                                        atWall = True
                                if abs(self.rect.center[0]-self.game.player.rect.center[0])<20 and self.type >=30:
                                    self.direction = directionToPlayer
                                    self.vel.x = self.direction*(self.speed)
                                elif abs(self.rect.center[0]-self.game.player.rect.center[0])<200 and self.type >=30 and not atWall:
                                    self.direction = -directionToPlayer
                                    self.vel.x = self.direction*(self.speed)
                                else:
                                    self.vel.x = 0
                                    self.direction = directionToPlayer

                            else:
                                if not self.hitting:
                                    direction = directionToPlayer
                                    self.vel.x = direction*(self.speed)
                                if self.type >=20 and not self.hitting:
                                    if abs(self.rect.center[0]-self.game.player.rect.center[0])<25:
                                        direction = -directionToPlayer
                                        self.vel.x = direction*(self.speed)
                            self.newCommand = random.randint(50,75)
                        if self.direction == directionToPlayer and self.gunner:
                            shoot = random.randint(1,50)
                            if shoot == 1 and self.shotTimer < 0:
                                self.shotTimer = 40
                                valen = False
                                for i in self.game.equipedItems:
                                    if i == self.game.valentinesPowerup:
                                        dudshot = random.randint(1,100)
                                        chance = 0
                                        if self.game.powerupLevel[4] == 0:
                                            chance = 1
                                        if self.game.powerupLevel[4] == 1:
                                            chance = 1
                                        if self.game.powerupLevel[4] == 2:
                                            chance = 2
                                        if self.game.powerupLevel[4] == 3:
                                            chance = 2
                                        if self.game.powerupLevel[4] == 4:
                                            chance = 3
                                        if self.game.powerupLevel[4] == 5:
                                            chance = 3
                                        if self.game.powerupLevel[4] == 6:
                                            chance = 4
                                        if self.game.powerupLevel[4] == 7:
                                            chance = 5
                                        if self.game.powerupLevel[4] == 8:
                                            chance = 6
                                        if self.game.powerupLevel[4] == 9 or self.game.powerupLevel[4] == 10:
                                            chance = 7
                                        
                                        if dudshot <=chance:
                                            valen = True
                                            shotDistance = random.randint(14,20)
                                            c = DroppedHeart(self.game,(self.rect.center),self.direction*shotDistance)
                                            self.game.all_sprites.add(c)
                                            self.game.DroppedHeartGroup.add(c)
                                        
                                if self.direction == 1 and not valen:
                                    newB = Bullet(self,1,self.game,0,'enemy')
                                    self.game.bullets.add(newB)
                                    self.game.all_sprites.add(newB)
                                if self.direction == -1 and not valen:
                                    newB = Bullet(self,-1,self.game,0,'enemy')
                                    self.game.bullets.add(newB)
                                    self.game.all_sprites.add(newB)
                        self.shotTimer -=1
                        #move towards player
                        if not self.gunner and not self.hitting:
                            if abs(self.rect.center[0]-self.game.player.rect.center[0])<75 and self.type <20:
                                self.hitting = True
                                self.hitSetup = 15
                                self.vel.x = 0
                                self.direction = directionToPlayer
                            elif (abs(self.rect.center[0]-self.game.player.rect.center[0])<75 and
                                  abs(self.rect.center[0]-self.game.player.rect.center[0])>20):
                                self.hitting = True
                                self.hitSetup = 5
                                self.vel.x = 0
                                self.direction = directionToPlayer
                        if self.hitSetup >=0:
                            self.hitSetup-=1
                            if self.hitSetup == 0:
                                self.ttC = 0
                                self.picture = 0
                                h = Hitting(self.game,self)
                                self.game.hittingGroup.add(h)
     
                    elif self.type == 100 or self.type == 101:#code for the boss control
                        if self.type == 100:
                            if self.health >250:
                                if self.modeTimer <=0:
                                    if self.type == 100:
                                        self.activeMode = self.allModes[random.randint(0,1)]
                                    else: self.activeMode = self.allModes[random.randint(0,2)]
                                    self.modeTimer = 600
                            elif self.health >175:
                                self.activeMode = 'hitting'
                            elif self.health > 50:
                                self.activeMode = 'hitting'
                        if self.type == 101:
                            if self.modeTimer <=0:
                                self.activeMode = self.allModes[random.randint(0,2)]
                                self.modeTimer = 600
                                if self.health <150 and self.activeMode!= 'summon':
                                    self.activeMode = self.allModes[random.randint(0,2)]
                                    
                        self.modeTimer -=1
                        if self.activeMode == 'shooting':
                            #move boss away from player if in shooting mode
                            if self.newCommand == 0:
                                atWall = False
                                for i in self.game.floors:
                                    if ((i.rect.left == self.rect.right or i.rect.right == self.rect.left and self.vel.x == 0)
                                        and(i.rect.bottom>self.rect.top and i.rect.top<self.rect.bottom)):
                                        atWall = True
                                if abs(self.rect.center[0]-self.game.player.rect.center[0])<20:
                                    self.direction = directionToPlayer
                                    self.vel.x = self.direction*(self.speed)
                                elif abs(self.rect.center[0]-self.game.player.rect.center[0])<200 and not atWall:
                                    self.direction = -directionToPlayer
                                    self.vel.x = self.direction*(self.speed)
                                else:
                                    self.vel.x = 0
                                    self.direction = directionToPlayer
                                self.newCommand = 50
                            if self.direction == directionToPlayer:
                                shoot = random.randint(1,40)
                                if shoot == 1 and self.shotTimer < 0:
                                    self.shotTimer = 30
                                    if self.direction == 1:
                                        newB = Bullet(self,1,self.game,0,'enemy')
                                        self.game.bullets.add(newB)
                                        self.game.all_sprites.add(newB)
                                    if self.direction == -1:
                                        newB = Bullet(self,-1,self.game,0,'enemy')
                                        self.game.bullets.add(newB)
                                        self.game.all_sprites.add(newB)
                            self.shotTimer -=1
                            
                        if self.activeMode == 'hitting':
                            if self.newCommand <=0:
                                if not self.hitting:
                                    direction = directionToPlayer
                                    self.vel.x = direction*(self.speed)
                                if self.type >=20 and not self.hitting:
                                    if abs(self.rect.center[0]-self.game.player.rect.center[0])<25:
                                        direction = -directionToPlayer
                                        self.vel.x = direction*(self.speed)
                                if self.health >200:
                                    self.newCommand = random.randint(50,75)
                                elif self.health >100:
                                    self.newCommand = random.randint(25,50)
                                else:
                                    self.newCommand = 25
                                
                            if not self.hitting:
                                if (abs(self.rect.center[0]-self.game.player.rect.center[0])<75 and
                                      abs(self.rect.center[0]-self.game.player.rect.center[0])>20):
                                    self.hitting = True
                                    if self.health >200:
                                        self.hitSetup = 5
                                    else: self.hitSetup = 1
                                    self.vel.x = 0
                                    self.direction = directionToPlayer
                                if self.direction == directionToPlayer:
                                    shoot = random.randint(1,50)
                                    if shoot == 1 and self.shotTimer < 0:
                                        self.shotTimer = 40
                                        if self.direction == 1:
                                            newB = Bullet(self,1,self.game,0,'enemy')
                                            self.game.bullets.add(newB)
                                            self.game.all_sprites.add(newB)
                                        if self.direction == -1:
                                            newB = Bullet(self,-1,self.game,0,'enemy')
                                            self.game.bullets.add(newB)
                                            self.game.all_sprites.add(newB)
                            self.shotTimer -=1
                            if self.hitSetup >=0:
                                self.hitSetup-=1
                                if self.hitSetup == 0:
                                    self.ttC = 0
                                    self.picture = 0
                                    h = Hitting(self.game,self)
                                    self.game.hittingGroup.add(h)

                        if self.activeMode == 'summon':
                            self.shotTimer -=1
                            if self.newCommand == 0:
                                atWall = False
                                for i in self.game.floors:
                                    if ((i.rect.left == self.rect.right or i.rect.right == self.rect.left and self.vel.x == 0)
                                        and(i.rect.bottom>self.rect.bottom and i.rect.top<self.rect.top)):
                                        atWall = True
                                if abs(self.rect.center[0]-self.game.player.rect.center[0])<20:
                                    self.direction = directionToPlayer
                                    self.vel.x = self.direction*(self.speed)
                                elif abs(self.rect.center[0]-self.game.player.rect.center[0])<200 and not atWall:
                                    self.direction = -directionToPlayer
                                    self.vel.x = self.direction*(self.speed)
                                else:
                                    self.vel.x = 0
                                    self.direction = directionToPlayer
                                self.newCommand = 50
                            self.newCommand -=1
                            if self.direction == directionToPlayer:
                                shoot = random.randint(1,40)
                                if shoot == 1 and self.shotTimer < 0:
                                    self.shotTimer = 25
                                    if self.direction == 1:
                                        newB = Bullet(self,1,self.game,0,'enemy')
                                        self.game.bullets.add(newB)
                                        self.game.all_sprites.add(newB)
                                    if self.direction == -1:
                                        newB = Bullet(self,-1,self.game,0,'enemy')
                                        self.game.bullets.add(newB)
                                        self.game.all_sprites.add(newB)
                            if self.health >600:
                                spawnEnemy = random.randint(1,290)
                            elif self.health >300:
                                spawnEnemy = random.randint(1,200)
                            else: spawnEnemy = random.randint(1,120)

                            if spawnEnemy == 1 and len(self.game.enemies)<6:
                                firstnum = (random.randint(1,5))*10
                                if firstnum == 10:
                                    firstnum = 0
                                if firstnum == 40:
                                    secondnum = random.randint(0,6)
                                elif firstnum == 50: secondnum = random.randint(1,7)
                                else:secondnum = random.randint(0,5)
                                enemyType = firstnum+secondnum
                                e = Enemy(self.game,enemyType,self.rect.center,'standard',0,1,'none')
                                self.game.all_sprites.add(e)
                                self.game.enemies.add(e)
                                e.health -=1
                                
            #for containing the enemies                
            boundry = py.sprite.spritecollide(self,self.game.Ebound,False)
            if boundry and not self.knockback and self.boundryTimer==0 and not self.alert:
                self.vel.x = -self.vel.x
                self.boundryTimer = 5
                if self.vel.x>0:
                    self.direction = 1
                else: self.direction = -1
            self.newCommand -= 1

            if self.boundryTimer >0:
                self.boundryTimer -=1
            if self.knockback:
                self.knockbackTimer +=1
            if self.knockbackTimer == 45:
                self.knockbackTimer = 0
                self.knockback = False
                self.vel.x = 0

            if self.coldTimer >0:
                self.vel.x = self.vel.x*.4
            self.rect.left += self.vel.x  # X and Y positions are updated
            self.collide(self.vel.x, 0, self.game.floors)
            self.collide(self.vel.x,0,self.game.spikes)
            self.collide(self.vel.x,0,self.game.doors,1)
            if self.coldTimer >0:
                self.vel.x = self.vel.x/0.4
            self.rect.top += self.vel.y
            self.collide(0, self.vel.y, self.game.floors)
            self.collide(0, self.vel.y, self.game.spikes)
            self.animate()
        
    def animate(self):
        if self.vel.x == 0:
            if not self.hitting or self.hitSetup>0:
                if self.direction == 1:
                    if self.picture>len(self.standingr)-1:
                        self.picture = 0
                    self.image = self.standingr[self.picture]
                    if self.ttC == 0:
                        self.picture+=1
                    self.ttC+=1
                    if self.ttC>=24:
                        self.ttC=0 
                    if self.alert:
                        if self.gunner or self.activeMode in ['shooting','summon']:
                            self.image = self.standingrAlert[0]
                        else:
                            self.image = self.batonR[0]
                        
                if self.direction == -1:
                    if self.picture>len(self.standingl)-1:
                        self.picture = 0
                    self.image = self.standingl[self.picture]
                    if self.ttC == 0:
                        self.picture+=1
                    self.ttC+=1
                    if self.ttC>=24:
                        self.ttC=0
                    if self.alert:
                        if self.gunner or self.activeMode in ['shooting','summon']:
                            self.image = self.standinglAlert[0]
                        else:
                            self.image = self.batonL[0]

        if self.vel.x>0:
            if self.picture>len(self.walkingr)-1:
                self.picture=0
            if self.alert:
                if self.gunner or self.activeMode in ['shooting','summon']:
                    self.image = self.gunr[self.picture]
                else:
                    self.image = self.walkingr[self.picture]
            else:
                self.image=self.walkingr[self.picture]
            if self.ttC==0:#right walking animation
                self.picture+=1
            self.ttC+=1
            if self.ttC>=6:#6 frame delay
                self.ttC=0
                    
        if self.vel.x<0:
            if self.picture>len(self.walkingl)-1:
                self.picture=0
            if self.alert:
                if self.gunner or self.activeMode in ['shooting','summon']:
                    self.image = self.gunl[self.picture]
                else:
                    self.image=self.walkingl[self.picture]
            else:
                self.image=self.walkingl[self.picture]
            if self.ttC==0:#left walking animation
                self.picture+=1
            self.ttC+=1#6 frame delay
            if self.ttC>=6:
                self.ttC=0
                                
        if self.hitting and self.hitSetup<=0:
            self.ttC+=1
            if self.picture>=len(self.batonL):
                    self.picture = len(self.batonL)-1
            if self.direction == 1:
                self.image = self.batonR[self.picture]
            else: self.image = self.batonL[self.picture]
            if self.ttC >=5:
                self.ttC = 0
                self.picture+=1
        self.image.set_colorkey(white)
        
    def load_images(self):
        #loading all imagaes for the player sprite
        self.standingr=[]
        self.standingl=[]
        self.walkingr=[]
        self.walkingl=[]
        self.gunr=[]
        self.gunl = []
        self.batonR = []
        self.batonL = []
        if self.type != 101:
            self.standingrAlert = [py.image.load(path.join(self.game.policeIdle,'PoliceShootRight.png')).convert()]
            self.standinglAlert = [py.image.load(path.join(self.game.policeIdle,'PoliceShootLeft.png')).convert()]
            self.standingr.append(py.image.load(path.join(self.game.policeIdle,'Police Idle Right1.png')).convert())
            self.standingr.append(py.image.load(path.join(self.game.policeIdle,'Police Idle Right2.png')).convert())
            self.standingl.append(py.image.load(path.join(self.game.policeIdle,'Police Idle Left1.png')).convert())
            self.standingl.append(py.image.load(path.join(self.game.policeIdle,'Police Idle Left2.png')).convert())
            for i in range(1,9):
                self.walkingr.append(py.image.load(path.join(self.game.policeWalkingR,'PoliceRight'+str(i)+'.png')).convert())
                self.walkingl.append(py.image.load(path.join(self.game.policeWalkingL,'PoliceLeft'+str(i)+'.png')).convert())
                self.gunr.append(py.image.load(path.join(self.game.policeGunR,'PoliceShootRight'+str(i)+'.png')).convert())
                self.gunl.append(py.image.load(path.join(self.game.policeGunL,'PoliceShootLeft'+str(i)+'.png')).convert())
            for i in range(1,7):
                self.batonR.append(py.image.load(path.join(self.game.policeBaton,'Melee'+str(i)+'.png')).convert())
            for i in self.batonR:
                self.batonL.append(py.transform.flip(i,True,False))
        else:
            self.standingrAlert = [py.image.load(path.join(self.game.captainGun,'image-1.png.png')).convert_alpha()]
            self.standinglAlert = [py.image.load(path.join(self.game.captainGun,'image-2.png.png')).convert_alpha()]
            self.standingr.append(py.image.load(path.join(self.game.captainIdle,'Captain idle-1.png.png')).convert_alpha())
            self.standingr.append(py.image.load(path.join(self.game.captainIdle,'Captain idle-2.png.png')).convert_alpha())
            self.standingl.append(py.transform.flip(py.image.load(path.join(self.game.captainIdle,'Captain idle-1.png.png')).convert_alpha(),True,False))
            self.standingl.append(py.transform.flip(py.image.load(path.join(self.game.captainIdle,'Captain idle-2.png.png')).convert_alpha(),True,False))
            for i in range(1,9):
                self.walkingr.append(py.image.load(path.join(self.game.captainWalking,'walking captain-'+str(i)+'.png.png')).convert_alpha())
                self.walkingl.append(py.transform.flip(py.image.load(path.join(self.game.captainWalking,'walking captain-'+str(i)+'.png.png')).convert_alpha(),True,False))
                self.gunr.append(py.image.load(path.join(self.game.captainGunWalk,'walking captain-'+str(i)+'.png.png')).convert_alpha())
                self.gunl.append(py.transform.flip(py.image.load(path.join(self.game.captainGunWalk,'walking captain-'+str(i)+'.png.png')).convert_alpha(),True,False))
            for i in range(1,7):
                self.batonR.append(py.image.load(path.join(self.game.captainMelee,'Captain melee-'+str(i)+'.png.png')).convert_alpha())
            for i in self.batonR:
                self.batonL.append(py.transform.flip(i,True,False))


class NPC(py.sprite.Sprite):#players like dean
    def __init__(self,game,x,y,person,interactType,interact):
        py.sprite.Sprite.__init__(self)
        self.game = game
        self.person = person
        self.interact = interact
        self.interactType = interactType
        if self.person == 'Dean':
            self.right = self.game.DeanIdleR
            self.left = self.game.DeanIdleL
        if self.person == 'Risa':
            self.right = self.game.RisaIdleR
            self.left = self.game.RisaIdleL
        if self.person == 'Saver':
            self.right = self.game.SaverIdleR
            self.left = self.game.SaverIdleL
        self.image = self.right[0]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x,y)
        self.picture = 0
        self.ttC = 0
        self.direction  = 1

    def update(self):#look towards player
        if self.rect.center[0]>self.game.player.rect.center[0]:
            self.direction = -1
        else: self.direction = 1
        self.animate()

    def animate(self):#simple 2 frame animation
        if self.ttC == 0:
            self.picture +=1
            if self.picture>len(self.right)-1:
                self.picture = 0
            if self.direction == 1:
                self.image = self.right[self.picture]
            else: self.image =self.left[self.picture]
        self.ttC +=1
        if self.ttC >25:
            self.ttC = 0

            
class Floor(py.sprite.Sprite):#floor class
    def __init__(self,game,x,y,width,height,speed = 0):
        py.sprite.Sprite.__init__(self)
        self.game = game
        self.image = py.Surface((width,height))
        self.rect = self.image.get_rect()
        self.image.set_colorkey(black)
        self.rect.topleft = (x,y)
        self.speed = speed
        self.collidedwithplayer = False
        

class EnemyBound(py.sprite.Sprite):#prevents enemies from leaving certian areas
    def __init__(self,x,y,width,height):
        py.sprite.Sprite.__init__(self)
        self.rect = py.Rect(x,y,width,height)
        self.image = py.Surface((1,1))
        self.image.set_colorkey(black)

class Bullet(py.sprite.Sprite):#bullet that players and enemies shoot
    def __init__(self,shooter,direction,game,targetPlayer,btype):
        py.sprite.Sprite.__init__(self)
        self.game = game
        self.newBullet = True
        self.flyingBullet = True
        self.destroyBullet= False
        self.Btype = self.game.equipedBullet[0]
        self.gravity = 0
        self.yvel = 0
        self.hits = 1
        self.existTime = 2
        self.hitEnemies = []
        self.user = shooter
        if btype == 'enemy' or btype == self.game.normalBullet:
            if direction == 1:
                self.imageList = self.game.bulletPicsR
            else: self.imageList = self.game.bulletPicsL
            self.type = 'normal'
            self.Btype = self.game.normalBullet
        if btype == self.game.dualBullet:
            if direction == 1:
                self.imageList = self.game.dualBulletPicsR
            else: self.imageList = self.game.dualBulletPicsL
            self.type = 'dual'
        if btype == self.game.snowBullet:
            if direction == 1:
                self.imageList = self.game.snowBulletPicR
            else: self.imageList = self.game.snowBulletPicL
            self.gravity = 0.1
            self.type = 'snow'
        if btype == self.game.sniperBullet:
            if direction == 1:
                self.imageList = self.game.sniperBulletPicR
            else: self.imageList = self.game.sniperBulletPicL
            self.type = 'sniper'
            self.hits = 3
        if btype == self.game.antiBullet:
            if direction == 1:
                self.imageList = self.game.antiBulletPicR
            else: self.imageList = self.game.antiBulletPicL
            self.type = 'anti'
        if btype == self.game.batteryBullet:
            if self.game.batteryTimer >=100:
                if direction == 1:
                    self.imageList = self.game.largeBatBulletPicR
                else: self.imageList = self.game.largeBatBulletPicL
            else:
                if direction == 1:
                    self.imageList = self.game.smallBatBulletPicR
                else: self.imageList = self.game.smallBatBulletPicL
            self.type = 'battery'
            self.batteryTime = self.game.batteryTimer
        self.direction=direction
        self.picture = 0
        self.newPic = 0
        self.animate()
        
        self.rect=self.image.get_rect()
        if direction == 1:
            self.rect.left=shooter.rect.right+10
        else:
            self.rect.right = shooter.rect.left-10
        if shooter in self.game.enemies:
            self.canHit = 1
        else:
            self.canHit = 0
        self.rect.centery=shooter.rect.top+shooter.gunHeight
        if targetPlayer == 1:
            self.canHit = 1
            self.rect.x = 10
        if targetPlayer == 2:
            self.canHit = 1
            self.rect.x = WIDTH-4
        #position bullet according to shooters center, offset by a bit
        
    def update(self):#animate and move the bullet
        self.animate()
        self.existTime -=1
        if self.newBullet:
            self.rect.x+=self.direction*4
        elif self.flyingBullet:
            if self.canHit == 0:
                self.rect.x +=self.direction*10
            self.rect.x+=self.direction*15
            if self.type == 'sniper':
                self.rect.x += self.direction*10
            if self.type == 'anti':
                self.rect.x -= self.direction*18
            self.yvel +=self.gravity
        self.rect.y += self.yvel

    def animate(self):#bullets animation, 3 stages: start, fly, destroy
        if self.Btype == self.game.normalBullet or self.Btype == self.game.dualBullet:
            if self.newBullet:
                if self.newPic == 0:
                    self.image = self.imageList[0][self.picture]
                self.newPic +=1
                if self.newPic>=3:
                    self.newPic = 0
                    self.picture+=1
                    if self.picture>len(self.imageList[0])-1:
                        self.picture = 0
                        self.newBullet = False
                        
            elif self.flyingBullet:
                if self.newPic == 0:
                    self.image = self.imageList[1][self.picture]
                self.newPic +=1
                if self.newPic>=3:
                    self.picture+=1
                    self.newPic = 0
                    if self.picture>len(self.imageList[1])-1:
                        self.picture = 0
                        
            elif self.destroyBullet:
                if self.newPic == 0:
                    self.image = self.imageList[2][self.picture]
                self.newPic+=1
                if self.newPic>=4:
                    self.picture+=1
                    self.newPic = 0
                    if self.picture>len(self.imageList[2])-1:
                        self.kill()
        if self.Btype == self.game.snowBullet:
            self.image = self.imageList
            self.newBullet = False
            if self.destroyBullet: self.kill()

        if self.Btype == self.game.sniperBullet:
            self.newBullet = False
            if self.newPic == 0:
                self.image = self.imageList[self.picture]
            self.newPic +=1
            if self.newPic>=5:
                self.picture+=1
                self.newPic = 0
                if self.picture>len(self.imageList)-1:
                    self.picture = 0
            if self.destroyBullet: self.kill()

        if self.Btype == self.game.antiBullet:
            self.newBullet = False
            if self.newPic == 0:
                self.image = self.imageList[self.picture]
            self.newPic +=1
            if self.newPic>=5:
                self.picture+=1
                self.newPic = 0
                if self.picture>len(self.imageList)-1:
                    self.picture = 0
            if self.destroyBullet:
                for i in range(4):
                    if self.game.bulletLevel[4]==0:
                        damage = 20
                    if self.game.bulletLevel[4]==1:
                        damage = 22
                    if self.game.bulletLevel[4]==2:
                        damage = 24
                    if self.game.bulletLevel[4]==3:
                        damage = 27
                    if self.game.bulletLevel[4]==4:
                        damage = 30
                    if self.game.bulletLevel[4]==5:
                        damage = 33
                    if self.game.bulletLevel[4]==6:
                        damage = 37
                    if self.game.bulletLevel[4]==7:
                        damage = 42
                    if self.game.bulletLevel[4]==8:
                        damage = 47
                    if self.game.bulletLevel[4]==9:
                        damage = 52
                    if self.game.bulletLevel[4]==10:
                        damage = 52
                    
                    c = C4blast(self.game,i,damage,'antiBlast',self)
                    self.game.all_sprites.add(c)
                    self.game.C4Group.add(c)
                self.kill()
                
        if self.Btype == self.game.batteryBullet:
            self.newBullet = False
            if self.newPic == 0:
                self.image = self.imageList[self.picture]
            self.newPic +=1
            if self.newPic>=4:
                self.picture+=1
                self.newPic = 0
                if self.picture>len(self.imageList)-1:
                    self.picture = 0
            if self.destroyBullet: self.kill()
                
class Spike(py.sprite.Sprite):#spikes, made smaller, for collision
    def __init__(self,game,center,w,h,direction):
        py.sprite.Sprite.__init__(self)
        self.game = game
        self.direction = direction
        self.image = py.Surface((w,h))
        self.image.set_colorkey(black)
        self.smallRect=self.image.get_rect()
        self.smallRect.center=center
        ds = DamageSpike(center,w,h)
        self.game.all_sprites.add(ds)
        self.game.damSpikes.add(ds)
        self.rect = self.smallRect.inflate(-2,-2)


class DamageSpike(py.sprite.Sprite):#actual size spikes, cause damage
    def __init__(self,center,w,h):
        py.sprite.Sprite.__init__(self)
        self.image = py.Surface((w,h))
        self.image.set_colorkey(black)
        self.rect = py.Rect(0,0,w,h)
        self.rect.center = center


class otherImg(py.sprite.Sprite):#decoration images
    def __init__(self,bx,by,image):
        py.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.image.set_colorkey(white)
        self.rect.bottomleft = (bx,by)

class Door(py.sprite.Sprite):#door that goes between parts of levels
    def __init__(self,game,x,y,opened,direction,openKeys,openTo):
        py.sprite.Sprite.__init__(self)
        self.game = game
        self.openTo = openTo
        self.direction = direction
        if direction == 'right':
            self.pictures = self.game.doorPicr
        elif direction == 'left':
            self.pictures = self.game.doorPicl
        else: self.pictures = self.game.doorPicBack
        self.finished = False
        self.openKeys = openKeys
        if opened == 0:
            self.opened = False
        else: self.opened = True
        self.closeReady = False
        self.inprocessClose = False
        self.inprocessOpen = False
        self.openTimer = 0
        self.image = self.pictures[0]
        if self.direction[0:4] !='back':
            self.rect = py.Rect(x,y,15,144)
        else:
            if not self.opened:
                if self.game.keys<self.openKeys:
                    self.image = self.pictures[2]
            self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        if self.opened and self.direction[0:4] !='back':
            self.image = self.pictures[3]
            self.openTimer = 18
        elif self.opened:
            self.image = self.pictures[1]
            self.openTimer = 18

    def doorOpening(self):#for image/state when in process opening
        self.openTimer +=1
        if self.direction[0:4] !='back':
            if self.openTimer == 6:
                self.image = self.pictures[1]
            if self.openTimer == 12:
                self.image = self.pictures[2]
            if self.openTimer == 18:
                self.image = self.pictures[3]
                self.inprocessOpen = False
                self.opened = True
        else:
            if self.openTimer == 18:
                self.image = self.pictures[1]
                self.inprocessOpen = False
                self.opened = True

    def doorClosing(self):#for closing doors, not often actually seen
        self.openTimer -=1
        if self.direction[0:4]!='back':
            if self.openTimer == 6:
                self.image = self.pictures[1]
                self.opened = False
            if self.openTimer == 12:
                self.image = self.pictures[2]
            if self.openTimer == 0:
                self.image = self.pictures[0]
                self.inprocessClose = False
        else:
            if self.openTimer == 6:
                self.opened = False
            if self.openTimer == 0:
                self.image = self.pictures[0]
                self.inprocessClose = False
            
class Key(py.sprite.Sprite):#key players can collect to move to new part of level
    def __init__(self,game,x,y,showing,needed,number):
        py.sprite.Sprite.__init__(self)
        self.game = game
        if showing == 0:
            self.showing = False#if the key is outline or actually showing
        else: self.showing = True
        self.needed = needed #requirements for key to turn to showing
        self.pictures = self.game.keyPic
        if self.showing:
            self.image = self.pictures[0]
            self.currentPic = 0
        else:
            self.currentPic = 1
            self.image = self.pictures[1]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.changePic = 0
        self.startpos = (x,y)
        self.number = number

    def update(self):#animation
        if not self.showing:
            if self.changePic == 0:
                self.currentPic +=1
                if self.currentPic >3:
                    self.currentPic = 1
                self.image = self.pictures[self.currentPic]
            self.changePic +=1
            if self.changePic >=10:
                self.changePic = 0


class Coin(py.sprite.Sprite):#coins
    def __init__(self,game,center,value,number):
        py.sprite.Sprite.__init__(self)
        self.game = game
        self.coin = self.game.coins
        self.sparkles = self.game.sparkles
        self.sparkle = False
        self.picture = 0
        self.ttC = 0
        self.Alpha = 255
        self.animate()
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.value = value
        self.number = number
        self.AlphaDirection = -1
        self.y = -10
        self.timer = 600

    def update(self):
        self.animate()
        if self.value == 2:#gravity only if enemy drops it
            self.y +=GRAVITY
            self.rect.y += self.y
            self.collide(0, self.y, self.game.floors)
            self.timer -= 1
            if self.timer < 180:
                self.Alpha +=self.AlphaDirection*15
                if self.Alpha < 0:
                    self.Alpha = 0
                    self.AlphaDirection = 1
                if self.Alpha>255:
                    self.Alpha = 255
                    self.AlphaDirection = -1
            if self.timer <=0:
                self.kill()
        self.image.set_alpha(self.Alpha)
        

    def collide(self, xDif, yDif, platform_list):#collision with floor
        for i in platform_list:
            if py.sprite.collide_rect(self, i):
                if yDif > 0:
                    self.rect.bottom = i.rect.top
                    self.y = 0
                if yDif < 0:
                    self.rect.top = i.rect.bottom
                    self.y = 0

    def animate(self):
        if not self.sparkle:#rotation+sparkles
            if self.ttC == 0:
                self.image = self.coin[self.picture]
            self.ttC +=1
            if self.ttC == 5:
                self.picture+=1
                if self.picture>=len(self.coin):
                    self.picture = 0
                self.ttC = 0
            self.image.set_alpha(self.Alpha)
        else:
            if self.ttC == 0:
                self.image = self.sparkles[self.picture]
            self.ttC+=1
            if self.ttC == 3:
                self.picture+=1
                if self.picture>=len(self.sparkles):
                    self.game.all_sprites.remove(self)
                    self.kill()
                self.ttC = 0 
            
class MoneyBag(py.sprite.Sprite):#vault money bags
    def __init__(self,game,center,value,number):
        py.sprite.Sprite.__init__(self)
        self.game = game
        self.value = value
        self.number = number
        if self.value<500:
            self.image = self.game.moneyBagImg[0]
        elif self.value < 1200:
            self.image = self.game.moneyBagImg[1]
        elif self.value < 2600:
            self.image = self.game.moneyBagImg[2]
        elif self.value < 40000:
            self.image = self.game.moneyBagImg[3]
        self.rect = self.image.get_rect()
        self.rect.center = center


class DroppedHeart(py.sprite.Sprite):#hearts enemies drop
    def __init__(self,game,center,xvel):
        py.sprite.Sprite.__init__(self)
        self.game = game
        self.xvel = xvel
        self.image =  self.game.heartPickup
        self.rect = self.image.get_rect()
        self.rect.center = center
        if xvel == 0:
            self.y = -10
        else: self.y = -5
        self.timer = 600
        self.heartAlpha = 255
        self.heartAlphaDirection = -1
        self.image.set_colorkey(black)

    def update(self):#gravity+destroy
        self.y +=GRAVITY
        self.rect.y += self.y
        self.collide(0, self.y, self.game.floors)
        self.timer -= 1
        if self.xvel >0:
            self.xvel -=.3
        elif self.xvel < 0:
            self.xvel +=.3
        self.rect.x += self.xvel
        self.collide(self.xvel,0,self.game.floors)
        if self.timer < 180:
            self.heartAlpha +=self.heartAlphaDirection*15
            if self.heartAlpha < 0:
                self.heartAlpha = 0
                self.heartAlphaDirection = 1
            if self.heartAlpha>255:
                self.heartAlpha = 255
                self.heartAlphaDirection = -1
        self.image.set_alpha(self.heartAlpha)
        if self.timer <=0:
            self.kill()
        self.image.set_colorkey(black)
        

    def collide(self, xDif, yDif, platform_list):
        for i in platform_list:
            if py.sprite.collide_rect(self, i):
                if yDif > 0:
                    self.rect.bottom = i.rect.top
                    self.y = 0
                    self.xvel = 0
                if yDif < 0:
                    self.rect.top = i.rect.bottom
                    self.y = 0
                if xDif < 0:
                    self.rect.left = i.rect.right
                    self.xvel = 0
                if xDif >0:
                    self.rect.right = i.rect.left
                    self.xvel = 0


class DroppedAmmo(py.sprite.Sprite):
    def __init__(self,game,center):
        py.sprite.Sprite.__init__(self)
        self.game = game
        self.image =  self.game.ammoPickup
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.y = -10
        self.timer = 600
        self.Alpha = 255
        self.AlphaDirection = -1
        self.image.set_colorkey(black)

    def update(self):#destroy+rotate loop
        self.y +=GRAVITY
        self.rect.y += self.y
        self.collide(0, self.y, self.game.floors)
        self.timer -= 1
        if self.timer < 180:
            self.Alpha +=self.AlphaDirection*15
            if self.Alpha < 0:
                self.Alpha = 0
                self.AlphaDirection = 1
            if self.Alpha>255:
                self.Alpha = 255
                self.AlphaDirection = -1
        self.image.set_alpha(self.Alpha)
        if self.timer <=0:
            self.kill()
        self.image.set_colorkey(black)
        

    def collide(self, xDif, yDif, platform_list):
        for i in platform_list:
            if py.sprite.collide_rect(self, i):
                if yDif > 0:
                    self.rect.bottom = i.rect.top
                    self.y = 0
                if yDif < 0:
                    self.rect.top = i.rect.bottom
                    self.y = 0


class signPost(py.sprite.Sprite):
    def __init__(self,center,text):
        py.sprite.Sprite.__init__(self)
        self.text = text
        self.image = py.Surface((64,64))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.image.set_colorkey(black)


class FireStuff(py.sprite.Sprite):
    def __init__(self,game,bottomLeft):
        py.sprite.Sprite.__init__(self)
        self.game = game
        self.images = self.game.movingFire
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = bottomLeft
        if self.game.powerupLevel[7] == 0:
            self.timer = 180
        if self.game.powerupLevel[7] == 1:
            self.timer = 180
        if self.game.powerupLevel[7] == 2:
            self.timer = 180
        if self.game.powerupLevel[7] == 3:
            self.timer = 240
        if self.game.powerupLevel[7] == 4:
            self.timer = 240
        if self.game.powerupLevel[7] == 5:
            self.timer = 240
        if self.game.powerupLevel[7] == 6 or self.game.powerupLevel[7] == 7:
            self.timer = 300
        self.timer = 300
        self.pictures = 0
        self.changePic = 0

    def update(self):
        self.timer -=1
        if self.changePic == 0:
            self.pictures +=1
            if self.pictures >= len(self.images):
                self.pictures = 0
            self.image = self.images[self.pictures]
        if self.timer <=0:
            self.kill()
        self.changePic +=1
        if self.changePic >=12:
            self.changePic = 0


class C4blast(py.sprite.Sprite):
    def __init__(self,game,direction,damage,blastType,user):
        py.sprite.Sprite.__init__(self)
        self.game = game
        self.user = user
        self.damage = damage
        self.blastType = blastType
        self.direction = direction
        if self.blastType == 'C4blast':
            self.image = self.game.C4Directions[direction]
            self.rect = self.image.get_rect()
            self.rect.center = self.game.player.rect.center
        elif self.blastType == 'antiBlast':
            self.images = self.game.antiBlasts[direction]
            self.picture = 0
            self.changePic = 0
            self.animate()
            self.rect = self.image.get_rect()
            self.rect.center = user.rect.center
        

    def update(self):
        if self.blastType == 'C4blast':
            if self.direction == 0:
                self.rect.y -=16
                p = Particles(self.game,(random.randint(220,255),random.randint(220,255),random.randint(0,10)),
                              random.randint((self.rect.left+10),(self.rect.right-10)),
                              self.rect.bottom,8,random.randint(-5,5),None,4,(3,7))
                self.game.particleGroup.add(p)
            if self.direction == 1:
                self.rect.x +=16
                p = Particles(self.game,(random.randint(220,255),random.randint(220,255),random.randint(0,10)),
                              self.rect.left,random.randint((self.rect.top+10),(self.rect.bottom-10)),
                              random.randint(-5,5),-8,None,4,(3,7))
                self.game.particleGroup.add(p)
            if self.direction == 2:
                self.rect.y +=16
                p = Particles(self.game,(random.randint(220,255),random.randint(220,255),random.randint(0,10)),
                              random.randint((self.rect.left+10),(self.rect.right-10)),
                              self.rect.top,-8,random.randint(-5,5),None,4,(3,7))
                self.game.particleGroup.add(p)
            if self.direction == 3:
                self.rect.x -=16
                p = Particles(self.game,(random.randint(220,255),random.randint(220,255),random.randint(0,10)),
                              self.rect.right,random.randint((self.rect.top+10),(self.rect.bottom-10)),
                              random.randint(-5,5),8,None,4,(3,7))
                self.game.particleGroup.add(p)
                
        if self.blastType == 'antiBlast':
            self.animate()
            if self.direction == 0:
                self.rect.y -=16
                p = Particles(self.game,(random.randint(220,255),random.randint(220,255),random.randint(0,10)),
                              random.randint((self.rect.left+10),(self.rect.right-10)),
                              self.rect.bottom,8,random.randint(-5,5),None,4,(3,7))
                self.game.particleGroup.add(p)
            if self.direction == 1:
                self.rect.x +=16
                p = Particles(self.game,(random.randint(220,255),random.randint(220,255),random.randint(0,10)),
                              self.rect.left,random.randint((self.rect.top+10),(self.rect.bottom-10)),
                              random.randint(-5,5),-8,None,4,(3,7))
                self.game.particleGroup.add(p)
            if self.direction == 2:
                self.rect.y +=16
                p = Particles(self.game,(random.randint(220,255),random.randint(220,255),random.randint(0,10)),
                              random.randint((self.rect.left+10),(self.rect.right-10)),
                              self.rect.top,-8,random.randint(-5,5),None,4,(3,7))
                self.game.particleGroup.add(p)
            if self.direction == 3:
                self.rect.x -=16
                p = Particles(self.game,(random.randint(220,255),random.randint(220,255),random.randint(0,10)),
                              self.rect.right,random.randint((self.rect.top+10),(self.rect.bottom-10)),
                              random.randint(-5,5),8,None,4,(3,7))
                self.game.particleGroup.add(p)

        
        if self.rect.x >WIDTH or self.rect.x<0 or self.rect.y>HEIGHT or self.rect.y<0:
            self.kill()

    def animate(self):
        if self.changePic == 0:
            self.image = self.images[self.picture]
            self.picture +=1
            if self.picture >= len(self.images):
                self.picture = 0
            self.changePic = 5
        self.changePic -=1

class MapPlayer(py.sprite.Sprite):
    def __init__(self,game,x,y,group):
        py.sprite.Sprite.__init__(self)
        self.game = game
        self.images = self.game.betweenPlayer
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.timer = 30
        self.xspeed = 0
        self.yspeed = 0
        self.group = group
        self.detect()

    def update(self):
        self.animate()
        self.rect.x += self.xspeed
        self.rect.y += self.yspeed
        self.detect()

    def detect(self):  # Group will be for MapStop objects
        for i in self.group:
            if self.rect.x == i.rect.x and self.rect.y == i.rect.y:
                self.xspeed = 0
                self.yspeed = 0
                self.target = i
        if not self.target:
            print("Player is not on a tile")
            raise AttributeError
            
               
    def animate(self):  # Animate every second
        self.timer -= 1
        if self.timer == 0:
            self.timer = 30
            if self.image == self.images[0]:
                self.image = self.images[1]
            else:
                self.image = self.images[0]

        
class MapStop(py.sprite.Sprite):
    def __init__(self, goLeft, goRight, goUp, goDown, x, y, text):
        py.sprite.Sprite.__init__(self)
        self.goLeft = goLeft
        self.goRight = goRight
        self.goDown = goDown
        self.goUp = goUp
        self.text = text
        self.rect = py.Rect(x,y,64,64)    
