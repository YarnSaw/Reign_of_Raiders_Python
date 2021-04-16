#########################################################
#Ryan Saweczko, Mohamed Ibrahim                         # 
#Revised - 1/17/2019                                    #
#Reign of Raiders                                       #
#Adventure sidescroll game, try to rob all the banks!   #
#########################################################
import sys,time,random
from os import path
import pygame as py
import pygame.freetype
from settings import *
from sprites import *
from tilemap import *
#this class controls the time the player is travelling through levels
class Game:
    def __init__(self,maps):
        #setting up standard variables
        self.goToTitle = False
        self.playerDead = False
        self.levelMenu = True
        self.running = False
        self.wasPaused = False
        #loading ALL images
        self.policeFold = path.join(img_folder,'Police enemy')
        self.policeIdle = path.join(self.policeFold,'Idle')
        self.policeWalkingR = path.join(self.policeFold,'Police Walking Right')
        self.policeWalkingL = path.join(self.policeFold,'Police Walking Left')
        self.policeGunR = path.join(self.policeFold,'Police Shooting Right')
        self.policeGunL = path.join(self.policeFold,'Police Shooting Left')
        self.policeBaton = path.join(self.policeFold, 'Police Melee Attack')
        self.captainIdle = path.join(self.policeFold,'Captain Idle')
        self.captainWalking = path.join(self.policeFold,'Captain Walk')
        self.captainGunWalk = path.join(self.policeFold,'Captain walk shoot')
        self.captainGun = path.join(self.policeFold,'Captain shoot')
        self.captainMelee = path.join(self.policeFold,'Captain melee')
        self.walkingr_fold = path.join(img_folder,'Player walking Right')
        self.walkingl_fold = path.join(img_folder,'player walking Left')
        self.walkingrGunFold = path.join(img_folder,'Gun Right animation')
        self.walkinglGunFold = path.join(img_folder,'Gun Left animation')
        self.gunWhipFold = path.join(img_folder,'Player melee attack')
        self.DeanPicFold = path.join(img_folder,'Dean')
        self.DeanIdleR = [py.image.load(path.join(self.DeanPicFold,'Dean-1.png')),
                         py.image.load(path.join(self.DeanPicFold,'Dean-2.png'))]
        self.DeanIdleL = []
        for i in self.DeanIdleR:
            self.DeanIdleL.append(py.transform.flip(i,True,False))
        self.RisaIdleR = [py.image.load(path.join(img_folder,'Shop keeper-1.png')),
                          py.image.load(path.join(img_folder,'Shop keeper-2.png'))]
        self.RisaIdleL = []
        for i in self.RisaIdleR:
            self.RisaIdleL.append(py.transform.flip(i,True,False))
        self.SaverIdleR = [py.image.load(path.join(img_folder,'Random person idle-1.png')),
                           py.image.load(path.join(img_folder,'Random person idle-2.png'))]
        self.SaverIdleL = []
        for i in self.SaverIdleR:
            self.SaverIdleL.append(py.transform.flip(i,True,False))
        self.teller = py.image.load(path.join(img_folder,'Bank teller stand.png')).convert_alpha()
        self.aboveDoor = py.image.load(path.join(img_folder, 'above door.png'))
        self.spikeFold = path.join(img_folder,'spike')
        self.spikePic = [py.image.load(path.join(self.spikeFold,'Spike1.png'))]
        for i in range(3):
            self.spikePic.append(py.transform.rotate(self.spikePic[0],-(i+1)*90))
        self.bulletFold = path.join(img_folder,'Bullet')
        self.newBulletFold = path.join(self.bulletFold,'newBullet')
        self.flyingBullet = path.join(self.bulletFold,'Bullet Flying')
        self.destroyBullet = path.join(self.bulletFold,'destroyBullet')
        self.bulletPicsR = [[py.image.load(path.join(self.newBulletFold,'Bullet1.png')),
                            py.image.load(path.join(self.newBulletFold,'Bullet2.png')),
                            py.image.load(path.join(self.newBulletFold,'Bullet3.png')),
                            py.image.load(path.join(self.newBulletFold,'Bullet4.png')),
                            py.image.load(path.join(self.newBulletFold,'Bullet5.png'))],
                           [py.image.load(path.join(self.flyingBullet,'FlyingBullet1.png')),
                            py.image.load(path.join(self.flyingBullet,'FlyingBullet2.png')),
                            py.image.load(path.join(self.flyingBullet,'FlyingBullet3.png')),
                            py.image.load(path.join(self.flyingBullet,'FlyingBullet4.png')),
                            py.image.load(path.join(self.flyingBullet,'FlyingBullet5.png')),
                            py.image.load(path.join(self.flyingBullet,'FlyingBullet6.png'))],
                           [py.image.load(path.join(self.destroyBullet,'BulletDestroyed1.png')),
                            py.image.load(path.join(self.destroyBullet,'BulletDestroyed2.png')),
                            py.image.load(path.join(self.destroyBullet,'BulletDestroyed3.png')),
                            py.image.load(path.join(self.destroyBullet,'BulletDestroyed4.png')),
                            py.image.load(path.join(self.destroyBullet,'BulletDestroyed5.png'))]]
        self.moneyBagFold = path.join(img_folder,'Money Bags')
        self.moneyBagImg = [py.image.load(path.join(self.moneyBagFold,'Bag1.png')),
                          py.image.load(path.join(self.moneyBagFold,'Bag2.png')),
                          py.image.load(path.join(self.moneyBagFold,'Bag3.png')),
                          py.image.load(path.join(self.moneyBagFold,'Bag4.png')),
                          py.image.load(path.join(self.moneyBagFold,'Bag5.png'))]
        self.playerWallFold = path.join(img_folder,'Player wall jump')
        self.EnemyDeathFold = path.join(self.policeFold,'Death')
        self.EnemyDeathL = []
        self.EnemyDeathR = []
        self.coinFold = path.join(img_folder,'Coins')
        self.coinsFold = path.join(self.coinFold,'Coin')
        self.sparklesFold = path.join(self.coinFold,'Sparkles')
        self.heartPickup = py.image.load(path.join(img_folder,'Heart pickup.png')).convert()
        self.holdingKey = py.image.load(path.join(img_folder,'holdingKey.png'))
        self.ammoPickup = py.image.load(path.join(img_folder,'ammo pickup.png')).convert()
        self.ammoPickup = py.transform.scale(self.ammoPickup,(32,32))
        self.coins = []
        self.sparkles = []
        for i in range(1,11):
            if i <=6:
                self.coins.append(py.image.load(path.join(self.coinsFold,'Coin'+str(i)+'.png')))
            self.sparkles.append(py.image.load(path.join(self.sparklesFold,'Sparkles'+str(i)+'.png')))
        for i in range(1,12):
            self.EnemyDeathL.append(py.image.load(path.join(self.EnemyDeathFold,'LeftDeath'+str(i)+'.png')))
            self.EnemyDeathR.append(py.transform.flip(self.EnemyDeathL[i-1],True,False))
        self.bulletPicsL=[]
        group = 0
        actual = 0
        #flipping bullet pics for other side
        for i in self.bulletPicsR:
            pics = []
            for p in i:
                transformScale = (32,32)
                self.bulletPicsR[group][actual] = py.transform.scale(p, (48,48))
                pics.append(py.transform.flip(self.bulletPicsR[group][actual],True,False))
                actual+=1
            self.bulletPicsL.append(pics)
            actual = 0
            group+=1
        self.dualBulletPicsR = []
        self.dualBulletPicsL = []
        for i in range(len(self.bulletPicsR)):
            x = []
            y = []
            for h in range(len(self.bulletPicsR[i])):
                x.append(py.transform.scale(self.bulletPicsR[i][h],(32,32)))
                y.append(py.transform.flip(py.transform.scale(self.bulletPicsR[i][h],(32,32)),True,False))
            self.dualBulletPicsR.append(x)
            self.dualBulletPicsL.append(y)
                
        self.heartFold = path.join(img_folder,'Health')
        self.heartsImgOS = [py.image.load(path.join(self.heartFold,'Heart1.png')),
                       py.image.load(path.join(self.heartFold,'Heart2.png')),
                       py.image.load(path.join(self.heartFold,'Heart3.png')),
                       py.image.load(path.join(self.heartFold,'Heart4.png')),
                       py.image.load(path.join(self.heartFold,'Heart5.png'))]
        self.heartsImg = []
        for i in self.heartsImgOS:
            self.heartsImg.append(py.transform.scale(i,(32,32)))
            
        self.doorFold = path.join(img_folder,'Door opening')
        self.doorPicr = [py.image.load(path.join(self.doorFold,'Door1.png')),
                        py.image.load(path.join(self.doorFold,'Door2.png')),
                        py.image.load(path.join(self.doorFold,'Door3.png')),
                        py.image.load(path.join(self.doorFold,'Door4.png'))]
        self.doorPicl = []
        for i in self.doorPicr:
            self.doorPicl.append(py.transform.flip(i, True, False))
        self.doorPicBack = [py.image.load(path.join(self.doorFold,'doorBack1.png')),
                            py.image.load(path.join(self.doorFold,'doorBack2.png')),
                            py.image.load(path.join(self.doorFold,'locked door.png')).convert_alpha()]
        self.keysFold = path.join(img_folder,'Key and outline')
        self.keyPic = [py.image.load(path.join(self.keysFold,'Key.png')),
                       py.image.load(path.join(self.keysFold,'KeyOutline1.png')),
                       py.image.load(path.join(self.keysFold,'KeyOutline2.png')),
                       py.image.load(path.join(self.keysFold,'KeyOutline3.png'))]
        self.exclamationMarkFold = path.join(img_folder,'Exclamation mark animation')
        self.exclamationMark =[py.image.load(path.join(self.exclamationMarkFold,'exclamation mark.png'))]
        #all powerup images
        self.heartPowerup = py.image.load(path.join(img_folder,'Heart PowerUp.png'))
        self.speedPowerup = py.image.load(path.join(img_folder,'Speed PowerUp.png'))
        self.meleePowerup = py.image.load(path.join(img_folder,'Melee PowerUp.png')).convert()
        self.shootingPowerup = py.image.load(path.join(img_folder,'Shooting PowerUp.png'))
        self.valentinesPowerup = py.image.load(path.join(img_folder,'Valentines Day.png')).convert_alpha()
        self.steelPowerup = py.image.load(path.join(img_folder,'Steel Boots.png')).convert_alpha()
        self.quickPowerup = py.image.load(path.join(img_folder,'Quick Trigger.png')).convert_alpha()
        self.firePowerup = py.image.load(path.join(img_folder,'Flame Boots.png')).convert()
        self.C4Powerup = py.image.load(path.join(img_folder,'See four.png')).convert_alpha()
        self.blockPowerup = py.image.load(path.join(img_folder,'BlockMaster.png')).convert_alpha()
        self.deanPowerup = py.image.load(path.join(img_folder,'Deans Medal.png')).convert_alpha()

        self.goldFold = path.join(img_folder,'maxed powerups')
        self.heartPowerupG = py.image.load(path.join(self.goldFold,'Heart PowerUp.png')).convert_alpha()
        self.speedPowerupG= py.image.load(path.join(self.goldFold,'Speed PowerUp.png')).convert_alpha()
        self.meleePowerupG = py.image.load(path.join(self.goldFold,'Melee PowerUp.png')).convert_alpha()
        self.shootingPowerupG = py.image.load(path.join(self.goldFold,'Shooting PowerUp.png')).convert_alpha()
        self.valentinesPowerupG = py.image.load(path.join(self.goldFold,'Valentines Day.png')).convert_alpha()
        self.steelPowerupG = py.image.load(path.join(self.goldFold,'Steel Boots.png')).convert_alpha()
        self.quickPowerupG = py.image.load(path.join(self.goldFold,'Quick Trigger.png')).convert_alpha()
        self.firePowerupG = py.image.load(path.join(self.goldFold,'Flame Boots.png')).convert_alpha()
        self.C4PowerupG = py.image.load(path.join(self.goldFold,'See four.png')).convert_alpha()
        self.blockPowerupG = py.image.load(path.join(self.goldFold,'BlockMaster.png')).convert_alpha()
        self.maxedList = [self.heartPowerupG,self.speedPowerupG,self.shootingPowerupG,self.meleePowerupG,self.valentinesPowerupG,self.quickPowerupG,
                          self.steelPowerupG,self.firePowerupG,self.C4PowerupG,self.blockPowerupG,self.deanPowerup]
        self.firePowerup.set_colorkey(white)
        self.shootingPowerup.set_colorkey(white)
        self.heartPowerup.set_colorkey(white)
        self.meleePowerup.set_colorkey(white)
        self.speedPowerup.set_colorkey(white)
        self.movingFire = [py.image.load(path.join(img_folder,'Flame for flame boots-1.png')).convert(),
                           py.image.load(path.join(img_folder,'Flame for flame boots-2.png')).convert()]
        self.movingFireG =[py.image.load(path.join(self.goldFold,'Flame for flame boots-1.png')).convert_alpha(),
                           py.image.load(path.join(self.goldFold,'Flame for flame boots-2.png')).convert_alpha()]
        for i in self.movingFire:
            i.set_colorkey(black)
        self.speechBubble = py.image.load(path.join(img_folder,'SpeechBubble.png')).convert_alpha()
        self.C4Directions = []
        mainc4= py.image.load(path.join(img_folder,'Blast wave from explosion.png')).convert_alpha()
        self.C4Directions.append(py.transform.rotate(mainc4,90))
        self.C4Directions.append(mainc4)
        self.C4Directions.append(py.transform.rotate(mainc4,-90))
        self.C4Directions.append(py.transform.flip(mainc4,True,False))
        self.betweenPlayer = [py.image.load(path.join(img_folder,"MapPlayer1.png")),
                              py.image.load(path.join(img_folder,"MapPlayer2.png"))] # Both frames for the sprite
        self.mbag = py.image.load(path.join(img_folder,'MBag.png')).convert_alpha()
        #other bullet images load
        self.normalBullet = py.image.load(path.join(self.flyingBullet,'FlyingBullet1.png')).convert_alpha()
        self.dualBullet = py.image.load(path.join(img_folder,'DualBullet.png')).convert_alpha()
        self.extraBulletFold = path.join(img_folder,'extra bullets')
        self.snowBullet = py.image.load(path.join(self.extraBulletFold,'snowball.png')).convert_alpha()
        self.snowBulletPicR = py.transform.scale(self.snowBullet,(32,32))
        self.snowBulletPicL = py.transform.flip(self.snowBulletPicR,True,False)
        self.sniperFolder = path.join(self.extraBulletFold,'Sniper bullets')
        self.sniperBullet = py.image.load(path.join(self.sniperFolder,'sniper bullet1.png')).convert_alpha()
        self.sniperBulletPicR = [py.transform.scale(py.image.load(path.join(self.sniperFolder,'sniper bullet1.png')).convert_alpha(),(32,32)),
                                 py.transform.scale(py.image.load(path.join(self.sniperFolder,'sniper bullet2.png')).convert_alpha(),(32,32)),
                                 py.transform.scale(py.image.load(path.join(self.sniperFolder,'sniper bullet3.png')).convert_alpha(),(32,32)),
                                 py.transform.scale(py.image.load(path.join(self.sniperFolder,'sniper bullet4.png')).convert_alpha(),(32,32))]
        self.sniperBulletPicL = []
        for i in self.sniperBulletPicR:
            self.sniperBulletPicL.append(py.transform.flip(i,True,False))
        self.antiMatterGen = path.join(self.extraBulletFold,'Antimatter bullet')
        self.antiBulletFold = path.join(self.antiMatterGen,'Bullets')
        self.antiBlastFold = path.join(self.antiMatterGen,'Blast Wave')
        self.antiBullet = py.image.load(path.join(self.antiBulletFold,'Antimatter Bullets-1.png')).convert_alpha()
        
        self.antiBlasts=[[py.transform.rotate(py.image.load(path.join(self.antiBlastFold,'Blast from Antimatter bullet-1.png')).convert_alpha(),90),
                          py.transform.rotate(py.image.load(path.join(self.antiBlastFold,'Blast from Antimatter bullet-2.png')).convert_alpha(),90),
                          py.transform.rotate(py.image.load(path.join(self.antiBlastFold,'Blast from Antimatter bullet-3.png')).convert_alpha(),90),
                          py.transform.rotate(py.image.load(path.join(self.antiBlastFold,'Blast from Antimatter bullet-4.png')).convert_alpha(),90),
                          py.transform.rotate(py.image.load(path.join(self.antiBlastFold,'Blast from Antimatter bullet-5.png')).convert_alpha(),90)],
                         [py.image.load(path.join(self.antiBlastFold,'Blast from Antimatter bullet-1.png')).convert_alpha(),
                          py.image.load(path.join(self.antiBlastFold,'Blast from Antimatter bullet-2.png')).convert_alpha(),
                          py.image.load(path.join(self.antiBlastFold,'Blast from Antimatter bullet-3.png')).convert_alpha(),
                          py.image.load(path.join(self.antiBlastFold,'Blast from Antimatter bullet-4.png')).convert_alpha(),
                          py.image.load(path.join(self.antiBlastFold,'Blast from Antimatter bullet-5.png')).convert_alpha()],
                         [py.transform.rotate(py.image.load(path.join(self.antiBlastFold,'Blast from Antimatter bullet-1.png')).convert_alpha(),-90),
                          py.transform.rotate(py.image.load(path.join(self.antiBlastFold,'Blast from Antimatter bullet-2.png')).convert_alpha(),-90),
                          py.transform.rotate(py.image.load(path.join(self.antiBlastFold,'Blast from Antimatter bullet-3.png')).convert_alpha(),-90),
                          py.transform.rotate(py.image.load(path.join(self.antiBlastFold,'Blast from Antimatter bullet-4.png')).convert_alpha(),-90),
                          py.transform.rotate(py.image.load(path.join(self.antiBlastFold,'Blast from Antimatter bullet-5.png')).convert_alpha(),-90)],
                         [py.transform.flip(py.image.load(path.join(self.antiBlastFold,'Blast from Antimatter bullet-1.png')).convert_alpha(),True,False),
                          py.transform.flip(py.image.load(path.join(self.antiBlastFold,'Blast from Antimatter bullet-2.png')).convert_alpha(),True,False),
                          py.transform.flip(py.image.load(path.join(self.antiBlastFold,'Blast from Antimatter bullet-3.png')).convert_alpha(),True,False),
                          py.transform.flip(py.image.load(path.join(self.antiBlastFold,'Blast from Antimatter bullet-4.png')).convert_alpha(),True,False),
                          py.transform.flip(py.image.load(path.join(self.antiBlastFold,'Blast from Antimatter bullet-5.png')).convert_alpha(),True,False)]]

        self.antiBulletPicR = [py.image.load(path.join(self.antiBulletFold,'Antimatter Bullets-1.png')).convert_alpha(),
                               py.image.load(path.join(self.antiBulletFold,'Antimatter Bullets-2.png')).convert_alpha(),
                               py.image.load(path.join(self.antiBulletFold,'Antimatter Bullets-3.png')).convert_alpha(),
                               py.image.load(path.join(self.antiBulletFold,'Antimatter Bullets-4.png')).convert_alpha()]
        self.antiBulletPicL = []
        for i in self.antiBulletPicR:
            self.antiBulletPicL.append(py.transform.flip(i,True,False))
        self.smallbatFold = path.join(self.extraBulletFold,'Small battery bullets')
        self.largebatFold = path.join(self.extraBulletFold,'Big battery bullets')
        self.batteryBullet = py.image.load(path.join(self.largebatFold,'Battery Bullets (Big and Small)-4.png.png')).convert_alpha()
        self.smallBatBulletPicR = [py.image.load(path.join(self.smallbatFold,'Battery Bullets (Big and Small)-1.png.png')).convert_alpha(),
                                   py.image.load(path.join(self.smallbatFold,'Battery Bullets (Big and Small)-2.png.png')).convert_alpha(),
                                   py.image.load(path.join(self.smallbatFold,'Battery Bullets (Big and Small)-3.png.png')).convert_alpha()]
        self.largeBatBulletPicR = [py.image.load(path.join(self.largebatFold,'Battery Bullets (Big and Small)-4.png.png')).convert_alpha(),
                                   py.image.load(path.join(self.largebatFold,'Battery Bullets (Big and Small)-5.png.png')).convert_alpha(),
                                   py.image.load(path.join(self.largebatFold,'Battery Bullets (Big and Small)-6.png.png')).convert_alpha()]
        self.smallBatBulletPicL = []
        for i in self.smallBatBulletPicR:
            self.smallBatBulletPicL.append(py.transform.flip(i,True,False))
        self.largeBatBulletPicL = []
        for i in self.largeBatBulletPicR:
            self.largeBatBulletPicL.append(py.transform.flip(i,True,False))
        self.lockedSlot = py.image.load(path.join(img_folder,'lock.png')).convert_alpha()
        self.bulletSound = py.mixer.Sound(path.join(music_folder,'gunshot.wav'))
        self.heartSound = py.mixer.Sound(path.join(music_folder,'heartPickup.wav'))
        self.hitSound = py.mixer.Sound(path.join(music_folder,'playerHit.wav'))
        self.jumpSound = py.mixer.Sound(path.join(music_folder,'playerJump.wav'))
        self.coinSound = py.mixer.Sound(path.join(music_folder,'collectCoin.wav'))
        self.selectSound = py.mixer.Sound(path.join(music_folder,'newSelect.wav'))
        self.selectImagesFold = path.join(img_folder,'Switch icons')
        self.selectImages = [py.image.load(path.join(self.selectImagesFold,'1 Standard switch.png')).convert_alpha(),
                             py.image.load(path.join(self.selectImagesFold,'2 dual switch.png')).convert_alpha(),
                             py.image.load(path.join(self.selectImagesFold,'3 battery switch.png')).convert_alpha(),
                             py.image.load(path.join(self.selectImagesFold,'4 sniper switch.png')).convert_alpha(),
                             py.image.load(path.join(self.selectImagesFold,'5 snowball switch.png')).convert_alpha(),
                             py.image.load(path.join(self.selectImagesFold,'6 anti switch.png')).convert_alpha()]
        for i in range(len(self.selectImages)):
            self.selectImages[i] = py.transform.scale(self.selectImages[i],(32,32))
        self.orderedBullets = [self.normalBullet,0,0,0,0,0]
        self.coinSound.set_volume(0.2)
        self.jumpSound.set_volume(0.2)
        self.hitSound.set_volume(0.2)
        self.heartSound.set_volume(0.2)
        #initializing variables for the game
        self.clock = py.time.Clock()
        self.map = maps
        #initializing player variables
        self.maxAmmo=105
        self.bulletsClip=15
        self.reload=False
        self.neededB = 0
        self.bulletWait = [0,0,0,0,0,0,0]
        self.bulletTime = [20,28,24,70,3000,10]
        self.bulletLevel = [0,0,0,0,0,0]
        self.powerupLevel = [0,0,0,0,0,0,0,0,0,0,0]
        self.area = 0
        self.unlocked = 1
        self.newGame = True
        self.keys = 0
        self.damaged = False
        self.damagedTimer = FPS
        self.damagedTime = 0
        self.levelGold = 0
        self.totalGold = 0
        self.hearts = 3
        self.healthLeft = self.hearts*3
        self.atHome = False
        self.toShowSpeech = 0
        self.createFire = 30
        self.C4Hits = 0
        self.talkedToDean = 0
        #for changing boundry of the cameras as player moves through map
        #fade screen variables
        self.screenFade = False
        self.screenAlpha = 0
        self.playerAlpha = 255
        self.playerAlphaDirection = -1
        self.fadeTimer = 0
        self.fadeDone = 60
        self.blackness = py.Surface((WIDTH,HEIGHT))
        self.endGameBullets = 0
        self.currentBooster = 0
        self.boosterValue = 8
        self.secondBullet = 0
        self.batteryCharging = False
        self.batteryTimer = 0
        self.skillActive = False
        self.skillTimer = 0
        self.skillNeeded = 6000
        self.skillBarColor = blue
        self.skillBarColorChange = 30
        self.skillBarColorDirec = -1
        self.dualBulletSkillTimer = 5
        self.valentinesTimer = 900
        self.beatBoss = False
        self.speedPercent = 1
        self.currentStolen = 0
        self.doubleJumpAble = True
        self.newGameTimer = 2
        self.newBulletTimer = 0
        #initialize keys for player
        self.moveLeftKey = moveLeftKey
        self.moveRightKey = moveRightKey
        
        #setting pygame groups
        self.floors = py.sprite.Group()
        self.all_sprites = py.sprite.Group()
        self.bullets = py.sprite.Group()
        self.spikes = py.sprite.Group()
        self.cameraBound=py.sprite.Group()
        self.enemies = py.sprite.Group()
        self.bossenemies = py.sprite.Group()
        self.deadEnemies = py.sprite.Group()
        self.damSpikes = py.sprite.Group()
        self.otherImg = py.sprite.Group()
        self.Ebound = py.sprite.Group()
        self.doors = py.sprite.Group()
        self.keysGroup = py.sprite.Group()
        self.keysDone = py.sprite.Group()
        self.allCoins = py.sprite.Group()
        self.hittingGroup = py.sprite.Group()
        self.textBoxes = py.sprite.Group()
        self.moneyBags = py.sprite.Group()
        self.EndLevelObj = py.sprite.Group()
        self.DroppedHeartGroup = py.sprite.Group()
        self.levelMenuGroup = py.sprite.Group()
        self.DroppedAmmoGroup = py.sprite.Group()
        self.NPCs = py.sprite.Group()
        self.signPostGroup = py.sprite.Group()
        self.fireGroup = py.sprite.Group()
        self.C4Group = py.sprite.Group()
        self.particleGroup = py.sprite.Group()
        #initializing camera
        self.camera = vec(WIDTH/2,HEIGHT/2)
        #initializing items/equipables
        self.unlockedSlots = 1
        self.equipedItems = ['none']
        self.purchasedItems = []
        self.forSaleItems = [self.steelPowerup,self.shootingPowerup,self.quickPowerup,self.blockPowerup,self.C4Powerup,self.speedPowerup,
                             self.meleePowerup,self.valentinesPowerup]
        self.notYetForSaleItems = [self.heartPowerup,self.firePowerup,self.deanPowerup]
        self.equipedBullet = [self.normalBullet]
        self.purchasedBullets = []
        self.forSaleBullets = [self.dualBullet,self.sniperBullet,self.batteryBullet,self.antiBullet]
        self.notYetForSaleBullets = [self.snowBullet]
        self.bagsStolen = [0,0,0,0,0,0]
        
    def new(self):#setting up by taking information from map
        #multi-dimensional - 1st layer is which bank. second layer is which setion. 3rd layer is file or map
        self.running=True
        enemyIndex = 0
        keyIndex = 0
        coinIndex = 0
        moneyIndex = 0
        for tile_object in (self.map[self.area][self.openTo][0].tmxdata.objects):#gets all objects from map
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            #placing the objects from tiled
            if tile_object.name == 'Start':
                if self.openDirection == tile_object.direction:
                    offset = vec(-tile_object.x,-tile_object.y)
                if tile_object.direction == 'none':
                    offset = vec(-tile_object.x,-tile_object.y)
            if tile_object.name == 'Player':
                if (self.openDirection == tile_object.direction or
                    tile_object.direction == 'none'):
                    self.player = Player(self,obj_center.x,obj_center.y)
                    self.all_sprites.add(self.player)
                    self.player.canMove = False
            if tile_object.name == 'Floor':
                f =Floor(self,tile_object.x,tile_object.y,
                         tile_object.width,tile_object.height)
                self.floors.add(f)
                self.all_sprites.add(f)
                try:
                    if tile_object.door != 'lolJkWHYTF':
                        imgNeeded = py.Surface((tile_object.width,tile_object.height))
                        imgNeeded.blit(self.aboveDoor,(0,0),(0,0,tile_object.width,tile_object.height))
                        o = otherImg(tile_object.x,tile_object.y+tile_object.height,imgNeeded)
                        self.otherImg.add(o)
                        self.all_sprites.add(o)
                except AttributeError:
                    pass
            if tile_object.name == "Spike":
                s=Spike(self,obj_center,tile_object.width,tile_object.height,tile_object.direction)
                self.spikes.add(s)
                self.all_sprites.add(s)
                s2 = otherImg(tile_object.x,tile_object.y+tile_object.height,self.spikePic[int(tile_object.direction)-1])
                self.otherImg.add(s2)
                self.all_sprites.add(s2)
            if tile_object.name == 'Camera':
                try:
                    c = CameraBound(tile_object.direction,tile_object.x,tile_object.y,tile_object.width,tile_object.height,
                                    int(tile_object.create))
                except AttributeError:
                    c = CameraBound(tile_object.direction,tile_object.x,tile_object.y,tile_object.width,tile_object.height,
                                    -1)
                self.all_sprites.add(c)
                self.cameraBound.add(c)
            if tile_object.name == 'Enemy':
                try:
                    if tile_object.lateSpawn == 'True':
                        if self.keys>=4:
                            e = Enemy(self,int(tile_object.Etype),obj_center,tile_object.mode,0,0,'none')
                            self.all_sprites.add(e)
                            self.enemies.add(e)
                except AttributeError:
                    if self.enemySpawning[self.openTo][enemyIndex] == 1:
                        try:
                            e = Enemy(self,int(tile_object.Etype),obj_center,tile_object.mode,int(tile_object.keyReq),int(tile_object.number),tile_object.text)
                        except AttributeError:
                            e = Enemy(self,int(tile_object.Etype),obj_center,tile_object.mode,int(tile_object.keyReq),int(tile_object.number),'none')
                        self.all_sprites.add(e)
                        self.enemies.add(e)
                    enemyIndex+=1
            if tile_object.name == 'Teller':
                o = otherImg(tile_object.x,tile_object.y+tile_object.height,self.teller)
                self.otherImg.add(o)
                self.all_sprites.add(o)
            if tile_object.name == 'EBound':
                b= EnemyBound(tile_object.x,tile_object.y,tile_object.width,tile_object.height)
                self.all_sprites.add(b)
                self.Ebound.add(b)
            if tile_object.name == 'Door':
                d = Door(self,tile_object.x,tile_object.y,int(tile_object.open),tile_object.direction,
                         int(tile_object.openKeys),int(tile_object.openTo))
                self.all_sprites.add(d)
                self.doors.add(d)
            if tile_object.name == 'Key':
                if self.keySpawning[self.openTo][keyIndex] == 1:
                    k = Key(self,tile_object.x,tile_object.y,int(tile_object.showing),int(tile_object.needed),int(tile_object.number))
                    self.all_sprites.add(k)
                    self.keysGroup.add(k)
                keyIndex = 0
            if tile_object.name == 'Coin':
                if self.coinSpawning[self.openTo][coinIndex] == 1:
                    c = Coin(self,obj_center,int(tile_object.value),int(tile_object.number))
                    self.all_sprites.add(c)
                    self.allCoins.add(c)
                coinIndex+=1
            if tile_object.name == 'Text':
                t = TextTime(obj_center,tile_object.width,tile_object.height,tile_object.text,int(tile_object.keysNeeded))
                self.all_sprites.add(t)
                self.textBoxes.add(t)
            if tile_object.name == 'Money':
                if self.moneybagSpawning[moneyIndex] == 1:
                    if tile_object.number == 11:
                        if self.mondybagSpawning[11] == 1:
                            m = MoneyBag(self,obj_center,int(tile_object.value),int(tile_object.number))
                            self.all_sprites.add(m)
                            self.moneyBags.add(m)
                    else:
                        m = MoneyBag(self,obj_center,int(tile_object.value),int(tile_object.number))
                        self.all_sprites.add(m)
                        self.moneyBags.add(m)
            if tile_object.name == 'EndGame':
                if int(tile_object.neededKeys) == self.keys:
                    e = EndLevel(obj_center,tile_object.width,tile_object.height,tile_object.file)
                    self.all_sprites.add(e)
                    self.EndLevelObj.add(e)
                moneyIndex +=1
            if tile_object.name == 'LevelMenu':
                m = menu(obj_center)
                self.levelMenuGroup.add(m)
                self.all_sprites.add(m)
            if tile_object.name == 'NPC':
                if tile_object.interactType != 'fireBoots' and tile_object.interactType != 'snowBullet':
                    n = NPC(self,tile_object.x,tile_object.y+tile_object.height,tile_object.person,tile_object.interactType,tile_object.interact)
                    self.all_sprites.add(n)
                    self.NPCs.add(n)
                elif tile_object.interactType == 'fireBoots':
                    for i in self.notYetForSaleItems:
                        if i == self.firePowerup:
                            n = NPC(self,tile_object.x,tile_object.y+tile_object.height,tile_object.person,tile_object.interactType,tile_object.interact)
                            self.all_sprites.add(n)
                            self.NPCs.add(n)
                elif tile_object.interactType == 'snowBullet':
                    for i in self.notYetForSaleBullets:
                        if i == self.snowBullet:
                            n = NPC(self,tile_object.x,tile_object.y+tile_object.height,tile_object.person,tile_object.interactType,tile_object.interact)
                            self.all_sprites.add(n)
                            self.NPCs.add(n)
            if tile_object.name == 'Sign':
                s = signPost(obj_center,tile_object.text)
                self.all_sprites.add(s)
                self.signPostGroup.add(s)
        #setting where all sprites have to start
        for i in self.all_sprites:
            i.rect.center+=offset
        self.mapTL = vec(offset.x,offset.y)
        offset = -self.camera + vec(WIDTH/2,HEIGHT/2)
        self.mapTL +=offset
        self.nextOpenTo = -10
        #only when entering boss room first time, stopping timer
        if self.openTo == self.bossRoom and len(self.enemies)>0:
            pastTime = time.time()
            leftTime = self.maxTime - (pastTime-self.timeStart)
            self.maxTime = leftTime
            self.bossMaxhealth = 0
            for i in self.enemies:
                self.bossMaxhealth += i.maxHealth
            if self.area == 5:
                py.mixer.music.load(path.join(music_folder,'bfmusic.mp3'))
                py.mixer.music.play()
                py.mixer.music.pause()
        self.speedPercent = 1
        for item in self.equipedItems:
            if item == self.steelPowerup:
                if self.powerupLevel[6] == 0:
                    self.speedPercent -=.4
                if self.powerupLevel[6] == 1:
                    self.speedPercent -=.35
                if self.powerupLevel[6] == 2:
                    self.speedPercent -=.3
                if self.powerupLevel[6] == 3:
                    self.speedPercent -=.2
                if self.powerupLevel[6] == 4 or self.powerupLevel[6] == 5:
                    self.speedPercent -=.1
        self.speedPercent -= 0.03*self.currentStolen
        if self.mode == 'easy':
            self.speedPercent +=0.015*self.currentStolen
        
        self.draw()
        self.newGameTimer = 2
        #control timer for game
            
    def run(self):
        #running through all the menues
        while not self.goToTitle:
            if self.levelMenu:
                self.levelMenuScreen()
            if self.playerDead:
                self.dead()
            while self.running:
                self.clock.tick(FPS)
                self.update()
                self.events()
                self.draw()
            

    def update(self):
        self.newGameTimer -=1
        if self.newGameTimer == 0: self.player.canMove = True
        self.toShowSpeech = 0
        self.all_sprites.update()
        self.hittingGroup.update()
        self.particleGroup.update()
        #update music
        if not py.mixer.music.get_busy():
            if self.area == 0:
                py.mixer.music.load(path.join(music_folder,'mmmusic.mp3'))
            if self.area == 1:
                py.mixer.music.load(path.join(music_folder,'l1music.mp3'))
            if self.area == 2:
                py.mixer.music.load(path.join(music_folder,'l2music.mp3'))
            if self.area == 3:
                py.mixer.music.load(path.join(music_folder,'l3music.mp3'))
            if self.area == 4:
                py.mixer.music.load(path.join(music_folder,'l4music.mp3'))
            if self.area == 5:
                if self.openTo == self.bossRoom:
                    py.mixer.music.load(path.join(music_folder,'bfmusic.mp3'))
                else:
                    py.mixer.music.load(path.join(music_folder,'l5music.mp3'))
            py.mixer.music.play()
        #update camera
        follow = vec(self.player.rect.x,self.player.rect.y)
        difference = follow - self.camera
        self.camera += difference
        offset = -self.camera + vec(WIDTH/2,HEIGHT/2)
        #update object positions due to new camera
        for i in self.all_sprites:
            i.rect.top+=offset.y
            i.rect.left+=offset.x
        self.mapTL+=offset
        #changing the camera offset if the player is in a corner of the screen
        for i in self.cameraBound:
            if ((i.direction==1 and i.rect.bottom>0) or (i.direction == 3 and i.rect.top<HEIGHT)) and i.showing:
                for a in self.all_sprites:
                    a.rect.top-=offset.y
                self.mapTL.y-=offset.y
            if ((i.direction == 2 and i.rect.x<WIDTH) or (i.direction == 4 and i.rect.right>0)) and i.showing:
                for a in self.all_sprites:
                    a.rect.left-=offset.x
                self.mapTL.x-=offset.x
                if self.player.rect.x>WIDTH+5:
                    offset.x = self.player.rect.left
                    for a in self.all_sprites:
                        a.rect.left-=offset.x
                    self.mapTL.x-=offset.x
                if self.player.rect.right<-7:
                    offset.x = -WIDTH+self.player.rect.right
                    for a in self.all_sprites:
                        a.rect.left-=offset.x
                    self.mapTL.x-=offset.x
            #creating screen fade if the player passes through a camera
            if ((i.direction == 1 and self.player.rect.bottom<i.rect.top) or
                (i.direction == 2 and self.player.rect.left > i.rect.left) or
                (i.direction == 3 and self.player.rect.top > i.rect.bottom) or
                (i.direction == 4 and self.player.rect.right < i.rect.right)) and i.showing:
                i.showing = False
                self.screenFade = True
                self.player.gActivated = False
                self.player.vel.y = 0
        #for any time i need to know state of keyboard in updates
        pressed = py.key.get_pressed()
        #particles in the second and third levels
        if self.area == 2 and self.openTo >1:
            p = Particles(self,(random.randint(200,255),random.randint(0,50),random.randint(0,50)),
                          random.randint(-300,1300),768,-5,random.randint(-5,5),'x',4,(12,20))
            self.particleGroup.add(p)
            p = Particles(self,(random.randint(200,255),random.randint(0,50),random.randint(0,50)),
                          random.randint(-300,1300),768,-5,random.randint(-5,5),'x',4,(12,20))
            self.particleGroup.add(p)
        if self.area == 3:
            p = Particles(self,(random.randint(250,255),random.randint(250,255),random.randint(250,255)),
                          random.randint(-300,1300),0,3,random.randint(-5,5),'x',1,(7,10))
            self.particleGroup.add(p)
            p = Particles(self,(random.randint(230,255),random.randint(230,255),random.randint(250,255)),
                          random.randint(-300,1300),0,3,random.randint(-5,5),'x',1,(7,10))
            self.particleGroup.add(p)

        #battery bullet charge
        if self.batteryCharging:
            self.batteryTimer +=1
            
        for i in self.bullets:
            if i.existTime == 1:
                self.bulletSound.play()
                self.bulletSound.set_volume(0.2)
            #checking for collision with walls/doors to destroy the object
            collision = py.sprite.spritecollide(i,self.floors,False)
            if collision and not i.destroyBullet:
                i.newBullet = False
                i.destroyBullet = True
                i.flyingBullet = False
                i.newPic = 0
                i.picture = 0
            for d in self.doors:
                coll2 = py.sprite.collide_rect(i,d)
                if coll2 and not i.destroyBullet and d.direction[0:4] !='back':
                    i.newBullet = False
                    i.destroyBullet = True
                    i.flyingBullet = False
                    i.newPic = 0
                    i.picture = 0
            #checking if bullet is offscreen to kill it
            if i.rect.x<0 or i.rect.x>WIDTH:
                i.kill()
            #if bullet collides with enemies
            if i.canHit == 0:
                for e in self.enemies:
                    collision = py.sprite.collide_rect(i,e)
                    if collision and not i.destroyBullet:
                        nomore = False#checking for sniper bullet to make sure enemies
                        for hitalready in i.hitEnemies:#are not hit multiple times by 1 bullet
                            if e == hitalready:
                                nomore = True
                        if not nomore:
                            if i.type == 'normal':
                                e.health -=8
                                if self.bulletLevel[0]>=1:
                                    e.health -=2
                                if self.bulletLevel[0]>=2:
                                    e.health -=2
                                if self.bulletLevel[0]>=3:
                                    e.health -=3
                                if self.bulletLevel[0]>=4:
                                    e.health -=3
                                if self.bulletLevel[0]>=5 and self.bulletsClip <=8:
                                    e.health -=5
                            if i.type == 'dual':
                                e.health -=5
                                if self.bulletLevel[1]>=1:
                                    e.health -=1
                                if self.bulletLevel[1]>=2:
                                    e.health -=1
                                if self.bulletLevel[1]>=3:
                                    e.health -=1
                                if self.bulletLevel[1]>=4:
                                    e.health -=1
                            if i.type == 'snow':
                                e.health -=6
                                e.coldTimer = 180
                                if self.bulletLevel[2]>=1:
                                    e.health -=1
                                if self.bulletLevel[2]>=2:
                                    e.health -=1
                                if self.bulletLevel[2]>=3:
                                    e.health -=1
                                if self.bulletLevel[2]>=4:
                                    e.health -=1
                                if self.bulletLevel[2]>=5:
                                    e.health -=2
                                if self.bulletLevel[2]>=6:
                                    e.health -=4
                            if i.type == 'sniper':
                                e.health -=15
                                if self.bulletLevel[3]>=1:
                                    e.health -=2
                                if self.bulletLevel[3]>=2:
                                    e.health -=3
                                if self.bulletLevel[3]>=3:
                                    e.health -=4
                                if self.bulletLevel[3]>=4:
                                    e.health -=5
                                if self.bulletLevel[3]>=5:
                                    e.health -=5
                                if self.bulletLevel[3]>=6:
                                    e.health -=5
                                if self.bulletLevel[3]==7:
                                    if i.hits ==2:
                                        e.health -= 5
                                    if i.hits == 1:
                                        e.health -= 10
                            if i.type == 'anti':
                                e.health -= 150
                                if e.type == 100 or e.type == 101:
                                    e.health +=40
                            if i.type == 'battery':#need to control uncharged and fully charged damage for each level of the battery bullet
                                if self.bulletLevel[5] == 0:
                                    if i.batteryTime >= 100:
                                        e.health -=16
                                    else:
                                        e.health -= int(i.batteryTime/8)
                                if self.bulletLevel[5] == 1:
                                    if i.batteryTime >= 100:
                                        e.health -=19
                                    else:
                                        e.health -= int(i.batteryTime/8)
                                if self.bulletLevel[5] == 2:
                                    if i.batteryTime >= 100:
                                        e.health -=22
                                    else:
                                        e.health -= int(i.batteryTime/7)
                                if self.bulletLevel[5] == 3:
                                    if i.batteryTime >= 100:
                                        e.health -=26
                                    else:
                                        e.health -= int(i.batteryTime/7)
                                if self.bulletLevel[5] == 4:
                                    if i.batteryTime >= 100:
                                        e.health -=30
                                    else:
                                        e.health -= int(i.batteryTime/6)
                                if self.bulletLevel[5] == 5:
                                    if i.batteryTime >= 100:
                                        e.health -=34
                                    else:
                                        e.health -= int(i.batteryTime/5)
                                if self.bulletLevel[5] == 6:
                                    if i.batteryTime >= 100:
                                        e.health -=39
                                    else:
                                        e.health -= int(i.batteryTime/4)
                                if self.bulletLevel[5] == 7:
                                    if i.batteryTime >= 100:
                                        e.health -=46
                                    else:
                                        e.health -= int(i.batteryTime/4)
                                if self.bulletLevel[5] == 8:
                                    if i.batteryTime >= 100:
                                        e.health -=53
                                    else:
                                        e.health -= int(i.batteryTime/3)
                                if self.bulletLevel[5] == 9:
                                    if i.batteryTime >= 100:
                                        e.health -=60
                                    else:
                                        e.health -= int(i.batteryTime/2)
                                if self.bulletLevel[5] == 10:
                                    if i.batteryTime >= 100:
                                        e.health -=60
                                    else:
                                        e.health -= int(i.batteryTime/2)
                                        
                            e.knockback = True
                            e.damaged = True
                            if e.rect.center[0] > self.player.rect.center[0]:
                                e.vel.x= 3
                            else:
                                e.vel.x = -3
                            e.vel.y = -5
                            i.hits -=1
                            if i.hits == 0:
                                i.newBullet = False
                                i.flyingBullet = False
                                i.destroyBullet = True
                                i.newPic = 0
                                i.picture = 0
                            else: i.hitEnemies.append(e)
                            if self.skillNeeded<6000:
                                self.skillNeeded +=180
                            
            #if bullet collides with the player
            collision = py.sprite.collide_rect(i,self.player)
            if collision and not i.destroyBullet and i.canHit == 1 and not self.screenFade:
                i.newBullet = False
                i.destroyBullet = True
                i.flyingBullet = False
                i.newPic = 0
                i.picture = 0
                if not self.damaged:
                    self.C4Hits +=1
                    self.damaged = True
                    if not self.skillActive:#prevents damage if player is using skill
                        downHealth = 1
                        if i.user.type != 'Player':#end level bullet fix
                            if i.user.type>=30:#increase damage in later levels
                                downHealth +=1
                            if i.user.type >=40:
                                downHealth +=1
                            if i.user.type >=50 and self.mode == 'normal':
                                downHealth +=1
                            if self.bulletLevel[2]==7:#decrease damage if frozen/deans medalion
                                if i.user.coldTimer >0:
                                    downHealth = int(round(downHealth/2,0))
                            if self.deanPowerup in self.equipedItems:
                                downHealth = int(round(downHealth/2,0))
                            if downHealth == 0:
                                downHealth = 1
                        else:#end level bullets damage
                            downHealth = 1
                            if time.time()-self.timeStart>self.maxTime+20:
                                downHealth +=1
                            if time.time()-self.timeStart>self.maxTime+40:
                                downHealth +=1
                        self.healthLeft -= downHealth
                        self.hitSound.play()
                        noKb = False#no kb if the steel powerup is maxed/equiped
                        for items in self.equipedItems:
                            if items == self.steelPowerup and self.powerupLevel[6] == 5:
                                noKb = True
                        if not noKb:
                            self.player.knockback = True
                            self.player.knockbackTimer +=10
                            if self.player.rect.center[0] > i.user.rect.center[0]:
                                self.player.vel.x= 5
                            else:
                                self.player.vel.x = -5
                            self.player.vel.y = -10

        #for collision with the spikes from the player
        for i in self.spikes:
            if (self.player.rect.bottom == i.rect.top and i.direction == '1' or
                self.player.rect.left == i.rect.right and i.direction == '2' or
                self.player.rect.top == i.rect.bottom and i.direction == '3' or
                self.player.rect.right == i.rect.left and i.direction == '4'):
                for i in self.damSpikes:
                    collision2 = py.sprite.collide_rect(self.player,i)
                    noDam = False
                    for i in self.equipedItems:
                        if i == self.steelPowerup:
                            noDam = True
                    if collision2 and not self.damaged and not noDam:
                        self.healthLeft -=4
                        self.damaged = True
                        break
        #the hitting group, for enemy and player melee attacks
        for h in self.hittingGroup:
            #hitting the player
            if h.canHit == 0 and not self.screenFade and h.timer<=15:
                collision = py.sprite.collide_rect(self.player,h)
                if collision and not self.damaged:
                    self.C4Hits +=1
                    self.damaged = True
                    if not self.skillActive:#same damage as for bullets, but for melee attacks now
                        downHealth = 0
                        downHealth +=1
                        if h.user.type>=30:
                            downHealth +=1
                        if h.user.type >=40:
                            downHealth +=1
                        if h.user.type >=50 and self.mode == 'normal':
                            downHealth +=1
                        if self.bulletLevel[2]==7:
                            if h.user.coldTimer >0:
                                downHealth = int(round(downHealth/2,0))
                        if self.deanPowerup in self.equipedItems:
                            downHealth = int(round(downHealth/2,0))
                        if downHealth == 0:
                            downHealth = 1
                        self.healthLeft -= downHealth
                        self.hitSound.play()

                        noKb = False
                        for i in self.equipedItems:
                            if i == self.steelPowerup and self.powerupLevel[6] == 5:
                                noKb = True
                        if not noKb:
                            self.player.knockback = True
                            if self.player.rect.center[0] > h.user.rect.center[0]:
                                self.player.vel.x= 5
                            else:
                                self.player.vel.x = -5
                            self.player.vel.y = -10
            elif h.timer<=8:
                #hitting the enemy
                for e in self.enemies:
                    collision = py.sprite.collide_rect(h,e)
                    if collision and not e.damaged:
                        for item in self.equipedItems:
                            if item == self.meleePowerup:#control extra damage if brass knuckles equiped
                                instaKill = random.randint(1,100)
                                chance = 0
                                if self.powerupLevel[3] == 0:
                                    chance = 2
                                if self.powerupLevel[3] == 1:
                                    chance = 3
                                if self.powerupLevel[3] == 2:
                                    chance = 4
                                if self.powerupLevel[3] == 3:
                                    chance = 6
                                if self.powerupLevel[3] == 4:
                                    chance = 8
                                if self.powerupLevel[3] == 5:
                                    chance = 11
                                if self.powerupLevel[3] == 6:
                                    chance = 14
                                if self.powerupLevel[3] == 7:
                                    chance = 17
                                if self.powerupLevel[3] == 8:
                                    chance = 21
                                if self.powerupLevel[3] == 9 or self.powerupLevel[3] == 10:
                                    chance = 25
                                if instaKill <=chance:
                                    e.health -=50
                        e.damaged = True
                        e.health -=6
                        for i in self.equipedItems:
                            if i == self.shootingPowerup:
                                if self.powerupLevel[2] == 7:
                                    e.health -=6
                            if i == self.meleePowerup:
                                if self.powerupLevel[3] == 10:
                                    e.health -=6
                        e.quickHit +=1
                        e.quickHitTimer = 20
                        if e.quickHit == 3:
                            e.knockback = True
                            if e.rect.center[0] > h.user.rect.center[0]:
                                e.vel.x= 8
                            else:
                                e.vel.x = -8
                            e.vel.y = -6
                        if self.skillNeeded<6000:
                            self.skillNeeded +=180
            if h.canHit != 0:#block the bullets if block powerup is equiped
                for i in self.equipedItems:
                    if i == self.blockPowerup:
                        for b in self.bullets:
                            collision = py.sprite.collide_rect(b,h)
                            if collision and not b.destroyBullet:
                                b.newBullet = False
                                b.destroyBullet = True
                                b.flyingBullet = False
                                b.newPic = 0
                                b.picture = 0
                                if self.powerupLevel[9] == 1:#if blockmaster is max, release blast wave
                                    if b.direction == 1:
                                        c = C4blast(self,3,8,'C4blast',self.player)
                                        self.all_sprites.add(c)
                                        self.C4Group.add(c)
                                    if b.direction == -1:
                                        c = C4blast(self,1,8,'C4blast',self.player)
                                        self.all_sprites.add(c)
                                        self.C4Group.add(c)
                                    
        #what happens to the enemies in main loop
        for e in self.enemies:
            if py.sprite.collide_rect(e,self.player):
                if e.text !='none' and not e.alert:
                    self.toShowSpeech = 1
                if e.text != 'none' and not e.alert and pressed[enterDoorKey] and self.player.vel.y == 0:
                    e.vel.x = 0
                    e.image=e.standingr[0]
                    self.printText(e.text)
            if e.damaged:#control different types of damage/effects on enemies
                e.damagedTimer +=1
                if e.damagedTimer >=13:
                    e.damagedTimer = 0
                    e.damaged = False
            if e.fireDamage:
                e.fireDamageTimer -=1
                if e.fireDamageTimer == 0:
                    e.fireDamageTimer = 60
                    e.fireDamage = False
            if e.coldTimer>0:
                e.coldTimer -=1
                new_img = e.image.copy()  # Create copy of image
                new_img.fill((0,50,150),special_flags = pygame.BLEND_RGB_ADD)  # Blend it
                e.image = new_img
            if (e.damaged and e.damagedTimer <=4) or (e.fireDamage and e.fireDamageTimer>=53):
                new_img = e.image.copy()  # Create copy of image
                new_img.fill((254,254,254),special_flags = pygame.BLEND_RGB_SUB)  # Blend it
                new_img.fill((254,254,254),special_flags = pygame.BLEND_RGB_ADD)  # Blend it
                e.image = new_img
            if not e.alert and e.health!=e.maxHealth:
                e.alert = True
                e.newAlert = True
                if not self.timerStart and self.openTo != self.bossRoom:
                    self.timerStart = True
                    self.timeStart = time.time()
            #check for enemy deaths
            if e.health <=0:
                self.deadEnemies.add(e)
                self.enemies.remove(e)
                
                for i in self.equipedItems:
                    if i == self.firePowerup and self.powerupLevel[7]==7:
                        self.maxTime +=5
                        
                if e.keyReq != 0 and e.keyReq != -1:
                    for k in self.keysGroup:
                        if e.keyReq == k.needed:
                            k.showing = True
                            k.image = k.pictures[0]
                self.enemySpawning[self.openTo][e.number] = 0
                if e.keyReq == -1:
                    self.bossDown+=1
                if self.bossDown==self.allBosses:
                    for k in self.keysGroup:
                        if e.keyReq == -1:
                            k.showing = True
                            k.image = k.pictures[0]
                    self.bossDown+=1
                    if self.area == 5:#cut scene for killing final boss
                        py.mixer.music.pause()
                        self.deadEnemies.remove(e)
                        self.bossenemies.add(e)
                        #kill everything
                        for i in self.particleGroup:
                            i.kill()
                        for i in self.bullets:
                            i.kill()
                        for i in self.C4Group:
                            i.kill()
                        for i in self.enemies:
                            i.kill()
                        for i in self.deadEnemies:
                            i.kill()
                        for i in self.allCoins:
                            i.kill()
                        for i in self.DroppedHeartGroup:
                            i.kill()
                        for i in self.DroppedAmmoGroup:
                            i.kill()
                        for i in self.fireGroup:
                            i.kill()
                        self.player.vel.x = 0
                        self.player.direction = 1
                        self.player.gunDrawn = False
                        for alphaval in self.player.allPlayerImages:
                            for secondalpha in alphaval:
                                secondalpha.set_alpha(255)
                        self.damaged = False
                        self.damagedTime = 0
                        self.playerAlpha = 255
                        self.playerAlphaDirection = -1
                        self.player.animate()
                        self.player.canMove = False
                        firstLoop = True
                        e.damaged = False
                        e.alert = False
                        e.vel.x = 0
                        e.animate()
                        #make sure player is standing on the ground
                        while firstLoop:
                            self.draw()
                            for i in self.floors:
                                if (self.player.rect.bottom == i.rect.top and
                                (self.player.rect.left < i.rect.right or self.player.rect.right > i.rect.left)) and not self.player.hitting:
                                    firstLoop = False
                            clock.tick(FPS)
                            for event in py.event.get():
                                if event.type == py.QUIT:
                                    py.quit()
                                    py.mixer.quit()
                                    exit()
                            self.player.update()
                        if e.rect.center[0]>self.player.rect.center[0]:
                            e.direction = -1
                            self.player.direction = 1
                        else:
                            self.player.direction = -1
                            e.direction = 1
                        
                        e.animate()
                        self.printText('endboss.txt')
                        for i in range(250):
                            if e.picture>len(e.standingl)-1:
                                    e.picture = 0 
                            if e.direction == 1:
                                e.image = e.standingr[e.picture]
                            if e.direction == -1:
                                e.image = e.standingl[e.picture]
                            if e.ttC == 0:
                                e.picture+=1
                            e.ttC+=1
                            if e.ttC>=24:
                                e.ttC=0
                            new_img = e.image.copy()
                            new_img.fill((i,i,i),special_flags = py.BLEND_RGB_ADD)
                            e.image = new_img
                            e.image.set_colorkey(white)
                            self.draw()
                            clock.tick(FPS)
                            for event in py.event.get():
                                if event.type == py.QUIT:
                                    py.quit()
                                    py.mixer.quit()
                                    exit()
                        e.kill()
                        self.draw()
                        for i in range(60):
                            clock.tick(FPS)
                            for event in py.event.get():
                                if event.type == py.QUIT:
                                    py.quit()
                                    py.mixer.quit()
                                    exit()
                        self.printText('endgame.txt')
                        #same stuff as if the player hits the end level object
                        self.totalGold += self.levelGold
                        self.timerStart = False
                        self.speedPercent = 1
                        for item in self.equipedItems:
                            if item == self.steelPowerup:
                                if self.powerupLevel[6] == 0:
                                    self.speedPercent -=.4
                                if self.powerupLevel[6] == 1:
                                    self.speedPercent -=.35
                                if self.powerupLevel[6] == 2:
                                    self.speedPercent -=.3
                                if self.powerupLevel[6] == 3:
                                    self.speedPercent -=.2
                                if self.powerupLevel[6] == 4 or self.powerupLevel[6] == 5:
                                    self.speedPercent -=.1
                        if self.unlocked == self.area:
                            self.unlocked +=1
                        self.healthLeft = self.hearts * 4
                        self.ammo=0
                        self.bulletsClip=0
                        self.screenFade = True
                        self.player.gActivated = False
                        self.player.vel.y = 0
                        self.nextOpenTo = 0
                        self.openDirection = 'left'
                        if self.boosterValue <18:
                            self.boosterValue +=2
                        if self.levelGold > self.bagsStolen[self.area-1]:
                            self.bagsStolen[self.area-1] = self.levelGold
                        self.area = 0
                        self.levelGold = 0
                        self.beatBoss = True
                        
                    self.timeStart = time.time()
                    pastTime = time.time()
                    minusTime = pastTime - self.timeStart
                    leftTime = self.maxTime - minusTime
                            
        #if enemy is dead, to display death animation
        for e in self.deadEnemies:
            if e.deadTimer <45:
                e.deadTimer +=1
                if e.deadTimer%4 == 0:
                    e.deadPicture+=1
                    if e.deadPicture >len(self.EnemyDeathL)-1:
                        e.deadPicture -=1
                if e.direction == 1:
                    e.image = self.EnemyDeathR[e.deadPicture]
                else: e.image = self.EnemyDeathL[e.deadPicture]
            if (e.deadTimer == 45) and e.mode !='dead':
                #enemies dropping coins/other items
                dropItem = random.randint(1,100)
                if dropItem <=65:
                    c = Coin(self,e.rect.center,2,-1)
                    self.all_sprites.add(c)
                    self.allCoins.add(c)
                elif dropItem <=85:
                    c = DroppedHeart(self,e.rect.center,0)
                    self.all_sprites.add(c)
                    self.DroppedHeartGroup.add(c)
                else:
                    c = DroppedAmmo(self,e.rect.center)
                    self.all_sprites.add(c)
                    self.DroppedAmmoGroup.add(c)
                if e.keyReq >0:
                    k = Key(self,e.rect.center[0],e.rect.center[1],1,1,1)
                    self.all_sprites.add(k)
                    self.keysGroup.add(k)
                e.kill()
                
        #other NPCs with their interactions
        for n in self.NPCs:
            if py.sprite.collide_rect(n,self.player):
                self.toShowSpeech = 1
                if pressed[enterDoorKey] and self.player.vel.y == 0:
                    #everything that can happen when you talk to dean
                    if n.interactType == 'DeanTalks':
                        if self.talkedToDean == 0 and self.unlocked >1:
                            
                            self.talkedToDean +=1
                            self.printText('1stDean.txt')
                            self.purchasedItems.append(self.heartPowerup)
                            self.notYetForSaleItems.remove(self.heartPowerup)
                        elif self.talkedToDean == 1 and self.unlocked >2:
                            self.talkedToDean +=1
                            self.printText('2ndDean.txt')
                            self.unlockedSlots +=1
                            self.equipedItems.append('none')
                        elif self.talkedToDean == 2 and self.unlocked >4:
                            self.talkedToDean +=1
                            self.printText('3rdDean.txt')
                            self.unlockedSlots +=1
                            self.equipedItems.append('none')
                        elif self.talkedToDean == 3 and self.unlocked >4:
                            self.talkedToDean +=1
                            self.printText('4thDean.txt')
                            self.purchasedItems.append(self.deanPowerup)
                            self.notYetForSaleItems.remove(self.deanPowerup)
                        else:
                            if self.talkedToDean == 4:
                                self.printText('Im still trying to remember what that     medal did...')
                            else:
                                self.printText(n.interact)
                    if n.interactType == 'shop':
                        self.shop()
                    if n.interactType == 'bullet':
                        self.bulletshop()
                    if n.interactType == 'save':
                        self.saveMenu()
                    if n.interactType == 'bulletUpgrade':
                        self.bulletUpgrade()
                    if n.interactType == 'powerupUpgrade':
                        self.powerupUpgrade()
                    if n.interactType == 'fireBoots':
                        asdf = True
                        for i in self.notYetForSaleItems:
                            if i == self.firePowerup:
                                asdf = False
                                self.printText('DeanFire.txt')
                                self.notYetForSaleItems.remove(self.firePowerup)
                                self.purchasedItems.append(self.firePowerup)
                        if asdf:
                            self.printText('Sorry, I have nothing else to give you now. Good luck')
                    if n.interactType == 'snowBullet':
                        asdf = True
                        for i in self.notYetForSaleBullets:
                            if i == self.snowBullet:
                                asdf = False
                                self.printText('DeanSnow.txt')
                                self.notYetForSaleBullets.remove(self.snowBullet)
                                self.purchasedBullets.append(self.snowBullet)
                                self.orderedBullets[4] = self.snowBullet
                        if asdf:
                            self.printText('Sorry, I have nothing else to give you now. Good luck')

        for s in self.signPostGroup:
            if py.sprite.collide_rect(s,self.player):
                self.toShowSpeech = 1
                if pressed[enterDoorKey] and self.player.vel.y == 0:
                    self.printText(s.text)

        #check for players death
        if self.healthLeft <= 0:
            self.running = False
            self.playerDead = True

        #prevent spam bullets
        for i in range(len(self.bulletWait)):
            if self.bulletWait[i] > 0:
                self.bulletWait[i] -=1
                if self.bulletWait[i]<0:
                    self.bulletWait[i]= 0
                    
        #flames from flame boots
        for i in self.fireGroup:
            for e in self.enemies:
                if py.sprite.collide_rect(i,e) and not e.fireDamage:
                    e.fireDamage = True
                    if self.powerupLevel[7] == 0:
                        e.health -=2
                    if self.powerupLevel[7] == 1:
                        e.health -=3
                    if self.powerupLevel[7] == 2:
                        e.health -=4
                    if self.powerupLevel[7] == 3:
                        e.health -=5
                    if self.powerupLevel[7] == 4:
                        e.health -=6
                    if self.powerupLevel[7] == 5:
                        e.health -=8
                    if self.powerupLevel[7] == 6 or self.powerupLevel[7] == 7:
                        e.health -=10
        #c4 blasts, from antimatter to heal player or hit enemies for damage   
        for c in self.C4Group:
            if py.sprite.collide_rect(self.player,c):
                if c.user !=self.player:
                    if self.bulletLevel[4] == 10:
                        if self.healthLeft <= (self.hearts-1)*4+1:
                            self.healthLeft +=3
                        else: self.healthLeft = self.hearts*4
                        c.kill()
            for e in self.enemies:
                if py.sprite.collide_rect(c,e) and not e.damaged:
                    e.damaged = True
                    e.health -=c.damage
                    e.knockback = True
                    if e.rect.center[0] > c.rect.center[0]:
                        e.vel.x= 7
                    else:
                        e.vel.x = -7
                    e.vel.y = -5
        #check equiped items for c4 blasts or fire boots
        for i in self.equipedItems:
            if i == self.firePowerup:
                self.createFire -=1
                if self.createFire <=0:
                    for i2 in self.floors:
                        if (i2.rect.top == self.player.rect.bottom and
                            self.player.rect.left > i2.rect.left and self.player.rect.right <i2.rect.right):
                            self.createFire = 30
                            f = FireStuff(self,self.player.rect.bottomleft)
                            self.fireGroup.add(f)
                            self.all_sprites.add(f)
            #different blast strengths depending on c4 level
            if i == self.C4Powerup:
                if self.powerupLevel[8]==0 and self.C4Hits >=5:
                    for i in range(4):
                        c = C4blast(self,i,10,'C4blast',self.player)
                        self.all_sprites.add(c)
                        self.C4Group.add(c)
                    self.C4Hits = 0
                if self.powerupLevel[8]==1 and self.C4Hits >=5:
                    for i in range(4):
                        c = C4blast(self,i,12,'C4blast',self.player)
                        self.all_sprites.add(c)
                        self.C4Group.add(c)
                    self.C4Hits = 0
                if self.powerupLevel[8]==2 and self.C4Hits >=5:
                    for i in range(4):
                        c = C4blast(self,i,15,'C4blast',self.player)
                        self.all_sprites.add(c)
                        self.C4Group.add(c)
                    self.C4Hits = 0
                if self.powerupLevel[8]==3 and self.C4Hits >=5:
                    for i in range(4):
                        c = C4blast(self,i,19,'C4blast',self.player)
                        self.all_sprites.add(c)
                        self.C4Group.add(c)
                    self.C4Hits = 0
                if self.powerupLevel[8]==4 and self.C4Hits >=4:
                    for i in range(4):
                        c = C4blast(self,i,24,'C4blast',self.player)
                        self.all_sprites.add(c)
                        self.C4Group.add(c)
                    self.C4Hits = 0
                if self.powerupLevel[8]==5 and self.C4Hits >=4:
                    for i in range(4):
                        c = C4blast(self,i,30,'C4blast',self.player)
                        self.all_sprites.add(c)
                        self.C4Group.add(c)
                    self.C4Hits = 0
                if self.powerupLevel[8]==6 and self.C4Hits >=3:
                    for i in range(4):
                        c = C4blast(self,i,36,'C4blast',self.player)
                        self.all_sprites.add(c)
                        self.C4Group.add(c)
                    self.C4Hits = 0
                if self.powerupLevel[8]==7 and self.C4Hits >=2:
                    for i in range(4):
                        c = C4blast(self,i,36,'C4blast',self.player)
                        self.all_sprites.add(c)
                        self.C4Group.add(c)
                    self.C4Hits = 0
                
                
            #heal player with the valentines powerup
            if i == self.valentinesPowerup:
                if self.powerupLevel[4] == 10:
                    self.valentinesTimer -=1
                if self.valentinesTimer == 0:
                    self.valentinesTimer = 900
                    if self.healthLeft<self.hearts*4:
                        self.healthLeft +=1
        #checking for players location to the doors, and if the door should open/
        #close or send the player through the doors to new room
        for d in self.doors:
            if abs(self.player.rect.center[0]-d.rect.center[0])<42 and(self.player.rect.top+3>d.rect.top and self.player.rect.bottom-5<d.rect.bottom):
                if d.opened:
                    if d.direction[0:4] !='back' and not self.screenFade:
                        self.screenFade = True
                        self.player.gActivated = False
                        self.player.vel.y = 0
                        self.nextOpenTo = d.openTo
                        self.openDirection = d.direction
                        
                    elif not self.screenFade:
                        if pressed[enterDoorKey]:
                            self.screenFade = True
                            self.player.gActivated = False
                            self.player.vel.y = 0
                            self.nextOpenTo = d.openTo
                            self.openDirection = d.direction
                            if self.player.gunDrawn:
                                self.speedPercent+=.2
                                self.player.gunDrawn = False
                else:
                    if not d.opened:
                        if self.keys-d.openKeys>=0:
                            d.inprocessOpen = True
            if d.inprocessOpen:
                d.doorOpening()

        #check if player collects a key
        for k in self.keysGroup:
            if k.showing:
                if py.sprite.collide_rect(k,self.player):
                    self.keys +=1
                    k.showing = False
                    self.keysDone.add(k)
                    self.all_sprites.remove(k)
                    self.keysGroup.remove(k)
                    self.keySpawning[self.openTo][k.number] = 0
                    for d in self.doors:
                        if d.direction[0:4] =='back':
                            if not d.opened:
                                if self.keys>=d.openKeys:
                                    d.image = d.pictures[0]
                    
        #check for player collecting a coin
        for c in self.allCoins:
            if py.sprite.collide_rect(c,self.player) and not c.sparkle:
                self.levelGold += c.value
                c.sparkle = True
                c.picture = 0
                c.ttC = 0
                self.coinSpawning[self.openTo][c.number] = 0
                self.coinSound.play()
                
        #check for player collecting money bags
        for m in self.moneyBags:
            if py.sprite.collide_rect(m,self.player):
                self.levelGold +=m.value
                self.moneybagSpawning[m.number] = 0
                self.currentStolen +=1
                self.speedPercent -= .03
                if self.mode == 'easy':
                    self.speedPercent +=.015
                self.speedPercent = round(self.speedPercent,4)
                m.kill()

        #check for player collecting Dropped Hearts
        for d in self.DroppedHeartGroup:
            if py.sprite.collide_rect(d,self.player):
                if self.healthLeft<(self.hearts-1)*4:
                    self.healthLeft +=4
                    for i in self.equipedItems:
                        if i == self.heartPowerup and self.powerupLevel[0]==4:
                            if self.healthLeft<self.hearts*4-2:
                                self.healthLeft +=2
                            else: self.healthLeft = self.hearts*4
                else:self.healthLeft = self.hearts*4
                self.heartSound.play()
                d.kill()

        #check for player collecting dropped ammo
        for a in self.DroppedAmmoGroup:
            if py.sprite.collide_rect(a,self.player):
                self.ammo +=20
                a.kill()

        #check if the player has beaten the level
        for e in self.EndLevelObj:
            if py.sprite.collide_rect(e,self.player):
                self.currentStolen = 0
                self.newGame = False
                if e.textFile !='none':
                    self.printText(e.textFile)
                self.totalGold += self.levelGold
                self.timerStart = False
                self.speedPercent = 1
                for item in self.equipedItems:
                    if item == self.steelPowerup:
                        if self.powerupLevel[6] == 0:
                            self.speedPercent -=.4
                        if self.powerupLevel[6] == 1:
                            self.speedPercent -=.35
                        if self.powerupLevel[6] == 2:
                            self.speedPercent -=.3
                        if self.powerupLevel[6] == 3:
                            self.speedPercent -=.2
                        if self.powerupLevel[6] == 4 or self.powerupLevel[6] == 5:
                            self.speedPercent -=.1
                if self.unlocked == self.area:
                    self.unlocked +=1
                    if self.area == 2 or self.area == 4:
                        self.hearts +=1
                self.healthLeft = self.hearts * 4
                self.ammo=0
                self.bulletsClip=0
                self.screenFade = True
                self.player.gActivated = False
                self.player.vel.y = 0
                self.nextOpenTo = 0
                self.openDirection = 'left'
                if self.boosterValue <18:
                    self.boosterValue +=2
                if self.levelGold > self.bagsStolen[self.area-1]:
                    self.bagsStolen[self.area-1] = self.levelGold
                self.area = 0
                self.levelGold = 0
                py.mixer.music.load(path.join(music_folder,'mmmusic.mp3'))
                py.mixer.music.play()
                e.kill()
            
        #testing for out of bullets for reloading
        if (((self.equipedBullet[0] == self.dualBullet and self.bulletsClip <=1 and self.ammo+self.bulletsClip >=2) or
            (self.equipedBullet[0] == self.normalBullet and self.bulletsClip <=0 and self.ammo+self.bulletsClip >=1) or
            (self.equipedBullet[0] == self.snowBullet and self.bulletsClip <=2 and self.ammo+self.bulletsClip >=3) or
            (self.equipedBullet[0] == self.sniperBullet and self.bulletsClip <=5 and self.ammo+self.bulletsClip >=6) or
            (self.equipedBullet[0] == self.antiBullet and self.bulletsClip <=11 and self.ammo+self.bulletsClip >=12) or
            (self.equipedBullet[0] == self.batteryBullet and self.bulletsClip <=3 and self.ammo+self.bulletsClip >=4))
            and not self.reload):
            self.reload=True
            if self.ammo>=15-self.bulletsClip:
                self.neededB= 15-self.bulletsClip
            else: self.neededB=self.ammo
            self.reloadTime = self.neededB*10
            
        #reloading loop
        if self.reload:
            self.reloadTime-=1
            if self.reloadTime==0:
                if self.ammo>self.neededB:
                    self.bulletsClip=15
                    self.ammo-=self.neededB
                else:
                    self.bulletsClip+=self.ammo
                    self.ammo=0
                self.reload=False

        #for when player gets damaged
        if self.damaged:
            self.damagedTime +=1
            self.playerAlpha+= self.playerAlphaDirection*17
            if self.playerAlpha<=0:
                self.playerAlpha = 0
                self.playerAlphaDirection = 1
            if self.playerAlpha >=255:
                self.playerAlpha = 255
                self.playerAlphaDirection = -1
            self.player.image.set_alpha(self.playerAlpha)
            if self.damagedTime == self.damagedTimer:
                self.damaged = False
                self.damagedTime = 0
                self.playerAlpha = 255
                self.playerAlphaDirection = -1
                for i in self.player.allPlayerImages:
                    for i2 in i:
                        i2.set_alpha(255)
        
        #deals with player knockback
        if self.player.knockback:
            self.player.knockbackTimer +=1
            if self.player.knockbackTimer == self.player.knockbackDone:
                self.player.knockbackTimer = 0
                self.player.knockback = False
                self.player.vel.x = 0
            self.player.vel.y+=.2

        #timer for players wall jump
        if self.player.wallJump:
            if self.player.wallJumpTimer > 0:
                self.player.wallJumpTimer -=1
            else:
                self.player.wallJump = False

         
        #end of game timer, sends hail of bullets at player        
        if self.timerStart and(self.openTo!=self.bossRoom or self.bossDown==self.allBosses):
            if time.time()-self.timeStart>self.maxTime and self.endGameBullets == 0:
                newb=Bullet(self.player,-1,self,2,self.normalBullet)
                self.bullets.add(newb)
                self.all_sprites.add(newb)
                newb = Bullet(self.player,1,self,1,self.normalBullet)
                self.bullets.add(newb)
                self.all_sprites.add(newb)
            self.endGameBullets+=1
            if self.endGameBullets >= 10:
                self.endGameBullets = 0 

        #text boxes displaying text
        for t in self.textBoxes:
            if py.sprite.collide_rect(t,self.player) and t.neededKeys == self.keys:
                if t.text == 'B1boss.txt' and self.unlocked == 1:
                    #cut scene in bank 1
                    py.mixer.music.pause()
                    self.player.vel.x = 0
                    self.player.direction = 1
                    if self.player.gunDrawn:
                        self.player.gunDrawn = False
                        self.speedPercent +=.2
                    self.player.animate()
                    self.player.canMove = False
                    firstLoop = True
                    for i in self.bullets:
                        i.kill()
                    while firstLoop:
                        #make sure player is on floor
                        self.draw()
                        for i in self.floors:
                            if (self.player.rect.bottom == i.rect.top and
                            (self.player.rect.left < i.rect.right or self.player.rect.right > i.rect.left)) and not self.player.hitting:
                                firstLoop = False
                        clock.tick(FPS)
                        for event in py.event.get():
                            if event.type == py.QUIT:
                                py.quit()
                                py.mixer.quit()
                                exit()
                        self.player.update()
                    for i in range(95):
                        #shift the screen over to the right
                        self.draw()
                        clock.tick(FPS)
                        for event in py.event.get():
                            if event.type == py.QUIT:
                                py.quit()
                                py.mixer.quit()
                                exit()
                        for i in self.all_sprites:
                            i.rect.left-=5
                        self.mapTL+=(-5,0)
                    e = Enemy(self,101,(WIDTH,self.player.rect.centery-10),'standard',0,-1,'none')
                    self.all_sprites.add(e)
                    self.bossenemies.add(e)
                    e.speed = 0
                    for i in range(15):
                        e.update()
                    e.rect.centerx = WIDTH
                    e.vel.x = -3
                    e.direction = -1
                    #captain walking in
                    for i in range(130):
                        self.draw()
                        e.rect.x += e.vel.x
                        e.animate()
                        clock.tick(FPS)
                        for event in py.event.get():
                            if event.type == py.QUIT:
                                py.quit()
                                py.mixer.quit()
                                exit()
                    e.vel.x = 0
                    e.animate()
                    self.printText(t.text)
                    t.kill()
                    e.vel.x = 3
                    #captain walking out
                    for i in range(130):
                        self.draw()
                        e.rect.x += e.vel.x
                        e.animate()
                        clock.tick(FPS)
                        for event in py.event.get():
                            if event.type == py.QUIT:
                                py.quit()
                                py.mixer.quit()
                                exit()
                    e.kill()
                    #shift screen back to normal
                    for i in range(95):
                        clock.tick(FPS)
                        self.draw()
                        for event in py.event.get():
                            if event.type == py.QUIT:
                                py.quit()
                                py.mixer.quit()
                                exit()
                        for i in self.all_sprites:
                            i.rect.left+=5
                        self.mapTL+=(5,0)
                    py.mixer.music.unpause()
                if t.text == 'B1start.txt' and self.newGame:
                    py.mixer.music.pause()
                    self.printText(t.text)
                    t.kill()
                    py.mixer.music.unpause()
                if t.text != 'B1start.txt' and t.text !='B1boss.txt':
                    self.printText(t.text)
                    t.kill()

        #sending player to level menu
        for l in self.levelMenuGroup:
            if self.player.rect.left<l.rect.right:
                self.levelMenu = True
                self.running = False
                break
        #increase the skill timer
        if self.skillNeeded <6000 and not self.skillActive:
            if self.equipedBullet[0] == self.dualBullet and self.bulletLevel[1]>=5:
                self.dualBulletSkillTimer-=1
                
            if self.dualBulletSkillTimer == 0:
                self.skillNeeded +=1
                self.dualBulletSkillTimer = 5
            self.skillNeeded +=1
            
            for i in self.equipedItems:
                if i == self.speedPowerup and self.powerupLevel[1]==4 and self.healthLeft <= self.hearts*1.4:
                    self.skillNeeded +=2
                elif i == self.speedPowerup and self.powerupLevel[1]==4:
                    self.skillNeeded +=1
                    
            if self.mode == 'easy':
                self.skillNeeded +=3
                
        #when the skill is active
        if self.skillActive:
            self.skillNeeded -=25
            self.skillTimer -=1
            if self.skillNeeded <=0:
                self.skillNeeded = 0
                self.skillActive = False
                
        if self.skillNeeded >6000:
            self.skillNeeded = 6000
            
    def events(self):
        #events within game loop
        normalJump = False
        wallJump = False
        for event in py.event.get():
            #quiting events
            if event.type == py.QUIT:
                py.quit()
                py.mixer.quit()
                sys.exit()
            if event.type == py.KEYDOWN and event.key == py.K_ESCAPE:
                if self.timerStart:
                    pastTime = time.time()
                    minusTime = pastTime - self.timeStart
                    self.maxTime -= minusTime
                self.paused()
            #everything that can happen when the player jumps
            if event.type ==py.KEYDOWN and event.key == jumpKey:
                for i in self.floors:
                    if (self.player.rect.bottom == i.rect.top and
                        (self.player.rect.left < i.rect.right or self.player.rect.right > i.rect.left)):
                        self.player.vel.y = -JUMP
                        for item in self.equipedItems:
                            if item == self.steelPowerup:
                                self.player.vel.y +=3
                        self.player.onGround = False
                        normalJump = True
                        self.jumpSound.play()
                        break
                    #wallJump
                    pressedKey = py.key.get_pressed()
                    if ((self.player.rect.left == i.rect.right and pressedKey[moveLeftKey]) or
                        (self.player.rect.right == i.rect.left and pressedKey[moveRightKey]) and
                        (self.player.rect.top<i.rect.bottom and self.player.rect.bottom>i.rect.top)):
                        wallJump = True
                for i in self.spikes:
                    if self.player.rect.bottom == i.rect.top:
                        self.player.vel.y = -JUMP
                        self.player.onGround = False
                        for item in self.equipedItems:
                            if item == self.steelPowerup:
                                self.player.vel.y +=3
                        normalJump = True
                        self.jumpSound.play()
                        break
                    
                    #wallJump
                    pressedKey = py.key.get_pressed()
                    if ((self.player.rect.left == i.rect.right and pressedKey[moveLeftKey]) or
                        (self.player.rect.right == i.rect.left and pressedKey[moveRightKey])and
                        (self.player.rect.top<i.rect.bottom and self.player.rect.bottom>i.rect.top)):
                        wallJump = True
                        
                if self.doubleJumpAble and not normalJump and not wallJump and self.mode == 'easy':
                    self.doubleJumpAble = False
                    self.player.vel.y = -JUMP+2.5
                    for item in self.equipedItems:
                        if item == self.steelPowerup:
                            self.player.vel.y +=3
                    self.jumpSound.play()
                    
                #jump stuff
            if event.type == py.KEYUP and event.key == jumpKey:
                if self.player.vel.y <-6:
                    self.player.vel.y = -6
            #drawing gun
            if event.type == py.KEYDOWN and event.key == drawGunKey and not self.reload:
                if self.player.gunDrawn:
                    self.speedPercent +=.2
                    self.player.gunDrawn = False
                else:
                    self.speedPercent -=.2
                    self.player.gunDrawn = True
            #shooting bullet
            if event.type == py.KEYDOWN and event.key == shootKey:
                if (self.player.gunDrawn and
                     ((self.bulletsClip>0 and self.equipedBullet[0] == self.normalBullet) or
                      (self.bulletsClip>1 and self.equipedBullet[0] == self.dualBullet) or
                      (self.bulletsClip>2 and self.equipedBullet[0] == self.snowBullet) or
                      (self.bulletsClip>5 and self.equipedBullet[0] == self.sniperBullet) or
                      (self.bulletsClip>11 and self.equipedBullet[0] == self.antiBullet) or
                      (self.bulletsClip>3 and self.equipedBullet[0] == self.batteryBullet))):
                    
                    if (((self.bulletWait[0] == 0 and self.equipedBullet[0] == self.normalBullet) or
                         (self.bulletWait[1] == 0 and self.equipedBullet[0] == self.dualBullet) or
                         (self.bulletWait[2] == 0 and self.equipedBullet[0] == self.snowBullet) or
                         (self.bulletWait[3] == 0 and self.equipedBullet[0] == self.sniperBullet) or
                         (self.bulletWait[4] == 0 and self.equipedBullet[0] == self.antiBullet))
                        and not self.reload):
                        for item in self.equipedItems:
                                #chance to not consume bullet
                                if item == self.shootingPowerup:
                                    nobullet = random.randint(1,100)
                                    chance = 0
                                    if self.powerupLevel[2] == 0:
                                        chance = 5
                                    if self.powerupLevel[2] == 1:
                                        chance = 7
                                    if self.powerupLevel[2] == 2:
                                        chance = 10
                                    if self.powerupLevel[2] == 3:
                                        chance = 13
                                    if self.powerupLevel[2] == 4:
                                        chance = 17
                                    if self.powerupLevel[2] == 5:
                                        chance = 21
                                    if self.powerupLevel[2] == 6:
                                        chance = 27
                                    if nobullet <=chance:
                                        self.bulletsClip +=1
                                        if self.equipedBullet[0] == self.dualBullet:
                                            self.bulletsClip+=1
                                        if self.equipedBullet[0] == self.snowBullet:
                                            self.bulletsClip+=2
                                        if self.equipedBullet[0] == self.sniperBullet:
                                            self.bulletsClip+=5
                                        if self.equipedBullet[0] == self.antiBullet:
                                            self.bulletsClip+=11
                            
                        if self.player.vel.x >5 or self.player.direction == 1:
                            newb=Bullet(self.player,1,self,0,self.equipedBullet[0])
                        else: newb=Bullet(self.player,-1,self,0,self.equipedBullet[0])
                        self.bullets.add(newb)
                        self.all_sprites.add(newb)
                        self.bulletsClip-=1
                        #increasing bullet wait for the bullet that was shot
                        if self.equipedBullet[0] == self.normalBullet:
                            self.bulletWait[0] = self.bulletTime[0]
                        if self.equipedBullet[0] == self.dualBullet:
                            self.bulletWait[1] = self.bulletTime[1]
                            self.bulletsClip-=1
                            self.secondBullet = 10
                        if self.equipedBullet[0] == self.snowBullet:
                            self.bulletWait[2] = self.bulletTime[2]
                            self.bulletsClip-=2
                        if self.equipedBullet[0] == self.sniperBullet:
                            self.bulletWait[3] = self.bulletTime[3]
                            self.bulletsClip-=5
                        if self.equipedBullet[0] == self.antiBullet:
                            self.bulletWait[4] = self.bulletTime[4]
                            self.bulletsClip-=11

                    elif (self.bulletWait[5] == 0 and self.equipedBullet[0] == self.batteryBullet):
                        self.batteryCharging = True
                #if not shooting, make it so the player will hit
                elif not self.player.hitting and not self.reload:
                    self.player.hitting = True
                    if self.player.onGround:
                        self.player.vel.x = 0
                    self.player.picture = 0
                    self.player.ttC = 0
                    h = Hitting(self,self.player)
                    self.hittingGroup.add(h)
            #shoot bullet if it was of the battery type
            if event.type == py.KEYUP and event.key == shootKey and self.batteryCharging:
                if self.player.vel.x >5 or self.player.direction == 1:
                    newb=Bullet(self.player,1,self,0,self.equipedBullet[0])
                else: newb=Bullet(self.player,-1,self,0,self.equipedBullet[0])
                self.bullets.add(newb)
                self.all_sprites.add(newb)
                self.batteryCharging = False
                self.batteryTimer = 0
                self.bulletsClip-=4
                for item in self.equipedItems:
                    if item == self.shootingPowerup:
                        nobullet = random.randint(1,100)
                        if nobullet <=30:
                            self.bulletsClip +=4
            #reloading
            if event.type == py.KEYDOWN and event.key == reloadKey and not self.reload and self.player.gunDrawn and not self.batteryCharging:
                if self.ammo>0 and self.bulletsClip<15:
                    self.reload=True
                    if self.ammo+self.bulletsClip>=15:
                        self.neededB=15-self.bulletsClip
                        self.reloadTime = self.neededB*10
                    else:
                        self.reloadTime = self.ammo*10
                        self.neededB=self.ammo
            if event.type == py.KEYDOWN and event.key == skillKey and not self.skillActive and self.skillNeeded>20:
                if self.skillNeeded == 6000:
                    if self.healthLeft <self.hearts*4-4:
                        self.healthLeft +=4
                    else: self.healthLeft = self.hearts*4
                self.skillActive = True

            if event.type == py.KEYDOWN:
                if len(self.purchasedBullets)>0:
                    if event.key == py.K_PERIOD:
                        foundOrdered = False
                        nextBullet = 0
                        for i in self.orderedBullets:
                            if foundOrdered:
                                if i != 0:
                                    nextBullet = i
                                    break
                            if i == self.equipedBullet[0]:
                                foundOrdered = True
                        
                        if nextBullet == 0:
                            for i in self.orderedBullets:
                                if i != 0:
                                    nextBullet = i
                                    break
                        

                    if event.key == py.K_COMMA:
                        foundOrdered = False
                        nextBullet = 0
                        
                        for i in range(len(self.orderedBullets)-1,-1,-1):
                            if foundOrdered:
                                if self.orderedBullets[i] != 0:
                                    nextBullet = self.orderedBullets[i]
                                    break
                            if self.orderedBullets[i] == self.equipedBullet[0]:
                                foundOrdered = True

                        if nextBullet == 0:
                            for i in range(len(self.orderedBullets)-1,-1,-1):
                                if self.orderedBullets[i] != 0:
                                    nextBullet = self.orderedBullets[i]
                                    break

                        
                    if event.key in [py.K_PERIOD,py.K_COMMA]:
                        self.newBulletTimer = 40
                        self.purchasedBullets.remove(nextBullet)
                        self.purchasedBullets.append(self.equipedBullet[0])
                        self.equipedBullet[0] = nextBullet
                        
        #only actually perform wallJump if enter this loop, prevents walljumps from standing on floor
        if wallJump and (self.player.vel.y != -JUMP or self.player.vel.y != -JUMP+5) and not normalJump:
            self.player.vel.y = -JUMP-2
            for item in self.equipedItems:
                if item == self.steelPowerup:
                    self.player.vel.y +=3
            if self.healthLeft <= self.hearts*1.4:
                for item in self.equipedItems:
                    if item == self.speedPowerup:
                        if self.powerupLevel[1] == 0:
                            self.player.speed = self.player.speed*1.3
                        if self.powerupLevel[1] == 1:
                            self.player.speed = self.player.speed*1.5
                        if self.powerupLevel[1] == 2:
                            self.player.speed = self.player.speed*1.7
                        if self.powerupLevel[1] == 3 or self.powerupLevel[1] == 4:
                            self.player.speed = self.player.speed*2
            if self.player.direction == 1:
                self.player.vel.x= -self.player.speed*1.3
                self.player.image = self.player.onWallL[0]
            else:
                self.player.image = self.player.onWallR[0]
                self.player.vel.x = self.player.speed*1.3
            self.player.image.set_colorkey((237,28,36))
            self.player.wallJump = True
            self.player.wallJumpTimer = 30
            self.player.wallJumpDirec = self.player.direction
            if self.healthLeft <= self.hearts*1.4:
                for item in self.equipedItems:
                    if item == self.speedPowerup:
                        if self.powerupLevel[1] == 0:
                            self.player.speed = self.player.speed/1.3
                        if self.powerupLevel[1] == 1:
                            self.player.speed = self.player.speed/1.5
                        if self.powerupLevel[1] == 2:
                            self.player.speed = self.player.speed/1.7
                        if self.powerupLevel[1] == 3 or self.powerupLevel[1] == 4:
                            self.player.speed = self.player.speed/2
        #shoot second bullet if dual bullet equiped
        if self.secondBullet != 0:
            self.secondBullet -=1
            if self.secondBullet == 0:
                if self.player.vel.x >5 or self.player.direction == 1:
                    newb=Bullet(self.player,1,self,0,self.equipedBullet[0])
                else: newb=Bullet(self.player,-1,self,0,self.equipedBullet[0])
                self.bullets.add(newb)
                self.all_sprites.add(newb)

  
    def draw(self):
        #draw everything to screen
        if not self.screenFade or self.fadeTimer >36:
            screen.fill(black)
            screen.blit(self.map[self.area][self.openTo][1],self.mapTL)
            self.all_sprites.remove(self.player)
            #deals with layering for the drawing, ie player must be on top etc
            for i in self.otherImg:
                self.all_sprites.remove(i)
            for i in self.doors:
                self.all_sprites.remove(i)
                if i.direction == 'right':
                    curImg = i.image.get_rect()
                    screen.blit(i.image,(i.rect.x-curImg.width+15,i.rect.y))
                else:
                    screen.blit(i.image,(i.rect.x,i.rect.y))
                
            self.all_sprites.draw(screen)
            for e in self.enemies:
                if e.newAlert:
                    e.newAlertTimer +=1
                    if e.newAlertTimer==35:
                        e.newAlertTimer = 0
                        e.newAlert = False
                    screen.blit(self.exclamationMark[0],(e.rect.centerx-24,e.rect.y-64))
                if e.keyReq>0 and not e.newAlert:
                    screen.blit(self.holdingKey,(e.rect.x+32,e.rect.y-32))
            for i in self.otherImg:
                self.all_sprites.add(i)
            self.otherImg.draw(screen)
            for i in self.doors:
                self.all_sprites.add(i)
                
            self.all_sprites.add(self.player)
            #display the player to the screen
            if self.player.direction == 1:
                if not self.player.wallJump:
                    screen.blit(self.player.image,(self.player.rect.x-8,self.player.rect.y-20))
                else:screen.blit(self.player.image,(self.player.rect.x,self.player.rect.y-20))
            else:
                if not self.player.wallJump:
                    screen.blit(self.player.image,(self.player.rect.x-24,self.player.rect.y-20))
                else: screen.blit(self.player.image,(self.player.rect.x,self.player.rect.y-20))
            if self.toShowSpeech == 1:
                screen.blit(self.speechBubble,(self.player.rect.centerx-16,self.player.rect.y-55))
            self.otherImg.draw(screen)
            self.particleGroup.draw(screen)
            
            py.draw.rect(screen,black,(0,0,WIDTH,75))
            #display ammo
            displaytext(("Ammo: "+str(self.ammo)+' / '+str(self.bulletsClip)),WIDTH-175,15,white,font24)
            #display hearts
            for i in range(self.hearts+1):
                if i >0:
                    if self.healthLeft>=i*4:
                        if i <=12:
                            screen.blit(self.heartsImg[4],(10+i*32,5))
                    elif self.healthLeft<=((i-1)*4):
                        if i <=12:
                            screen.blit(self.heartsImg[0],(10+i*32,5))
                    else:
                        if i <=12:
                            screen.blit(self.heartsImg[self.healthLeft%4],(10+i*32,5))
                        
            py.draw.rect(screen,(70,70,70),(42,44,206,27),5)
            skillbar = (self.skillNeeded/6000)*200
            if self.skillNeeded < 6000:
                py.draw.rect(screen,blue,(45,47,skillbar,21))
            else:
                self.skillBarColorChange += self.skillBarColorDirec
                if self.skillBarColorChange == 10:
                    self.skillBarColorDirec = 1
                if self.skillBarColorChange == 22:
                    self.skillBarColorDirec = -1
                if self.skillBarColorChange <14:
                    self.skillBarColor = (255,255,255)
                elif self.skillBarColorChange <18:
                    self.skillBarColor = (150,150,255)
                elif self.skillBarColorChange <22:
                    self.skillBarColor = (0,0,255)
                py.draw.rect(screen,self.skillBarColor,(45,47,skillbar,21))
                
            #display either level or total gold to scren
            screen.blit(self.mbag,(WIDTH-263,27))
            displaytext(':',WIDTH-200,50,white,font24)
            if self.area != 0:
                displaytext(str(self.levelGold),WIDTH-90,50,white,font24)
            else: displaytext(str(self.totalGold),WIDTH-90,50,white,font24)

            if self.newBulletTimer>0:
                self.newBulletTimer -=1
                for i in range(len(self.orderedBullets)):
                    if self.orderedBullets[i] == self.equipedBullet[0]:
                        screen.blit(self.selectImages[i],(self.player.rect.x+14,self.player.rect.y-50))
            
            #draw reload bar
            if self.reload:
                py.draw.rect(screen,black,(self.player.rect.x,self.player.rect.y-35,self.player.rect.width,15))
                py.draw.rect(screen,green,(self.player.rect.x+1,self.player.rect.y-34,(self.player.rect.width-2)*((self.reloadTime/FPS*4)/self.neededB),13))
            #draw bullet wait bar above the player
            if self.equipedBullet[0] == self.normalBullet:
                displayWait = self.bulletWait[0]
                displayMax = self.bulletTime[0]
            if self.equipedBullet[0] == self.dualBullet:
                displayWait = self.bulletWait[1]
                displayMax = self.bulletTime[1]
            if self.equipedBullet[0] == self.snowBullet:
                displayWait = self.bulletWait[2]
                displayMax = self.bulletTime[2]
            if self.equipedBullet[0] == self.sniperBullet:
                displayWait = self.bulletWait[3]
                displayMax = self.bulletTime[3]
            if self.equipedBullet[0] == self.antiBullet:
                displayWait = self.bulletWait[4]
                displayMax = self.bulletTime[4]
            if self.equipedBullet[0] == self.batteryBullet:
                displayWait = self.bulletWait[5]
                displayMax = self.bulletTime[5]
            if displayWait >0:
                py.draw.rect(screen,black,(self.player.rect.centerx-10,self.player.rect.y-19,20,6))
                displayLen = displayWait/displayMax
                py.draw.rect(screen,green,(self.player.rect.centerx-9,self.player.rect.y-18,(displayLen*18),4))
                
            if self.openTo!=self.bossRoom or self.bossDown>=self.allBosses:
                #displaying the timer to the screen
                if self.timerStart:
                    pastTime = time.time()
                    minusTime = pastTime - self.timeStart
                    leftTime = self.maxTime - minusTime
                    leftTimeList = [leftTime%60,leftTime//60]
                    leftTimeList[0] = int(leftTimeList[0])
                    if leftTimeList[0]<10:
                        leftTimeList[0] = '0'+str(int(leftTimeList[0]))
                    leftTimeList[1] = int(leftTimeList[1])
                    if leftTimeList[1] < 0:
                        displaytext('0:00',WIDTH/2,25,red,font36)
                    elif leftTimeList[1]>=2:
                        displaytext(str(leftTimeList[1])+':'+str(leftTimeList[0]),WIDTH/2,25,white,font24)
                    elif leftTimeList[1]>=1:
                        displaytext(str(leftTimeList[1])+':'+str(leftTimeList[0]),WIDTH/2,25,white,font30)
                    else: displaytext(str(leftTimeList[1])+':'+str(leftTimeList[0]),WIDTH/2,25,red,font36)
                else: displaytext('0:00',WIDTH/2,25,white,font24)
            else:
                #if you have to draw the boss bar
                mainboss = False
                for i in self.enemies:
                    if i.type == 100 or i.type == 101:
                        mainboss = True
                        totalHealth = i.health
                if not mainboss:
                    totalHealth = 0
                    for i in self.enemies:
                        totalHealth += i.health
                py.draw.rect(screen,grey,(WIDTH/2-180,20,360,30))
                length = (totalHealth/self.bossMaxhealth)*352
                py.draw.rect(screen,purple,(WIDTH/2-176,24,length,22))
        #deal with screen fade
        if self.screenFade:
            self.fadeTimer +=1
            if self.fadeTimer<=25:
                self.screenAlpha+=10
            if self.fadeTimer == 30:
                if self.nextOpenTo != -10:
                    for i in self.all_sprites:
                        i.kill()
                    for i in self.particleGroup:
                        i.kill()
                    self.camera = vec(WIDTH/2,HEIGHT/2)
                    self.openTo = self.nextOpenTo
                    if self.player.gunDrawn:
                        self.speedPercent +=.2
                        self.player.gunDrawn = False
                    self.new()
                    if self.beatBoss:
                        #cut scene if you just finished killing the final boss
                        self.beatBoss = False
                        leave = False
                        scroll = 0
                        while not leave:
                            scroll +=2
                            if scroll == 500:
                                for i in range(180):
                                    clock.tick(FPS)
                                    for event in py.event.get():
                                        if event.type == py.QUIT:
                                            py.quit()
                                            py.mixer.quit()
                                            exit()
                                        if event.type == py.KEYDOWN and event.key == py.K_RETURN:
                                            leave = True
                            if scroll ==  1234+500:
                                for i in range(300):
                                    clock.tick(FPS)
                                    for event in py.event.get():
                                        if event.type == py.QUIT:
                                            py.quit()
                                            py.mixer.quit()
                                            exit()
                                        if event.type == py.KEYDOWN and event.key == py.K_RETURN:
                                            leave = True
                                    leave = True
                            screen.fill(black)
                            clock.tick(FPS)
                            for event in py.event.get():
                                if event.type == py.QUIT:
                                    py.quit()
                                    py.mixer.quit()
                                    exit()
                                if event.type == py.KEYDOWN and event.key == py.K_RETURN:
                                    leave = True
                            #all the text that will be displayed for credits
                            displaytext('reign of raiders',WIDTH/2,HEIGHT-scroll,red,font36)
                            displaytext('Creators:',WIDTH/2,HEIGHT-scroll+575,white,font30)
                            displaytext('Main programmer: Ryan Saweczko',WIDTH/2,HEIGHT-scroll+652,white,font24)
                            displaytext('Graphic Designer: Mohamed Ibrahim',WIDTH/2,HEIGHT-scroll+692,white,font24)
                            displaytext('Music By: Etalify (find them on Youtube)',WIDTH/2,HEIGHT-scroll+772,white,font24)
                            displaytext('We hope you enjoyed playing reign of raiders!',WIDTH/2,HEIGHT-scroll + 1224,white,font18)
                            displaytext('Keep playing to try and unlock all bullets and powerups',WIDTH/2,HEIGHT-scroll + 1254,white,font18)


                            py.display.flip()
                        py.mixer.music.load(path.join(music_folder,'mmmusic.mp3'))
                        py.mixer.music.play()
                    ###########################################################################################################3
                self.player.gActivated = True
            if self.fadeTimer >=34:
                self.screenAlpha -=10
            if self.screenAlpha>255:
                self.screenAlpha=255
            if self.fadeTimer == self.fadeDone:
                self.screenAlpha = 0
                self.fadeTimer = 0
                self.screenFade = False
                if self.area == 5 and self.openTo ==self.bossRoom:
                    py.mixer.music.pause()
                    for i in self.enemies:
                        i.vel.x = 0
                        i.direction = -1
                        i.animate()
                        self.bossenemies.add(i)
                    self.draw()
                    self.printText('b5enter.txt')
                    self.bossenemies.empty()
                    py.mixer.music.unpause()
            self.blackness.set_alpha(self.screenAlpha)
            self.blackness.fill(black)
            screen.blit(self.blackness,(0,0))
        py.display.flip()
        
    def paused(self):
        #paused menu
        py.mixer.music.pause()
        index2 = 0
        while True:
            clock.tick(FPS)
            screen.fill(black)
            displaytext("Paused",WIDTH/2,100,white,font30)
            #all buttons that player can select from
            screen.blit(Pbutton1,Prect_1)
            screen.blit(Pbutton2,Prect_2)
            screen.blit(Pbutton3,Prect_3)
            screen.blit(Pbutton4,Prect_4)
            screen.blit(Pbutton5,Prect_5)
            py.draw.rect(screen, white, [PrectsList[index2].x - 30,(Prect_1.centery-3)+(50*index2),6,6],5)
            change,select = events(1)#event loop to find what player presses
            index2+=change
            if index2>4:
                index2=0
            if index2<0:
                index2=4
            if select != 0:
                if index2 == 0:
                    self.timeStart = time.time()
                    py.mixer.music.unpause()
                    break
                if index2 == 1:
                    self.inventoryMenu()
                if index2 == 2:
                    self.bulletMenu()
                if index2 == 3:
                    how_to_play()
                    self.moveLeftKey = moveLeftKey
                    self.moveRightKey = moveRightKey
                if index2 == 4:
                    self.running = False
                    self.goToTitle = True
                    self.wasPaused = True
                    break
            py.display.flip()

    def dead(self):
        self.currentStolen = 0
        self.skillNeeded = 6000
        for i in self.bulletWait:
            i = 0
        index2 = 0
        py.mixer.music.stop()
        #loop for when the player dies
        while True:
            clock.tick(FPS)
            screen.fill(black)
            displaytext("You have Died!",WIDTH/2,150,red,font30)
            displaytext("What would you like to do?",WIDTH/2,210,red,font30)
            #buttons the player can select from
            screen.blit(Dbutton1,Drect_1)
            screen.blit(Dbutton2,Drect_2)
            screen.blit(Dbutton3,Drect_3)
            py.draw.rect(screen, white, [DrectsList[index2].x - 30,(Drect_1.centery-3)+(50*index2),6,6],5)
            change,select = events(1)
            
            index2+=change
            if index2>2:
                index2=0
            if index2<0:
                index2=2
            if select != 0:
                #this all is if the player selects to retry level
                if index2 == 0:
                    self.percentSpeed = 0
                    self.levelGold = 0
                    for i in self.all_sprites:
                        i.kill()
                    for i in self.particleGroup:
                        i.kill()
                    self.playerDead = False
                    self.healthLeft = self.hearts*4
                    self.reload=False
                    self.keys = 0
                    self.damaged = False
                    self.damagedTimer = FPS*2
                    self.damagedTime = 0
                    self.cameraDone = 0
                    self.camera = vec(WIDTH/2,HEIGHT/2)
                    self.openTo = 0
                    self.bossDown = 0
                    self.bulletsClip = 15
                    self.ammo = 105
                    if self.mode == 'easy':
                        self.ammo +=30
                    #controls spawing in of objects that might not always be there
                    self.enemySpawning = [[1],[1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                                          [1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1],
                                          [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                                          [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
                    self.keySpawning = [[0],[1,1,1,1,1],[1,1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1]]
                    self.coinSpawning = [[0],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                                         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                                         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                                         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
                    self.moneybagSpawning = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
                    if self.area == 5:
                        self.maxTime =600
                    else:
                        self.maxTime = 360
                    self.levelMenu = False
                    self.running = True
                    self.timerStart = False
                    self.openDirection = 'right'
                    self.new()
                    break
                if index2 == 1:
                    self.running = False
                    self.levelMenu = True 
                    self.playerDead = False
                    break
                if index2 == 2:
                    self.running = False
                    self.goToTitle = True
                    self.playerDead = False
                    break
            py.display.flip()
        self.run()

    def levelMenuScreen(self):
        self.currentStolen = 0
        self.skillNeeded = 6000
        for i in self.bulletWait:
            i = 0
        py.mixer.music.load(path.join(music_folder,'lsmusic.mp3'))
        py.mixer.music.play()
        map_stops = py.sprite.Group()
        map_sprites = py.sprite.Group()
        levelCams = py.sprite.Group()
        self.levelGold = 0
        index2 = 0
        #display the level selector
        for i in self.all_sprites:
            i.kill()
        for i in self.particleGroup:
            i.kill()
        self.timerStart = False
        self.maxTime = 300
        self.openDirection = 'right'
        map_screen = True
        
        levelMap = TiledMap(path.join(map_folder, "levelSelector.tmx"))
        levelMapIMG = levelMap.make_map()
        levelMapRect = levelMapIMG.get_rect()
        
        info = pygame.Surface((WIDTH,110))
        for tile_object in levelMap.tmxdata.objects:
            if tile_object.name == "Stop":
                stop = MapStop(tile_object.Left,tile_object.Right,tile_object.Up,tile_object.Down,tile_object.x,tile_object.y,tile_object.text)
                map_stops.add(stop)
            if tile_object.name == "mapPlayer":
                map_me = MapPlayer(self,tile_object.x,tile_object.y,map_stops)
                map_sprites.add(map_me)
            if tile_object.name == 'Camera':
                c = CameraBound(tile_object.direction,tile_object.x,tile_object.y,tile_object.width,tile_object.height,-1)
                levelCams.add(c)
                
        camera = vec(WIDTH/2,HEIGHT/2)
        
        while map_screen:
            if not py.mixer.music.get_busy():
                py.mixer.music.load(path.join(music_folder,'lsmusic.mp3'))
                py.mixer.music.play()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if map_me.xspeed == 0 and map_me.yspeed == 0:
                        if event.key == pygame.K_UP and map_me.target.goUp == "true":  # Tiled gives booleans a string value instead of an actual True/False value
                            map_me.yspeed = -8
                        if event.key == pygame.K_DOWN and map_me.target.goDown == "true": # Weird huh?
                            map_me.yspeed = 8
                        if event.key == pygame.K_LEFT and map_me.target.goLeft == "true":
                            map_me.xspeed = -8
                        if event.key == pygame.K_RIGHT and map_me.target.goRight == "true":
                            map_me.xspeed = 8
                #selected a level
                if event.type == pygame.KEYDOWN and (event.key == jumpKey or event.key == py.K_RETURN):
                    self.healthLeft = self.hearts*4
                    self.reload=False
                    self.keys = 0
                    self.damaged = False
                    self.damagedTimer = FPS*2
                    self.damagedTime = 0
                    self.cameraDone = 0
                    self.camera = vec(WIDTH/2,HEIGHT/2)
                    self.enemySpawning = [[1],[1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                                          [1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1],
                                          [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                                          [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
                    self.keySpawning = [[0],[1,1,1,1,1],[1,1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1]]
                    self.coinSpawning = [[0],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                                         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                                         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                                         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
                    self.moneybagSpawning = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
                    self.ammo = self.maxAmmo
                    if self.mode == 'easy':
                        self.ammo +=30
                    self.bulletsClip = 15
                    self.openDirection = 'right'
                    if map_me.xspeed == 0 and map_me.yspeed == 0:
                        if map_me.target.text == "Home Base":
                            self.area = 0
                            self.openTo = 0
                            self.maxTime = 600
                            self.allBosses = 4
                            self.bossRoom = 4
                            self.bossDown = 0
                            self.ammo = 0
                            self.bulletsClip = 0
                            self.playerDead = False
                            self.levelMenu = False
                            py.mixer.music.load(path.join(music_folder,'mmmusic.mp3'))
                            py.mixer.music.play()
                            self.new()
                            map_screen = False
                        if map_me.target.text == 'TD Bank' and self.unlocked >=1:
                            if self.newGame:
                                self.printText('gameStart.txt',True)
                            self.area = 1
                            self.openTo = 0
                            self.maxTime = 450
                            self.allBosses = 4
                            self.bossRoom = 6
                            self.bossDown = 0
                            self.playerDead = False
                            self.levelMenu = False
                            py.mixer.music.load(path.join(music_folder,'l1music.mp3'))
                            py.mixer.music.play()
                            self.new()
                            map_screen = False
                        if map_me.target.text == 'Tangerine Rind Bank' and self.unlocked >=2:
                            self.area = 2
                            self.openTo = 0
                            self.maxTime = 480
                            self.allBosses = 2
                            self.bossRoom = 4
                            self.bossDown = 0
                            self.playerDead = False
                            self.levelMenu = False
                            py.mixer.music.load(path.join(music_folder,'l2music.mp3'))
                            py.mixer.music.play()
                            self.new()
                            map_screen = False
                        if map_me.target.text == 'Canadian Irresponsible Bank of Candy' and self.unlocked >=3:
                            self.area = 3
                            self.openTo = 0
                            self.maxTime = 420
                            self.allBosses = 2
                            self.bossRoom = 5
                            self.bossDown = 0
                            self.playerDead = False
                            self.levelMenu = False
                            py.mixer.music.load(path.join(music_folder,'l3music.mp3'))
                            py.mixer.music.play()
                            self.new()
                            map_screen = False
                        if map_me.target.text == 'Really Brutal Cops (RBC)' and self.unlocked >=4:
                            self.area = 4
                            self.openTo = 0
                            self.maxTime = 420
                            self.allBosses = 1
                            self.bossRoom = 4
                            self.bossDown = 0
                            self.playerDead = False
                            self.levelMenu = False
                            py.mixer.music.load(path.join(music_folder,'l4music.mp3'))
                            py.mixer.music.play()
                            self.new()
                            map_screen = False
                        if map_me.target.text == 'Scotiabank Stronghold' and self.unlocked >=5:
                            self.area = 5
                            self.openTo = 0
                            self.maxTime = 540
                            self.allBosses = 1
                            self.bossRoom = 6
                            self.bossDown = 0
                            self.playerDead = False
                            self.levelMenu = False
                            py.mixer.music.load(path.join(music_folder,'l5music.mp3'))
                            py.mixer.music.play()
                            self.new()
                            map_screen = False
                if event.type == py.KEYDOWN and event.key == py.K_ESCAPE:
                    self.paused()
                    if self.goToTitle:
                        map_screen = False
            map_me.update()
            screen.fill((0,0,0))
            info.fill((0,0,0))
            
            follow = vec(map_me.rect.x,map_me.rect.y)
            difference = follow - camera
            camera += difference
            offset = -camera + vec(WIDTH/2,HEIGHT/2)
            #update object positions due to new camera
            for i in map_stops:
                i.rect.left+=offset.x
            for i in levelCams:
                i.rect.left+=offset.x
            map_me.rect.left +=offset.x
            levelMapRect.x+=offset.x
            #changing the camera offset if the player is in a corner of the screen
            for i in levelCams:
                if ((i.direction == 2 and i.rect.x<WIDTH) or (i.direction == 4 and i.rect.right>0)) and i.showing:
                    for i in map_stops:
                        i.rect.left-=offset.x
                    for i in levelCams:
                        i.rect.left-=offset.x
                    map_me.rect.left -=offset.x
                    levelMapRect.x-=offset.x

            screen.blit(levelMapIMG, levelMapRect.topleft)
            screen.blit(map_me.image,map_me.rect)
            if map_me.xspeed == 0 and map_me.yspeed == 0 and map_me.target.text != "":
                text, rect = returnText(map_me.target.text,white,font24)
                rect.topleft = (10,10)
                info.blit(text,rect)
                screen.blit(info, (0,768-110))
                if map_me.target.text == 'TD Bank':
                    displaytextTL('High Score: '+str(self.bagsStolen[0]),WIDTH/2+100,HEIGHT-50,white,font24)
                if map_me.target.text == 'Tangerine Rind Bank':
                    displaytextTL('High Score: '+str(self.bagsStolen[1]),WIDTH/2+100,HEIGHT-50,white,font24)
                if map_me.target.text == 'Canadian Irresponsible Bank of Candy':
                    displaytextTL('High Score: '+str(self.bagsStolen[2]),WIDTH/2+100,HEIGHT-50,white,font24)
                if map_me.target.text == 'Really Brutal Cops (RBC)':
                    displaytextTL('High Score: '+str(self.bagsStolen[3]),WIDTH/2+100,HEIGHT-50,white,font24)
                if map_me.target.text == 'Scotiabank Stronghold':
                    displaytextTL('High Score: '+str(self.bagsStolen[4]),WIDTH/2+100,HEIGHT-50,white,font24)
                    
            pygame.display.flip()
            clock.tick(FPS)

    def bulletUpgrade(self):
        index2 = 0
        escapeTimer = 0
        self.purchasedBullets.append(self.equipedBullet[0])
        while True:
            pressed = py.key.get_pressed()
            if pressed[py.K_ESCAPE]:
                escapeTimer +=1
            else: escapeTimer = 0
            if escapeTimer >7:
                break
            clock.tick(FPS)
            screen.fill(black)
            displaytext("Upgrade Bullets",WIDTH/2,50,white,font24)
            displaytextTL('Press escape to leave',10,10,white,font18)
            py.draw.rect(screen,white,(100,200,WIDTH-200,300),3)
            for i in range(len(self.purchasedBullets)):
                if i <6:
                    screen.blit(self.purchasedBullets[i],(150+i*127,232))
                else: screen.blit(self.purchasedBullets[i],(150+(i-6)*127,382))
            if index2<6:
                py.draw.rect(screen, white, (148+index2*127,230,68,68),2)
            else:
                py.draw.rect(screen, white, (148+(index2-6)*127,380,68,68),2)
            
            if len(self.purchasedBullets)>0:
                if self.purchasedBullets[index2] == self.normalBullet:
                    itemNum = 0
                if self.purchasedBullets[index2] == self.dualBullet:
                    itemNum = 1
                if self.purchasedBullets[index2] == self.snowBullet:
                    itemNum = 2
                if self.purchasedBullets[index2] == self.sniperBullet:
                    itemNum = 3
                if self.purchasedBullets[index2] == self.antiBullet:
                    itemNum = 4
                if self.purchasedBullets[index2] == self.batteryBullet:
                    itemNum = 5
                    
                if self.bulletLevel[itemNum]<len(bulletLevelCosts[itemNum]):
                    itemInfo = bulletLevelText[itemNum][self.bulletLevel[itemNum]]
                else:
                    itemInfo = bulletLevelText[itemNum][self.bulletLevel[itemNum]-1]
                    itemInfoBonus = bulletEnhanceTextMod[itemNum]
                itemName = bulletNames[itemNum]

                if self.bulletLevel[itemNum]<(len(bulletLevelCosts[itemNum])-1):
                    screen.blit(ubutton1,urect_1)
                    screen.blit(ubutton2d,urect_2d)
                    py.draw.rect(screen,white,(100,HEIGHT-65,7,7),6)
                    printItemInfo = []
                    for i in range(7):
                        if len(itemInfo)>37:
                            printItemInfo.append(itemInfo[0:38])
                            itemInfo = itemInfo[38:]
                        if len(itemInfo)<=37:
                            printItemInfo.append(itemInfo)
                            break
                    for i in range(len(printItemInfo)):
                        displaytextTL(printItemInfo[i],100,HEIGHT-150+i*35,white,font24)
                    
                elif self.bulletLevel[itemNum]==(len(bulletLevelCosts[itemNum])-1):
                    screen.blit(ubutton1d,urect_1d)
                    screen.blit(ubutton2,urect_2)
                    py.draw.rect(screen,white,(350,HEIGHT-65,7,7),6)
                    printItemInfo = []
                    for i in range(7):
                        if len(itemInfo)>37:
                            printItemInfo.append(itemInfo[0:38])
                            itemInfo = itemInfo[38:]
                        if len(itemInfo)<=37:
                            printItemInfo.append(itemInfo)
                            break
                    for i in range(len(printItemInfo)):
                        displaytextTL(printItemInfo[i],100,HEIGHT-150+i*35,white,font24)
                else:
                    printItemInfo = []
                    for i in range(7):
                        if len(itemInfo)>37:
                            printItemInfo.append(itemInfo[0:38])
                            itemInfo = itemInfo[38:]
                        if len(itemInfo)<=37:
                            printItemInfo.append(itemInfo)
                            break
                    for i in range(len(printItemInfo)):
                        displaytextTL(printItemInfo[i],100,HEIGHT-100+i*35,white,font24)
                    printItemInfo = []
                    for i in range(7):
                        if len(itemInfoBonus)>37:
                            printItemInfo.append(itemInfoBonus[0:38])
                            itemInfoBonus = itemInfoBonus[38:]
                        if len(itemInfoBonus)<=37:
                            printItemInfo.append(itemInfoBonus)
                            break
                    for i in range(len(printItemInfo)):
                        displaytextTL(printItemInfo[i],100,HEIGHT-200+i*35,white,font24)

                screen.blit(self.mbag,(WIDTH-263,27))
                displaytext(':',WIDTH-200,50,white,font24)
                displaytext(str(self.totalGold),WIDTH-90,50,white,font24)

                displaytextTL(bulletUsage[itemNum]+' bullets per shot',WIDTH/2+100,HEIGHT-50,white,font18)
                
                if self.bulletLevel[itemNum]<len(bulletLevelCosts[itemNum])-1:
                    displaytextTL(('Level '+str(self.bulletLevel[itemNum]+1)+' '+itemName),100,HEIGHT-250,white,font24)
                elif self.bulletLevel[itemNum]==len(bulletLevelCosts[itemNum])-1:
                    displaytextTL(('Max level '+itemName),100,HEIGHT-250,white,font24)
                else:displaytextTL(('Max+ level '+itemName),100,HEIGHT-250,white,font24)
                change,select = events(6)
                index2+=change
                if index2>len(self.purchasedBullets)-1:
                    index2=0
                if index2<0:
                    index2=len(self.purchasedBullets)-1
                if select != 0 and self.bulletLevel[itemNum]<len(bulletLevelCosts[itemNum]):
                    selectedItem = self.purchasedBullets[index2]
                    index = 0
                    while True:
                        clock.tick(FPS)
                        screen.fill(black)
                        displaytext("Upgrade Bullets",WIDTH/2,50,white,font24)
                            
                        screen.blit(selectedItem,(WIDTH/2-32,HEIGHT/2-200))
                        
                        if self.purchasedBullets[index2] == self.normalBullet:
                            itemNum = 0
                        if self.purchasedBullets[index2] == self.dualBullet:
                            itemNum = 1
                        if self.purchasedBullets[index2] == self.snowBullet:
                            itemNum = 2
                        if self.purchasedBullets[index2] == self.sniperBullet:
                            itemNum = 3
                        if self.purchasedBullets[index2] == self.antiBullet:
                            itemNum = 4
                        if self.purchasedBullets[index2] == self.batteryBullet:
                            itemNum = 5

                        if self.bulletLevel[itemNum]<len(bulletLevelCosts[itemNum])-1:
                            itemInfo = 'Level '+str(self.bulletLevel[itemNum]+1)+': '+bulletLevelText[itemNum][self.bulletLevel[itemNum]]
                            if self.bulletLevel[itemNum]==len(bulletLevelCosts[itemNum])-2:
                                nextInfo = 'Max Level: '+bulletLevelText[itemNum][self.bulletLevel[itemNum]+1]
                            else:
                                nextInfo = 'Level '+str(self.bulletLevel[itemNum]+2)+': '+bulletLevelText[itemNum][self.bulletLevel[itemNum]+1]
                        else:
                            itemInfo = 'Effect: '+bulletEnhanceText[itemNum]
                        itemName = bulletNames[itemNum]
                        itemCost = bulletLevelCosts[itemNum][self.bulletLevel[itemNum]]

                        if self.bulletLevel[itemNum]<(len(bulletLevelCosts[itemNum])-1):
                            screen.blit(ubutton3,urect_3)
                            screen.blit(ubutton5,urect_5)
                            displaytext('Upgrade to next level?',WIDTH/2,HEIGHT/2-105,white,font24)
                            displaytext(itemInfo,WIDTH/2,HEIGHT/2-45,white,font24)
                            displaytext(nextInfo,WIDTH/2,HEIGHT/2,white,font24)
                            
                        elif self.bulletLevel[itemNum]==(len(bulletLevelCosts[itemNum])-1):
                            screen.blit(ubutton4,urect_4)
                            screen.blit(ubutton5,urect_5)
                            displaytext('Enhance this item?',WIDTH/2,HEIGHT/2-105,white,font24)
                            printItemInfo = []
                            for i in range(7):
                                if len(itemInfo)>41:
                                    printItemInfo.append(itemInfo[0:42])
                                    itemInfo = itemInfo[42:]
                                if len(itemInfo)<=41:
                                    printItemInfo.append(itemInfo)
                                    break
                            for i in range(len(printItemInfo)):
                                displaytext(printItemInfo[i],WIDTH/2,HEIGHT/2-45+i*35,white,font24)

                        displaytextTL('Cost: ',20,HEIGHT-50,white,font24)
                        displaytextTL(str(itemCost),150,HEIGHT-50,white,font24)
                        
                        displaytextTL(bulletUsage[itemNum]+' bullets per shot',WIDTH/2+100,HEIGHT-50,white,font18)
                        
                        screen.blit(self.mbag,(WIDTH-263,27))
                        displaytext(':',WIDTH-200,50,white,font24)
                        displaytext(str(self.totalGold),WIDTH-90,50,white,font24)
                        
                        if self.totalGold<itemCost:
                            displaytext('not enough money to purchase!',WIDTH/2,HEIGHT-200,white,font24)

                        py.draw.rect(screen, white, [upgradeRectList[index].left-15,upgradeRectList[index].centery,6,6],5)
                        #check events
                        change,select = events(5)
                        index +=change
                        #making sure the selector stays in range
                        if index >1:
                            index = 0
                        if index < 0:
                            index = 1
                        #when you select, determining what to do
                        if select !=0:
                            if index == 0:
                                if self.totalGold>=itemCost:
                                    self.bulletLevel[itemNum] +=1
                                    self.totalGold = int(self.totalGold-itemCost)
                                    if  selectedItem == self.antiBullet:
                                        if self.bulletLevel[4]==1:
                                            self.bulletTime[4] = 2880
                                        if self.bulletLevel[4]==2:
                                            self.bulletTime[4] = 2760
                                        if self.bulletLevel[4]==3:
                                            self.bulletTime[4] = 2580
                                        if self.bulletLevel[4]==4:
                                            self.bulletTime[4] = 2400
                                        if self.bulletLevel[4]==5:
                                            self.bulletTime[4] = 2220
                                        if self.bulletLevel[4]==6:
                                            self.bulletTime[4] = 2040
                                        if self.bulletLevel[4]==7:
                                            self.bulletTime[4] = 1800
                                        if self.bulletLevel[4]==8:
                                            self.bulletTime[4] = 1500
                                        if self.bulletLevel[4]==9:
                                            self.bulletTime[4] = 1200
                                        
                                    break
                            if index == 1:
                                break
                        py.display.flip()
            else:
                for event in py.event.get():
                    if event.type == py.QUIT:
                        py.quit()
                        py.mixer.quit()
                        exit()
                displaytext('No upgradeable bullets',WIDTH/2,HEIGHT/2, white, font30)        
            py.display.flip()
        self.purchasedBullets.remove(self.equipedBullet[0])

    def powerupUpgrade(self):
        index2 = 0
        escapeTimer = 0
        for i in range(len(self.equipedItems)):
            if self.equipedItems[i] != 'none':
                self.purchasedItems.append(self.equipedItems[i])
        while True:
            pressed = py.key.get_pressed()
            if pressed[py.K_ESCAPE]:
                escapeTimer +=1
            else: escapeTimer = 0
            if escapeTimer >7:
                break
            clock.tick(FPS)
            screen.fill(black)
            displaytext("Upgrade Powerups",WIDTH/2,50,white,font24)
            displaytextTL('Press escape to leave',10,10,white,font18)
            py.draw.rect(screen,white,(100,200,WIDTH-200,300),3)
            for i in range(len(self.purchasedItems)):
                if i <6:
                    screen.blit(self.purchasedItems[i],(150+i*127,232))
                else: screen.blit(self.purchasedItems[i],(150+(i-6)*127,382))
            if index2<6:
                py.draw.rect(screen, white, (148+index2*127,230,68,68),2)
            else:
                py.draw.rect(screen, white, (148+(index2-6)*127,380,68,68),2)
            
            if len(self.purchasedItems)>0:
                if self.purchasedItems[index2] == self.heartPowerup:
                    itemNum = 0
                if self.purchasedItems[index2] == self.speedPowerup:
                    itemNum = 1
                if self.purchasedItems[index2] == self.shootingPowerup:
                    itemNum = 2
                if self.purchasedItems[index2] == self.meleePowerup:
                    itemNum = 3
                if self.purchasedItems[index2] == self.valentinesPowerup:
                    itemNum = 4
                if self.purchasedItems[index2] == self.quickPowerup:
                    itemNum = 5
                if self.purchasedItems[index2] == self.steelPowerup:
                    itemNum = 6
                if self.purchasedItems[index2] == self.firePowerup:
                    itemNum = 7
                if self.purchasedItems[index2] == self.C4Powerup:
                    itemNum = 8
                if self.purchasedItems[index2] == self.blockPowerup:
                    itemNum = 9
                if self.purchasedItems[index2] == self.deanPowerup:
                    itemNum = 10
                    
                if self.powerupLevel[itemNum]<len(itemLevelCosts[itemNum]):
                    itemInfo = itemLevelText[itemNum][self.powerupLevel[itemNum]]
                else:
                    itemInfo = itemLevelText[itemNum][self.powerupLevel[itemNum]-1]
                    itemInfoBonus = itemEnhanceTextMod[itemNum]
                itemName = itemNames[itemNum]

                if self.powerupLevel[itemNum]<(len(itemLevelCosts[itemNum])-1):
                    screen.blit(ubutton1,urect_1)
                    screen.blit(ubutton2d,urect_2d)
                    py.draw.rect(screen,white,(100,HEIGHT-65,7,7),6)
                    printItemInfo = []
                    for i in range(7):
                        if len(itemInfo)>37:
                            printItemInfo.append(itemInfo[0:38])
                            itemInfo = itemInfo[38:]
                        if len(itemInfo)<=37:
                            printItemInfo.append(itemInfo)
                            break
                    for i in range(len(printItemInfo)):
                        displaytextTL(printItemInfo[i],100,HEIGHT-150+i*35,white,font24)
                    
                elif self.powerupLevel[itemNum]==(len(itemLevelCosts[itemNum])-1):
                    screen.blit(ubutton1d,urect_1d)
                    screen.blit(ubutton2,urect_2)
                    py.draw.rect(screen,white,(350,HEIGHT-65,7,7),6)
                    printItemInfo = []
                    for i in range(7):
                        if len(itemInfo)>37:
                            printItemInfo.append(itemInfo[0:38])
                            itemInfo = itemInfo[38:]
                        if len(itemInfo)<=37:
                            printItemInfo.append(itemInfo)
                            break
                    for i in range(len(printItemInfo)):
                        displaytextTL(printItemInfo[i],100,HEIGHT-150+i*35,white,font24)
                else:
                    if itemNum !=5 and itemNum != 8:
                        printItemInfo = []
                        for i in range(7):
                            if len(itemInfo)>37:
                                printItemInfo.append(itemInfo[0:38])
                                itemInfo = itemInfo[38:]
                            if len(itemInfo)<=37:
                                printItemInfo.append(itemInfo)
                                break
                        for i in range(len(printItemInfo)):
                            displaytextTL(printItemInfo[i],100,HEIGHT-100+i*35,white,font24)
                    printItemInfo = []
                    for i in range(7):
                        if len(itemInfoBonus)>37:
                            printItemInfo.append(itemInfoBonus[0:38])
                            itemInfoBonus = itemInfoBonus[38:]
                        if len(itemInfoBonus)<=37:
                            printItemInfo.append(itemInfoBonus)
                            break
                    for i in range(len(printItemInfo)):
                        displaytextTL(printItemInfo[i],100,HEIGHT-200+i*35,white,font24)

                screen.blit(self.mbag,(WIDTH-263,27))
                displaytext(':',WIDTH-200,50,white,font24)
                displaytext(str(self.totalGold),WIDTH-90,50,white,font24)
                    
                if self.powerupLevel[itemNum]<len(itemLevelCosts[itemNum])-1:
                    displaytextTL(('Level '+str(self.powerupLevel[itemNum]+1)+' '+itemName),100,HEIGHT-250,white,font24)
                elif self.powerupLevel[itemNum]==len(itemLevelCosts[itemNum])-1:
                    displaytextTL(('Max level '+itemName),100,HEIGHT-250,white,font24)
                else:displaytextTL(('Max+ level '+itemName),100,HEIGHT-250,white,font24)
                change,select = events(6)
                index2+=change
                if index2>len(self.purchasedItems)-1:
                    index2=0
                if index2<0:
                    index2=len(self.purchasedItems)-1
                if select != 0 and self.powerupLevel[itemNum]<len(itemLevelCosts[itemNum]):
                    selectedItem = self.purchasedItems[index2]
                    index = 0
                    while True:
                        clock.tick(FPS)
                        screen.fill(black)
                        displaytext("Upgrade Powerups",WIDTH/2,50,white,font24)
                            
                        screen.blit(selectedItem,(WIDTH/2-32,HEIGHT/2-200))
                        
                        if self.purchasedItems[index2] == self.heartPowerup:
                            itemNum = 0
                        if self.purchasedItems[index2] == self.speedPowerup:
                            itemNum = 1
                        if self.purchasedItems[index2] == self.shootingPowerup:
                            itemNum = 2
                        if self.purchasedItems[index2] == self.meleePowerup:
                            itemNum = 3
                        if self.purchasedItems[index2] == self.valentinesPowerup:
                            itemNum = 4
                        if self.purchasedItems[index2] == self.quickPowerup:
                            itemNum = 5
                        if self.purchasedItems[index2] == self.steelPowerup:
                            itemNum = 6
                        if self.purchasedItems[index2] == self.firePowerup:
                            itemNum = 7
                        if self.purchasedItems[index2] == self.C4Powerup:
                            itemNum = 8
                        if self.purchasedItems[index2] == self.blockPowerup:
                            itemNum = 9
                        if self.purchasedItems[index2] == self.deanPowerup:
                            itemNum = 10
                        
                        if self.powerupLevel[itemNum]<len(itemLevelCosts[itemNum])-1:
                            itemInfo = 'Level '+str(self.powerupLevel[itemNum]+1)+': '+itemLevelText[itemNum][self.powerupLevel[itemNum]]
                            if self.powerupLevel[itemNum]==len(itemLevelCosts[itemNum])-2:
                                nextInfo = 'Max Level: '+itemLevelText[itemNum][self.powerupLevel[itemNum]+1]
                            else:
                                nextInfo = 'Level '+str(self.powerupLevel[itemNum]+2)+': '+itemLevelText[itemNum][self.powerupLevel[itemNum]+1]
                        else:
                            itemInfo = 'Effect: '+itemEnhanceText[itemNum]
                        itemName = itemNames[itemNum]
                        itemCost = itemLevelCosts[itemNum][self.powerupLevel[itemNum]]

                        if self.powerupLevel[itemNum]<(len(itemLevelCosts[itemNum])-1):
                            screen.blit(ubutton3,urect_3)
                            screen.blit(ubutton5,urect_5)
                            displaytext('Upgrade to next level?',WIDTH/2,HEIGHT/2-105,white,font24)
                            displaytext(itemInfo,WIDTH/2,HEIGHT/2-45,white,font24)
                            displaytext(nextInfo,WIDTH/2,HEIGHT/2,white,font24)
                            
                        elif self.powerupLevel[itemNum]==(len(itemLevelCosts[itemNum])-1):
                            screen.blit(ubutton4,urect_4)
                            screen.blit(ubutton5,urect_5)
                            displaytext('Enhance this item?',WIDTH/2,HEIGHT/2-105,white,font24)
                            printItemInfo = []
                            for i in range(7):
                                if len(itemInfo)>41:
                                    printItemInfo.append(itemInfo[0:42])
                                    itemInfo = itemInfo[42:]
                                if len(itemInfo)<=41:
                                    printItemInfo.append(itemInfo)
                                    break
                            for i in range(len(printItemInfo)):
                                displaytext(printItemInfo[i],WIDTH/2,HEIGHT/2-45+i*35,white,font24)

                        screen.blit(self.mbag,(WIDTH-263,27))
                        displaytext(':',WIDTH-200,50,white,font24)
                        displaytext(str(self.totalGold),WIDTH-90,50,white,font24)

                        displaytextTL('Cost: ',20,HEIGHT-50,white,font24)
                        displaytextTL(str(itemCost),150,HEIGHT-50,white,font24)
                        
                        if self.totalGold<itemCost:
                            displaytext('not enough money to purchase!',WIDTH/2,HEIGHT-200,white,font24)

                        py.draw.rect(screen, white, [upgradeRectList[index].left-15,upgradeRectList[index].centery,6,6],5)
                        #check events
                        change,select = events(5)
                        index +=change
                        #making sure the selector stays in range
                        if index >1:
                            index = 0
                        if index < 0:
                            index = 1
                        #when you select, determining what to do
                        if select !=0:
                            if index == 0:
                                if self.totalGold>=itemCost:
                                    self.powerupLevel[itemNum] +=1
                                    self.totalGold = int(self.totalGold-itemCost)
                                    if self.powerupLevel[itemNum]==(len(itemLevelCosts[itemNum])):
                                        if self.purchasedItems[index2] == self.heartPowerup:
                                            del self.purchasedItems[index2]
                                            for i in range(len(self.equipedItems)):
                                                if self.equipedItems[i] == self.heartPowerup:
                                                    self.equipedItems[i] = self.maxedList[0]
                                            self.heartPowerup = self.maxedList[0]
                                            self.purchasedItems.insert(index2,self.heartPowerup)
                                        if self.purchasedItems[index2] == self.speedPowerup:
                                            del self.purchasedItems[index2]
                                            for i in range(len(self.equipedItems)):
                                                if self.equipedItems[i] == self.speedPowerup:
                                                    self.equipedItems[i] = self.maxedList[1]
                                            self.speedPowerup = self.maxedList[1]
                                            self.purchasedItems.insert(index2,self.speedPowerup)
                                        if self.purchasedItems[index2] == self.shootingPowerup:
                                            del self.purchasedItems[index2]
                                            for i in range(len(self.equipedItems)):
                                                if self.equipedItems[i] == self.shootingPowerup:
                                                    self.equipedItems[i] = self.maxedList[2]
                                            self.shootingPowerup = self.maxedList[2]
                                            self.purchasedItems.insert(index2,self.shootingPowerup)
                                        if self.purchasedItems[index2] == self.meleePowerup:
                                            del self.purchasedItems[index2]
                                            for i in range(len(self.equipedItems)):
                                                if self.equipedItems[i] == self.meleePowerup:
                                                    self.equipedItems[i] = self.maxedList[3]
                                            self.meleePowerup = self.maxedList[3]
                                            self.purchasedItems.insert(index2,self.meleePowerup)
                                        if self.purchasedItems[index2] == self.valentinesPowerup:
                                            del self.purchasedItems[index2]
                                            for i in range(len(self.equipedItems)):
                                                if self.equipedItems[i] == self.valentinesPowerup:
                                                    self.equipedItems[i] = self.maxedList[4]
                                            self.valentinesPowerup = self.maxedList[4]
                                            self.purchasedItems.insert(index2,self.valentinesPowerup)
                                        if self.purchasedItems[index2] == self.quickPowerup:
                                            del self.purchasedItems[index2]
                                            for i in range(len(self.equipedItems)):
                                                if self.equipedItems[i] == self.quickPowerup:
                                                    self.equipedItems[i] = self.maxedList[5]
                                            self.quickPowerup = self.maxedList[5]
                                            self.purchasedItems.insert(index2,self.quickPowerup)
                                        if self.purchasedItems[index2] == self.steelPowerup:
                                            del self.purchasedItems[index2]
                                            for i in range(len(self.equipedItems)):
                                                if self.equipedItems[i] == self.steelPowerup:
                                                    self.equipedItems[i] = self.maxedList[6]
                                            self.steelPowerup = self.maxedList[6]
                                            self.purchasedItems.insert(index2,self.steelPowerup)
                                        if self.purchasedItems[index2] == self.firePowerup:
                                            del self.purchasedItems[index2]
                                            for i in range(len(self.equipedItems)):
                                                if self.equipedItems[i] == self.firePowerup:
                                                    self.equipedItems[i] = self.maxedList[7]
                                            self.firePowerup = self.maxedList[7]
                                            self.purchasedItems.insert(index2,self.firePowerup)
                                            self.movingFire = self.movingFireG
                                            
                                        if self.purchasedItems[index2] == self.C4Powerup:
                                            del self.purchasedItems[index2]
                                            for i in range(len(self.equipedItems)):
                                                if self.equipedItems[i] == self.C4Powerup:
                                                    self.equipedItems[i] = self.maxedList[8]
                                            self.C4Powerup = self.maxedList[8]
                                            self.purchasedItems.insert(index2,self.C4Powerup)
                                        if self.purchasedItems[index2] == self.blockPowerup:
                                            del self.purchasedItems[index2]
                                            for i in range(len(self.equipedItems)):
                                                if self.equipedItems[i] == self.blockPowerup:
                                                    self.equipedItems[i] = self.maxedList[9]
                                            self.blockPowerup = self.maxedList[9]
                                            self.purchasedItems.insert(index2,self.blockPowerup)
                                        if self.purchasedItems[index2] == self.deanPowerup:
                                            del self.purchasedItems[index2]
                                            for i in range(len(self.equipedItems)):
                                                if self.equipedItems[i] == self.deanPowerup:
                                                    self.equipedItems[i] = self.maxedList[10]
                                            self.deanPowerup = self.maxedList[10]
                                            self.purchasedItems.insert(index2,self.deanPowerup)
                                    for i in self.equipedItems:
                                        if selectedItem == self.heartPowerup and i == self.heartPowerup:
                                            if self.powerupLevel[0] == 1:
                                                self.hearts +=1
                                            if self.powerupLevel[0] == 3:
                                                self.hearts +=1
                                        if selectedItem == self.steelPowerup and i == self.steelPowerup:
                                            if self.powerupLevel[6]<3:
                                                self.speedPercent +=.05
                                            elif self.powerupLevel <5:
                                                self.speedPercent +=.1
                                    break
                            if index == 1:
                                break
                        py.display.flip()
            else:
                for event in py.event.get():
                    if event.type == py.QUIT:
                        py.quit()
                        py.mixer.quit()
                        exit()
                displaytext('No upgradeable powerups',WIDTH/2,HEIGHT/2, white, font30)        
            py.display.flip()
        screen.fill(black)
        for i in range(len(self.equipedItems)):
            if self.equipedItems[i] != 'none':
                self.purchasedItems.remove(self.equipedItems[i])

    def bulletMenu(self):
        index2 = 0
        escapeTimer = 0
        #bullet menu
        while True:
            pressed = py.key.get_pressed()
            if pressed[py.K_ESCAPE]:
                escapeTimer +=1
            else: escapeTimer = 0
            if escapeTimer >7:
                break
            clock.tick(FPS)
            screen.fill(black)
            displaytext('You can  automatically switch your bullet type in game',WIDTH/2,75,white,font18)
            displaytext('by pressing < or >',WIDTH/2,100,white,font18)
            
            displaytext("Bullet Menu",WIDTH/2,50,white,font24)
            displaytextTL('Press escape to leave',10,10,white,font18)
            py.draw.rect(screen, white,[WIDTH/2-16,120,66,66],2)
            
            screen.blit(self.equipedBullet[0],(WIDTH/2-14,122))
                
            py.draw.rect(screen,white,(100,200,WIDTH-200,300),3)
            for i in range(len(self.purchasedBullets)):
                if i <6:
                    screen.blit(self.purchasedBullets[i],(150+i*127,232))
                else: screen.blit(self.purchasedBullets[i],(150+(i-6)*127,382))
            if index2<6:
                py.draw.rect(screen, white, (182+index2*127,220,6,6),5)
                py.draw.rect(screen, white, (148+index2*127,230,68,68),2)
            else:
                py.draw.rect(screen, white, (182+(index2-6)*127,370,6,6),5)
                py.draw.rect(screen, white, (148+(index2-6)*127,380,68,68),2)
            
            if len(self.purchasedBullets)>0:
                if self.purchasedBullets[index2] == self.normalBullet:
                    itemNum = 0
                if self.purchasedBullets[index2] == self.dualBullet:
                    itemNum = 1
                if self.purchasedBullets[index2] == self.snowBullet:
                    itemNum = 2
                if self.purchasedBullets[index2] == self.sniperBullet:
                    itemNum = 3
                if self.purchasedBullets[index2] == self.antiBullet:
                    itemNum = 4
                if self.purchasedBullets[index2] == self.batteryBullet:
                    itemNum = 5
                    
                if self.bulletLevel[itemNum]<len(bulletLevelCosts[itemNum]):
                    itemInfo = bulletLevelText[itemNum][self.bulletLevel[itemNum]]
                else:
                    itemInfo = bulletLevelText[itemNum][self.bulletLevel[itemNum]-1]
                    itemInfoBonus = bulletEnhanceTextMod[itemNum]
                itemName = bulletNames[itemNum]
                
                if self.bulletLevel[itemNum]<(len(bulletLevelCosts[itemNum])-1):
                    printItemInfo = []
                    for i in range(7):
                        if len(itemInfo)>37:
                            printItemInfo.append(itemInfo[0:38])
                            itemInfo = itemInfo[38:]
                        if len(itemInfo)<=37:
                            printItemInfo.append(itemInfo)
                            break
                    for i in range(len(printItemInfo)):
                        displaytextTL(printItemInfo[i],100,HEIGHT-150+i*25,white,font18)
                    
                elif self.bulletLevel[itemNum]==(len(bulletLevelCosts[itemNum])-1):
                    printItemInfo = []
                    for i in range(7):
                        if len(itemInfo)>37:
                            printItemInfo.append(itemInfo[0:38])
                            itemInfo = itemInfo[38:]
                        if len(itemInfo)<=37:
                            printItemInfo.append(itemInfo)
                            break
                    for i in range(len(printItemInfo)):
                        displaytextTL(printItemInfo[i],100,HEIGHT-150+i*25,white,font18)
                else:
                    printItemInfo = []
                    for i in range(7):
                        if len(itemInfo)>37:
                            printItemInfo.append(itemInfo[0:38])
                            itemInfo = itemInfo[38:]
                        if len(itemInfo)<=37:
                            printItemInfo.append(itemInfo)
                            break
                    for i in range(len(printItemInfo)):
                        displaytextTL(printItemInfo[i],100,HEIGHT-70+i*25,white,font18)
                    printItemInfo = []
                    for i in range(7):
                        if len(itemInfoBonus)>37:
                            printItemInfo.append(itemInfoBonus[0:38])
                            itemInfoBonus = itemInfoBonus[38:]
                        if len(itemInfoBonus)<=37:
                            printItemInfo.append(itemInfoBonus)
                            break
                    for i in range(len(printItemInfo)):
                        displaytextTL(printItemInfo[i],100,HEIGHT-150+i*25,white,font18)
                    
                if self.bulletLevel[itemNum]<len(bulletLevelCosts[itemNum])-1:
                    displaytextTL(('Level '+str(self.bulletLevel[itemNum]+1)+' '+itemName),20,HEIGHT-180,white,font24)
                elif self.bulletLevel[itemNum]==len(bulletLevelCosts[itemNum])-1:
                    displaytextTL(('Max level '+itemName),20,HEIGHT-180,white,font24)
                else:displaytextTL(('Max+ level '+itemName),20,HEIGHT-180,white,font24)
                displaytextTL(bulletUsage[itemNum]+' bullets per shot',WIDTH/2+100,HEIGHT-250,white,font18)
                
                change,select = events(6)
                index2+=change
                if index2>len(self.purchasedBullets)-1:
                    index2=0
                if index2<0:
                    index2=len(self.purchasedBullets)-1
                if select != 0:
                    selectedItem = self.purchasedBullets[index2]
                
                    while True:
                        clock.tick(FPS)
                        screen.fill(black)
                        displaytext("Bullet menu",WIDTH/2,50,white,font24)
                        displaytextTL('Press escape to leave',10,10,white,font18)
                        py.draw.rect(screen, white,[WIDTH/2-16,120,66,66],2)

                        screen.blit(self.equipedBullet[0],(WIDTH/2-14,122))
                        
                            
                        py.draw.rect(screen,white,(100,200,WIDTH-200,300),3)
                            
                        for i in range(len(self.purchasedBullets)):
                            if i <6:
                                screen.blit(self.purchasedBullets[i],(150+i*127,232))
                            else: screen.blit(self.purchasedBullets[i],(150+(i-6)*127,382))
                                
                        py.draw.rect(screen, white, (WIDTH/2-84+100,110,6,6),5)
                        if index2<6:
                            py.draw.rect(screen, white, (148+index2*127,230,68,68),2)
                        else:
                            py.draw.rect(screen, white, (148+(index2-6)*127,380,68,68),2)
                        
                        if index2!=0 and len(self.purchasedBullets)>0:
                            if self.purchasedBullets[index2] == self.normalBullet:
                                itemNum = 0
                            if self.purchasedBullets[index2] == self.dualBullet:
                                itemNum = 1
                            if self.purchasedBullets[index2] == self.snowBullet:
                                itemNum = 2
                            if self.purchasedBullets[index2] == self.sniperBullet:
                                itemNum = 3
                            if self.purchasedBullets[index2] == self.antiBullet:
                                itemNum = 4
                            if self.purchasedBullets[index2] == self.batteryBullet:
                                itemNum = 5
                            
                            if self.bulletLevel[itemNum]<len(bulletLevelCosts[itemNum]):
                                itemInfo = bulletLevelText[itemNum][self.bulletLevel[itemNum]]
                            else:
                                itemInfo = bulletLevelText[itemNum][self.bulletLevel[itemNum]-1]
                                itemInfoBonus = bulletEnhanceTextMod[itemNum]
                            itemName = bulletNames[itemNum]
                            
                            if self.bulletLevel[itemNum]<(len(bulletLevelCosts[itemNum])-1):
                                py.draw.rect(screen,white,(100,HEIGHT-65,7,7),6)
                                printItemInfo = []
                                for i in range(7):
                                    if len(itemInfo)>37:
                                        printItemInfo.append(itemInfo[0:38])
                                        itemInfo = itemInfo[38:]
                                    if len(itemInfo)<=37:
                                        printItemInfo.append(itemInfo)
                                        break
                                for i in range(len(printItemInfo)):
                                    displaytextTL(printItemInfo[i],100,HEIGHT-150+i*25,white,font18)
                                
                            elif self.bulletLevel[itemNum]==(len(bulletLevelCosts[itemNum])-1):
                                py.draw.rect(screen,white,(350,HEIGHT-65,7,7),6)
                                printItemInfo = []
                                for i in range(7):
                                    if len(itemInfo)>37:
                                        printItemInfo.append(itemInfo[0:38])
                                        itemInfo = itemInfo[38:]
                                    if len(itemInfo)<=37:
                                        printItemInfo.append(itemInfo)
                                        break
                                for i in range(len(printItemInfo)):
                                    displaytextTL(printItemInfo[i],100,HEIGHT-150+i*25,white,font18)
                            else:
                                printItemInfo = []
                                for i in range(7):
                                    if len(itemInfo)>37:
                                        printItemInfo.append(itemInfo[0:38])
                                        itemInfo = itemInfo[38:]
                                    if len(itemInfo)<=37:
                                        printItemInfo.append(itemInfo)
                                        break
                                for i in range(len(printItemInfo)):
                                    displaytextTL(printItemInfo[i],100,HEIGHT-70+i*25,white,font18)
                                printItemInfo = []
                                for i in range(7):
                                    if len(itemInfoBonus)>37:
                                        printItemInfo.append(itemInfoBonus[0:38])
                                        itemInfoBonus = itemInfoBonus[38:]
                                    if len(itemInfoBonus)<=37:
                                        printItemInfo.append(itemInfoBonus)
                                        break
                                for i in range(len(printItemInfo)):
                                    displaytextTL(printItemInfo[i],100,HEIGHT-150+i*25,white,font18)
                            
                        if self.bulletLevel[itemNum]<len(bulletLevelCosts[itemNum])-1:
                            displaytextTL(('Level '+str(self.bulletLevel[itemNum]+1)+' '+itemName),20,HEIGHT-180,white,font24)
                        elif self.bulletLevel[itemNum]==len(bulletLevelCosts[itemNum])-1:
                            displaytextTL(('Max level '+itemName),20,HEIGHT-180,white,font24)
                        else:displaytextTL(('Max+ level '+itemName),20,HEIGHT-180,white,font24)
                        
                        displaytextTL(bulletUsage[itemNum]+' bullets per shot',WIDTH/2+100,HEIGHT-250,white,font18)
                        
                        sectionNotTrue = False
                        pressed = py.key.get_pressed()
                        if pressed[py.K_ESCAPE]:
                            sectionNotTrue = True
                        for event in py.event.get():
                            if event.type == py.QUIT:
                                py.quit()
                                py.mixer.quit()
                                sys.exit()
                            if event.type == py.KEYDOWN and event.key == py.K_RETURN:
                                self.purchasedBullets.remove(selectedItem)
                                self.purchasedBullets.append(self.equipedBullet[0])
                                self.equipedBullet[0] = selectedItem
                                sectionNotTrue = True
                        if sectionNotTrue:
                            index2 = 0
                            break
                        py.display.flip()
            else:
                for event in py.event.get():
                    if event.type == py.QUIT:
                        py.quit()
                        py.mixer.quit()
                        exit()
                displaytext('No purchased bullets',WIDTH/2,HEIGHT/2, white, font30)        
            py.display.flip()

    def inventoryMenu(self):
        index2 = 0
        changeIndex = 0
        escapeTimer = 0
        #the shop menu########### WIP #########
        while True:
            pressed = py.key.get_pressed()
            if pressed[py.K_ESCAPE]:
                escapeTimer +=1
            else: escapeTimer = 0
            if escapeTimer >7:
                break
            clock.tick(FPS)
            screen.fill(black)
            displaytext("Powerups",WIDTH/2,50,white,font24)
            displaytextTL('Press escape to leave',10,10,white,font18)
            py.draw.rect(screen, white,[WIDTH/2-116,120,66,66],2)
            py.draw.rect(screen, white,[WIDTH/2-16,120,66,66],2)
            py.draw.rect(screen, white,[WIDTH/2+84,120,66,66],2)
            for i in range(len(self.equipedItems)):
                if self.equipedItems[i]!= 'none':
                    screen.blit(self.equipedItems[i],(WIDTH/2-114+100*i,122))
            for i in range(3-self.unlockedSlots):
                screen.blit(self.lockedSlot,(WIDTH/2+85-i*100,121))
                
            py.draw.rect(screen,white,(100,200,WIDTH-200,300),3)
            
            for i in range(len(self.purchasedItems)+1):
                if i != 0:
                    if i <6:
                        screen.blit(self.purchasedItems[i-1],(150+i*127,232))
                    else: screen.blit(self.purchasedItems[i-1],(150+(i-6)*127,382))
            if index2<6:
                py.draw.rect(screen, white, (182+index2*127,220,6,6),5)
                py.draw.rect(screen, white, (148+index2*127,230,68,68),2)
            else:
                py.draw.rect(screen, white, (182+(index2-6)*127,370,6,6),5)
                py.draw.rect(screen, white, (148+(index2-6)*127,380,68,68),2)
            
            if index2!=0 and len(self.purchasedItems)>0:
                if self.purchasedItems[index2-1] == self.heartPowerup:
                    itemNum = 0
                if self.purchasedItems[index2-1] == self.speedPowerup:
                    itemNum = 1
                if self.purchasedItems[index2-1] == self.shootingPowerup:
                    itemNum = 2
                if self.purchasedItems[index2-1] == self.meleePowerup:
                    itemNum = 3
                if self.purchasedItems[index2-1] == self.valentinesPowerup:
                    itemNum = 4
                if self.purchasedItems[index2-1] == self.quickPowerup:
                    itemNum = 5
                if self.purchasedItems[index2-1] == self.steelPowerup:
                    itemNum = 6
                if self.purchasedItems[index2-1] == self.firePowerup:
                    itemNum = 7
                if self.purchasedItems[index2-1] == self.C4Powerup:
                    itemNum = 8
                if self.purchasedItems[index2-1] == self.blockPowerup:
                    itemNum = 9
                if self.purchasedItems[index2-1] == self.deanPowerup:
                    itemNum = 10

                if self.powerupLevel[itemNum]<len(itemLevelCosts[itemNum]):
                    itemInfo = itemLevelText[itemNum][self.powerupLevel[itemNum]]
                else:
                    itemInfo = itemLevelText[itemNum][self.powerupLevel[itemNum]-1]
                    itemInfoBonus = itemEnhanceTextMod[itemNum]
                itemName = itemNames[itemNum]

                if self.powerupLevel[itemNum]<(len(itemLevelCosts[itemNum])-1):
                    printItemInfo = []
                    for i in range(7):
                        if len(itemInfo)>37:
                            printItemInfo.append(itemInfo[0:38])
                            itemInfo = itemInfo[38:]
                        if len(itemInfo)<=37:
                            printItemInfo.append(itemInfo)
                            break
                    for i in range(len(printItemInfo)):
                        displaytextTL(printItemInfo[i],100,HEIGHT-150+i*25,white,font18)
                    
                elif self.powerupLevel[itemNum]==(len(itemLevelCosts[itemNum])-1):
                    printItemInfo = []
                    for i in range(7):
                        if len(itemInfo)>37:
                            printItemInfo.append(itemInfo[0:38])
                            itemInfo = itemInfo[38:]
                        if len(itemInfo)<=37:
                            printItemInfo.append(itemInfo)
                            break
                    for i in range(len(printItemInfo)):
                        displaytextTL(printItemInfo[i],100,HEIGHT-150+i*25,white,font18)
                else:
                    if itemNum !=5 and itemNum != 8:
                        printItemInfo = []
                        for i in range(7):
                            if len(itemInfo)>37:
                                printItemInfo.append(itemInfo[0:38])
                                itemInfo = itemInfo[38:]
                            if len(itemInfo)<=37:
                                printItemInfo.append(itemInfo)
                                break
                        for i in range(len(printItemInfo)):
                            displaytextTL(printItemInfo[i],100,HEIGHT-70+i*25,white,font18)
                    printItemInfo = []
                    for i in range(7):
                        if len(itemInfoBonus)>37:
                            printItemInfo.append(itemInfoBonus[0:38])
                            itemInfoBonus = itemInfoBonus[38:]
                        if len(itemInfoBonus)<=37:
                            printItemInfo.append(itemInfoBonus)
                            break
                    for i in range(len(printItemInfo)):
                        displaytextTL(printItemInfo[i],100,HEIGHT-150+i*25,white,font18)
                        
                
                itemBooster = itemValues[itemNum]
            if index2 == 0:
                itemInfo = 'Remove Active Item'
                itemName = 'none'
                itemBooster = 0
                printItemInfo = []
                for i in range(7):
                    if len(itemInfo)>41:
                        printItemInfo.append(itemInfo[0:42])
                        itemInfo = itemInfo[42:]
                    if len(itemInfo)<=41:
                        printItemInfo.append(itemInfo)
                        break
                for i in range(len(printItemInfo)):
                    displaytextTL(printItemInfo[i],20,HEIGHT-150+i*35,white,font18)
                
            if itemName != 'none':
                if self.powerupLevel[itemNum]<len(itemLevelCosts[itemNum])-1:
                    displaytextTL(('Level '+str(self.powerupLevel[itemNum]+1)+' '+itemName),20,HEIGHT-180,white,font24)
                elif self.powerupLevel[itemNum]==len(itemLevelCosts[itemNum])-1:
                    displaytextTL(('Max level '+itemName),20,HEIGHT-180,white,font24)
                else:displaytextTL(('Max+ level '+itemName),20,HEIGHT-180,white,font24)
            else:
                displaytextTL(itemName,20,HEIGHT-180,white,font24)
                
            displaytextTL('Booster Points:',WIDTH-300,HEIGHT-180,white,font18)
            displaytextTL(str(itemBooster),WIDTH-30,HEIGHT-180,white,font18)
            displaytext('Booster Points Used:',WIDTH-400,HEIGHT/2+170,white,font24)
            displaytext(str(self.currentBooster)+'/'+str(self.boosterValue),WIDTH-60,HEIGHT/2+170,white,font24)
            
            change,select = events(6)
            index2+=change
            if index2>len(self.purchasedItems):
                index2=0
            if index2<0:
                index2=len(self.purchasedItems)
            if select != 0:
                if index2>0:
                    selectedItem = self.purchasedItems[index2-1]
                else: selectedItem = 'none'
                
                while True:
                    pressed = py.key.get_pressed()
                    if pressed[py.K_ESCAPE]:
                        break
                    clock.tick(FPS)
                    screen.fill(black)
                    displaytext("Inventory",WIDTH/2,50,white,font24)
                    displaytextTL('Press escape to leave',10,10,white,font18)
                    py.draw.rect(screen, white,[WIDTH/2-116,120,66,66],2)
                    py.draw.rect(screen, white,[WIDTH/2-16,120,66,66],2)
                    py.draw.rect(screen, white,[WIDTH/2+84,120,66,66],2)
                    for i in range(len(self.equipedItems)):
                        if self.equipedItems[i]!= 'none':
                            screen.blit(self.equipedItems[i],(WIDTH/2-114+100*i,122))
                    for i in range(3-self.unlockedSlots):
                        screen.blit(self.lockedSlot,(WIDTH/2+85-i*100,121))
                        
                    py.draw.rect(screen,white,(100,200,WIDTH-200,300),3)
                        
                    for i in range(len(self.purchasedItems)+1):
                        if i != 0:
                            if i <6:
                                screen.blit(self.purchasedItems[i-1],(150+i*127,232))
                            else: screen.blit(self.purchasedItems[i-1],(150+(i-6)*127,382))
                            
                    py.draw.rect(screen, white, (WIDTH/2-84+changeIndex*100,110,6,6),5)
                    if index2<6:
                        py.draw.rect(screen, white, (148+index2*127,230,68,68),2)
                    else:
                        py.draw.rect(screen, white, (148+(index2-6)*127,380,68,68),2)
                    
                    if index2!=0 and len(self.purchasedItems)>0:
                        if self.purchasedItems[index2-1] == self.heartPowerup:
                            itemNum = 0
                        if self.purchasedItems[index2-1] == self.speedPowerup:
                            itemNum = 1
                        if self.purchasedItems[index2-1] == self.shootingPowerup:
                            itemNum = 2
                        if self.purchasedItems[index2-1] == self.meleePowerup:
                            itemNum = 3
                        if self.purchasedItems[index2-1] == self.valentinesPowerup:
                            itemNum = 4
                        if self.purchasedItems[index2-1] == self.quickPowerup:
                            itemNum = 5
                        if self.purchasedItems[index2-1] == self.steelPowerup:
                            itemNum = 6
                        if self.purchasedItems[index2-1] == self.firePowerup:
                            itemNum = 7
                        if self.purchasedItems[index2-1] == self.C4Powerup:
                            itemNum = 8
                        if self.purchasedItems[index2-1] == self.blockPowerup:
                            itemNum = 9
                        if self.purchasedItems[index2-1] == self.deanPowerup:
                            itemNum = 10


                        if self.powerupLevel[itemNum]<len(itemLevelCosts[itemNum]):
                            itemInfo = itemLevelText[itemNum][self.powerupLevel[itemNum]]
                        else:
                            itemInfo = itemLevelText[itemNum][self.powerupLevel[itemNum]-1]
                            itemInfoBonus = itemEnhanceTextMod[itemNum]
                        itemName = itemNames[itemNum]

                        if self.powerupLevel[itemNum]<(len(itemLevelCosts[itemNum])-1):
                            printItemInfo = []
                            for i in range(7):
                                if len(itemInfo)>37:
                                    printItemInfo.append(itemInfo[0:38])
                                    itemInfo = itemInfo[38:]
                                if len(itemInfo)<=37:
                                    printItemInfo.append(itemInfo)
                                    break
                            for i in range(len(printItemInfo)):
                                displaytextTL(printItemInfo[i],100,HEIGHT-150+i*25,white,font18)
                            
                        elif self.powerupLevel[itemNum]==(len(itemLevelCosts[itemNum])-1):
                            printItemInfo = []
                            for i in range(7):
                                if len(itemInfo)>37:
                                    printItemInfo.append(itemInfo[0:38])
                                    itemInfo = itemInfo[38:]
                                if len(itemInfo)<=37:
                                    printItemInfo.append(itemInfo)
                                    break
                            for i in range(len(printItemInfo)):
                                displaytextTL(printItemInfo[i],100,HEIGHT-150+i*25,white,font18)
                        else:
                            if itemNum !=5 and itemNum != 8:
                                printItemInfo = []
                                for i in range(7):
                                    if len(itemInfo)>37:
                                        printItemInfo.append(itemInfo[0:38])
                                        itemInfo = itemInfo[38:]
                                    if len(itemInfo)<=37:
                                        printItemInfo.append(itemInfo)
                                        break
                                for i in range(len(printItemInfo)):
                                    displaytextTL(printItemInfo[i],100,HEIGHT-70+i*25,white,font18)
                            printItemInfo = []
                            for i in range(7):
                                if len(itemInfoBonus)>37:
                                    printItemInfo.append(itemInfoBonus[0:38])
                                    itemInfoBonus = itemInfoBonus[38:]
                                if len(itemInfoBonus)<=37:
                                    printItemInfo.append(itemInfoBonus)
                                    break
                            for i in range(len(printItemInfo)):
                                displaytextTL(printItemInfo[i],100,HEIGHT-150+i*25,white,font18)
                       
                        itemBooster = itemValues[itemNum]
                    if index2 == 0:
                        itemInfo = 'Remove Active Item'
                        itemName = 'none'
                        itemBooster = 0
                        printItemInfo = []
                        for i in range(7):
                            if len(itemInfo)>41:
                                printItemInfo.append(itemInfo[0:42])
                                itemInfo = itemInfo[42:]
                            if len(itemInfo)<=41:
                                printItemInfo.append(itemInfo)
                                break
                        for i in range(len(printItemInfo)):
                            displaytextTL(printItemInfo[i],20,HEIGHT-150+i*35,white,font18)
                        
                    if itemName != 'none':
                        if self.powerupLevel[itemNum]<len(itemLevelCosts[itemNum])-1:
                            displaytextTL(('Level '+str(self.powerupLevel[itemNum]+1)+' '+itemName),20,HEIGHT-180,white,font24)
                        elif self.powerupLevel[itemNum]==len(itemLevelCosts[itemNum])-1:
                            displaytextTL(('Max level '+itemName),20,HEIGHT-180,white,font24)
                        else:displaytextTL(('Max+ level '+itemName),20,HEIGHT-180,white,font24)
                    else:
                        displaytextTL(itemName,20,HEIGHT-180,white,font24)
                    
                    displaytextTL('Booster Points:',WIDTH-300,HEIGHT-180,white,font18)
                    displaytextTL(str(itemBooster),WIDTH-30,HEIGHT-180,white,font18)
                    displaytext('Booster Points Used:',WIDTH-400,HEIGHT/2+170,white,font24)
                    displaytext(str(self.currentBooster)+'/'+str(self.boosterValue),WIDTH-60,HEIGHT/2+170,white,font24)

                    equipedHover = self.equipedItems[changeIndex]
                    if equipedHover == self.heartPowerup:
                        removedBooster = itemValues[0]
                    elif equipedHover == self.speedPowerup:
                        removedBooster = itemValues[1]
                    elif equipedHover == self.shootingPowerup:
                        removedBooster = itemValues[2]
                    elif equipedHover == self.meleePowerup:
                        removedBooster = itemValues[3]
                    elif equipedHover == self.valentinesPowerup:
                        removedBooster = itemValues[4]
                    elif equipedHover == self.quickPowerup:
                        removedBooster = itemValues[5]
                    elif equipedHover == self.steelPowerup:
                        removedBooster = itemValues[6]
                    elif equipedHover == self.firePowerup:
                        removedBooster = itemValues[7]
                    elif equipedHover == self.C4Powerup:
                        removedBooster = itemValues[8]
                    elif equipedHover == self.blockPowerup:
                        removedBooster = itemValues[9]
                    elif equipedHover == self.deanPowerup:
                        removedBooster = itemValues[10]
                    else: removedBooster = 0
                    if self.currentBooster + itemBooster - removedBooster > self.boosterValue:
                        displaytext('Too many booster Points',WIDTH/2,HEIGHT/2+60,white,font30)
                        
                    change,select = events(6)
                    changeIndex+=change
                    if changeIndex>=self.unlockedSlots:
                        changeIndex=0
                    if changeIndex<0:
                        changeIndex=self.unlockedSlots-1
                    if select != 0:
                        self.currentBooster += itemBooster
                        self.currentBooster -= removedBooster
                        if self.currentBooster<=self.boosterValue:
                            if selectedItem != 'none':
                                self.purchasedItems.remove(selectedItem)
                                
                            if self.equipedItems[changeIndex]!='none':
                                if self.equipedItems[changeIndex] == self.heartPowerup:
                                    self.hearts -=1
                                    if self.healthLeft > self.hearts*4:
                                        self.healthLeft = self.hearts*4
                                    if self.powerupLevel[0] >=1:
                                        self.hearts -=1
                                        if self.healthLeft > self.hearts*4:
                                            self.healthLeft = self.hearts*4
                                    if self.powerupLevel[0]>=3:
                                        self.hearts -=1
                                        if self.healthLeft>self.hearts*4:
                                            self.healthLeft = self.hearts*4
                                            
                                if self.equipedItems[changeIndex] == self.quickPowerup:
                                    if self.powerupLevel[5] == 0:
                                        leftAmount = .90
                                    if self.powerupLevel[5] == 1:
                                        leftAmount = .85
                                    if self.powerupLevel[5] == 2:
                                        leftAmount = .80
                                    if self.powerupLevel[5] == 3:
                                        leftAmount = .75
                                    if self.powerupLevel[5] == 4:
                                        leftAmount = .70
                                    if self.powerupLevel[5] == 5:
                                        leftAmount = .55
                                    for i in range(len(self.bulletTime)):
                                        self.bulletTime[i] = self.bulletTime[i]/leftAmount
                                        
                                if self.equipedItems[changeIndex] == self.steelPowerup:
                                    if self.powerupLevel[6] == 0:
                                        self.speedPercent +=.4
                                    if self.powerupLevel[6] == 1:
                                        self.speedPercent +=.35
                                    if self.powerupLevel[6] == 2:
                                        self.speedPercent +=.3
                                    if self.powerupLevel[6] == 3:
                                        self.speedPercent +=.2
                                    if self.powerupLevel[6] == 4 or self.powerupLevel[6] == 5:
                                        self.speedPercent +=.1
                                if self.equipedItems[changeIndex] == self.firePowerup:
                                    self.createFire = 30
                                self.purchasedItems.append(self.equipedItems[changeIndex])
                            self.equipedItems[changeIndex] = selectedItem
                            if selectedItem == self.heartPowerup:
                                self.hearts +=1
                                if self.powerupLevel[0] >=1:
                                    self.hearts +=1
                                if self.powerupLevel[0]>=3:
                                    self.hearts +=1
                            if selectedItem == self.quickPowerup:
                                if self.powerupLevel[5] == 0:
                                    leftAmount = .90
                                if self.powerupLevel[5] == 1:
                                    leftAmount = .85
                                if self.powerupLevel[5] == 2:
                                    leftAmount = .80
                                if self.powerupLevel[5] == 3:
                                    leftAmount = .75
                                if self.powerupLevel[5] == 4:
                                    leftAmount = .70
                                if self.powerupLevel[5] == 5:
                                    leftAmount = .55
                                for i in range(len(self.bulletTime)):
                                    self.bulletTime[i] = self.bulletTime[i]*leftAmount
                            if selectedItem == self.steelPowerup:
                                if self.powerupLevel[6] == 0:
                                    self.speedPercent -=.4
                                if self.powerupLevel[6] == 1:
                                    self.speedPercent -=.35
                                if self.powerupLevel[6] == 2:
                                    self.speedPercent -=.3
                                if self.powerupLevel[6] == 3:
                                    self.speedPercent -=.2
                                if self.powerupLevel[6] == 4 or self.powerupLevel[6] == 5:
                                    self.speedPercent -=.1
                            if selectedItem == self.C4Powerup:
                                self.C4Hits = 0
                            index2 = 0
                            break
                        else:
                            self.currentBooster -= itemBooster
                            self.currentBooster += removedBooster
                    py.display.flip()
                    
            py.display.flip()

    def shop(self):
        index2 = 0
        changeIndex = 0
        escapeTimer = 0
        #the shop menu
        while True:
            pressed = py.key.get_pressed()
            if pressed[py.K_ESCAPE]:
                escapeTimer +=1
            else: escapeTimer = 0
            if escapeTimer >7:
                break
            clock.tick(FPS)
            screen.fill(black)
            displaytext("WELCOME TO THE Powerup SHOP!",WIDTH/2,100,white,font24)
            displaytextTL('Press escape to leave',10,10,white,font18)
            displaytext('To Equip purchased Items enter your',WIDTH/2,160,white,font24)
            displaytext('inventory through the pause menu',WIDTH/2,200,white,font24)

            for i in range(len(self.forSaleItems)):
                screen.blit(self.forSaleItems[i],(150+i*75,HEIGHT/2))
                
            if len(self.forSaleItems)>0:
                py.draw.rect(screen, white, (182+index2*75,HEIGHT/2-12,6,6),5)
                py.draw.rect(screen, white, (148+index2*75,HEIGHT/2-2,68,68),2)
                if self.forSaleItems[index2] == self.heartPowerup:
                    itemNum = 0
                if self.forSaleItems[index2] == self.speedPowerup:
                    itemNum = 1
                if self.forSaleItems[index2] == self.shootingPowerup:
                    itemNum = 2
                if self.forSaleItems[index2] == self.meleePowerup:
                    itemNum = 3
                if self.forSaleItems[index2] == self.valentinesPowerup:
                    itemNum = 4
                if self.forSaleItems[index2] == self.quickPowerup:
                    itemNum = 5
                if self.forSaleItems[index2] == self.steelPowerup:
                    itemNum = 6
                if self.forSaleItems[index2] == self.firePowerup:
                    itemNum = 7
                if self.forSaleItems[index2] == self.C4Powerup:
                    itemNum = 8
                if self.forSaleItems[index2] == self.blockPowerup:
                    itemNum = 9
                if self.forSaleItems[index2] == self.deanPowerup:
                    itemNum = 10
                itemBooster = itemValues[itemNum]
                itemCost = itemCosts[itemNum]
                itemInfo = itemDescriptions[itemNum]
                itemName = itemNames[itemNum]
            if len(self.forSaleItems)>0:
                printItemInfo = []
                for i in range(7):
                    if len(itemInfo)>41:
                        printItemInfo.append(itemInfo[0:42])
                        itemInfo = itemInfo[42:]
                    if len(itemInfo)<=41:
                        printItemInfo.append(itemInfo)
                        break
                for i in range(len(printItemInfo)):
                    displaytextTL(printItemInfo[i],20,HEIGHT-120+i*35,white,font18)
                displaytextTL('This item costs: ',20,HEIGHT-180,white,font24)
                displaytextTL(str(itemCost),WIDTH/2-100,HEIGHT-180,white,font24)
                displaytextTL(itemName,20,HEIGHT-250,white,font24)
                displaytextTL('Booster Points:',WIDTH-400,HEIGHT-200,white,font24)
                displaytextTL(str(itemBooster),WIDTH-30,HEIGHT-200,white,font24)
            else: displaytext('NO available items!',WIDTH/2,HEIGHT/2,white,font30)

            screen.blit(self.mbag,(WIDTH-263,27))
            displaytext(':',WIDTH-200,50,white,font24)
            displaytext(str(self.totalGold),WIDTH-90,50,white,font24)
            
            change,select = events(5)
            index2+=change
            if index2>len(self.forSaleItems)-1 and len(self.forSaleItems)>0:
                index2=0
            if index2<0:
                index2=len(self.forSaleItems)-1
            if select != 0 and len(self.forSaleItems)>0:
                selectedItem = self.forSaleItems[index2]
                
                while True:
                    sectionNotTrue = False
                    pressed = py.key.get_pressed()
                    if pressed[py.K_ESCAPE]:
                        break
                    for event in py.event.get():
                        if event.type == py.QUIT:
                            py.quit()
                            py.mixer.quit()
                            sys.exit()
                        if event.type == py.KEYDOWN and event.key == py.K_RETURN:
                            if self.totalGold>=itemCost:
                                self.forSaleItems.remove(selectedItem)
                                self.purchasedItems.append(selectedItem)
                                self.totalGold = int(self.totalGold-itemCost)
                                sectionNotTrue = True
                    if sectionNotTrue:
                        index2 = 0
                        break
                    clock.tick(FPS)
                    screen.fill(black)
                    displaytext("WELCOME TO THE Bullet SHOP!",WIDTH/2,100,white,font24)
                    displaytext('To Purchase press \'enter\'',WIDTH/2,200,white,font18)
                    displaytext('To go back press \'escape\'',WIDTH/2,240,white,font18)
                    
                    screen.blit(selectedItem,(WIDTH/2,HEIGHT/2))
                    
                    if self.forSaleItems[index2] == self.heartPowerup:
                        itemNum = 0
                    if self.forSaleItems[index2] == self.speedPowerup:
                        itemNum = 1
                    if self.forSaleItems[index2] == self.shootingPowerup:
                        itemNum = 2
                    if self.forSaleItems[index2] == self.meleePowerup:
                        itemNum = 3
                    if self.forSaleItems[index2] == self.valentinesPowerup:
                        itemNum = 4
                    if self.forSaleItems[index2] == self.quickPowerup:
                        itemNum = 5
                    if self.forSaleItems[index2] == self.steelPowerup:
                        itemNum = 6
                    if self.forSaleItems[index2] == self.firePowerup:
                        itemNum = 7
                    if self.forSaleItems[index2] == self.C4Powerup:
                        itemNum = 8
                    if self.forSaleItems[index2] == self.blockPowerup:
                        itemNum = 9
                    if self.forSaleItems[index2] == self.deanPowerup:
                        itemNum = 10
                    itemBooster = itemValues[itemNum]
                    itemCost = itemCosts[itemNum]
                    itemInfo = itemDescriptions[itemNum]
                    itemName = itemNames[itemNum]

                    printItemInfo = []
                    for i in range(7):
                        if len(itemInfo)>41:
                            printItemInfo.append(itemInfo[0:42])
                            itemInfo = itemInfo[42:]
                        if len(itemInfo)<=41:
                            printItemInfo.append(itemInfo)
                            break

                    screen.blit(self.mbag,(WIDTH-263,27))
                    displaytext(':',WIDTH-200,50,white,font24)
                    displaytext(str(self.totalGold),WIDTH-90,50,white,font24)
                    
                    for i in range(len(printItemInfo)):
                        displaytextTL(printItemInfo[i],20,HEIGHT-120+i*35,white,font18)
                    displaytextTL('This item costs: ',20,HEIGHT-180,white,font24)
                    displaytextTL(str(itemCost),WIDTH/2-100,HEIGHT-180,white,font24)
                    displaytextTL(itemName,20,HEIGHT-250,white,font24)
                    displaytextTL('Booster Points:',WIDTH-400,HEIGHT-200,white,font24)
                    displaytextTL(str(itemBooster),WIDTH-30,HEIGHT-200,white,font24)
                    if self.totalGold<itemCost:
                        displaytext('not enough money to purchase!',WIDTH/2,HEIGHT-300,white,font24)
                    
                    py.display.flip()
                    
            py.display.flip()

    def bulletshop(self):
        index2 = 0
        changeIndex = 0
        escapeTimer = 0
        #the shop menu
        while True:
            pressed = py.key.get_pressed()
            if pressed[py.K_ESCAPE]:
                escapeTimer +=1
            else: escapeTimer = 0
            if escapeTimer >7:
                break
            clock.tick(FPS)
            screen.fill(black)
            displaytext("WELCOME TO THE bullet SHOP!",WIDTH/2,100,white,font24)
            displaytextTL('Press escape to leave',10,10,white,font18)
            displaytext('To Equip purchased Items enter the',WIDTH/2,160,white,font24)
            displaytext('bullets menu through the pause menu',WIDTH/2,200,white,font24)

            for i in range(len(self.forSaleBullets)):
                screen.blit(self.forSaleBullets[i],(150+i*75,HEIGHT/2))
                
            if len(self.forSaleBullets)>0:
                py.draw.rect(screen, white, (182+index2*75,HEIGHT/2-12,6,6),5)
                py.draw.rect(screen, white, (148+index2*75,HEIGHT/2-2,68,68),2)
                if self.forSaleBullets[index2] == self.dualBullet:
                    itemNum = 1
                if self.forSaleBullets[index2] == self.snowBullet:
                    itemNum = 2
                if self.forSaleBullets[index2] == self.sniperBullet:
                    itemNum = 3
                if self.forSaleBullets[index2] == self.antiBullet:
                    itemNum = 4
                if self.forSaleBullets[index2] == self.batteryBullet:
                    itemNum = 5
                
                itemCost = bulletCosts[itemNum]
                itemInfo = bulletDescriptions[itemNum]
                itemName = bulletNames[itemNum]
            if len(self.forSaleBullets)>0:
                printItemInfo = []
                for i in range(7):
                    if len(itemInfo)>41:
                        printItemInfo.append(itemInfo[0:42])
                        itemInfo = itemInfo[42:]
                    if len(itemInfo)<=41:
                        printItemInfo.append(itemInfo)
                        break
                for i in range(len(printItemInfo)):
                    displaytextTL(printItemInfo[i],20,HEIGHT-120+i*35,white,font18)
                displaytextTL('This item costs: ',20,HEIGHT-180,white,font24)
                displaytextTL(str(itemCost),WIDTH/2-100,HEIGHT-180,white,font24)
                displaytextTL(itemName,20,HEIGHT-250,white,font24)
            else: displaytext('NO available items!',WIDTH/2,HEIGHT/2,white,font30)

            displaytextTL(bulletUsage[itemNum]+' bullets per shot',WIDTH/2+100,HEIGHT-250,white,font18)
                
            screen.blit(self.mbag,(WIDTH-263,27))
            displaytext(':',WIDTH-200,50,white,font24)
            displaytext(str(self.totalGold),WIDTH-90,50,white,font24)
            
            change,select = events(5)
            index2+=change
            if index2>len(self.forSaleBullets)-1 and len(self.forSaleBullets)>0:
                index2=0
            if index2<0:
                index2=len(self.forSaleBullets)-1
            if select != 0 and len(self.forSaleBullets)>0:
                selectedItem = self.forSaleBullets[index2]
                
                while True:
                    sectionNotTrue = False
                    pressed = py.key.get_pressed()
                    if pressed[py.K_ESCAPE]:
                        sectionNotTrue = True
                    for event in py.event.get():
                        if event.type == py.QUIT:
                            py.quit()
                            py.mixer.quit()
                            sys.exit()
                        if event.type == py.KEYDOWN and event.key == py.K_RETURN:
                            if self.totalGold>=itemCost:
                                self.forSaleBullets.remove(selectedItem)
                                self.purchasedBullets.append(selectedItem)
                                self.totalGold = int(self.totalGold-itemCost)
                                sectionNotTrue = True
                                if selectedItem == self.dualBullet:
                                    self.orderedBullets[1] = self.dualBullet
                                    
                                if selectedItem == self.batteryBullet:
                                    self.orderedBullets[2] = self.batteryBullet
                                    
                                if selectedItem == self.sniperBullet:
                                    self.orderedBullets[3] = self.sniperBullet
                                    
                                if selectedItem == self.antiBullet:
                                    self.orderedBullets[5] = self.antiBullet
                                    
                    if sectionNotTrue:
                        index2 = 0
                        break
                    clock.tick(FPS)
                    screen.fill(black)
                    displaytext("WELCOME TO THE bullet SHOP!",WIDTH/2,100,white,font24)
                    displaytext('To Purchase press \'enter\'',WIDTH/2,200,white,font18)
                    displaytext('To go back press \'escape\'',WIDTH/2,240,white,font18)
                    
                    screen.blit(selectedItem,(WIDTH/2,HEIGHT/2))
                    
                    if self.forSaleBullets[index2] == self.dualBullet:
                        itemNum = 1
                    if self.forSaleBullets[index2] == self.snowBullet:
                        itemNum = 2
                    if self.forSaleBullets[index2] == self.sniperBullet:
                        itemNum = 3
                    if self.forSaleBullets[index2] == self.antiBullet:
                        itemNum = 4
                    if self.forSaleBullets[index2] == self.batteryBullet:
                        itemNum = 5
                    
                    itemCost = bulletCosts[itemNum]
                    itemInfo = bulletDescriptions[itemNum]
                    itemName = bulletNames[itemNum]

                    printItemInfo = []
                    for i in range(7):
                        if len(itemInfo)>41:
                            printItemInfo.append(itemInfo[0:42])
                            itemInfo = itemInfo[42:]
                        if len(itemInfo)<=41:
                            printItemInfo.append(itemInfo)
                            break
                    for i in range(len(printItemInfo)):
                        displaytextTL(printItemInfo[i],20,HEIGHT-120+i*35,white,font18)
                    displaytextTL('This item costs: ',20,HEIGHT-180,white,font24)
                    displaytextTL(str(itemCost),WIDTH/2-100,HEIGHT-180,white,font24)
                    displaytextTL(itemName,20,HEIGHT-250,white,font24)
                    if self.totalGold<itemCost:
                        displaytext('not enough money to purchase!',WIDTH/2,HEIGHT-300,white,font24)
                        
                    displaytextTL(bulletUsage[itemNum]+' bullets per shot',WIDTH/2+100,HEIGHT-250,white,font18)
                    screen.blit(self.mbag,(WIDTH-263,27))
                    displaytext(':',WIDTH-200,50,white,font24)
                    displaytext(str(self.totalGold),WIDTH-90,50,white,font24)
                    
                    py.display.flip()
                    
            py.display.flip()
        
    def saveMenu(self):
        index = 0
        while True:#automatically starts in title screen
            clock.tick(FPS)
            py.draw.rect(screen,black,(WIDTH/2-200,200,400,200))
            py.draw.rect(screen,white,(WIDTH/2-205,195,410,210),10)
            #draw 5 buttons for: new game, continue, how to play, settings and exit
            screen.blit(savebutton1,saverect_1)
            screen.blit(savebutton2,saverect_2)
            
            py.draw.rect(screen, white, [saverectsList[index].x - 30,(saverectsList[index].centery-3),6,6],5)
            #check events
            change,select = events(1)
            index +=change
            #making sure the selector stays in range
            if index >1:
                index = 0
            if index < 0:
                index = 1
            #when you select, determining what to do
            if select !=0:
                if index ==0:
                    file = open(path.join(text_folder,'gameStat.txt'),'w')
                    file.write(str(self.totalGold)+'\n')
                    file.write(str(self.hearts)+'\n')
                    file.write(str(self.unlocked)+'\n')
                    itemstuff = [self.purchasedItems,self.equipedItems,self.forSaleItems,self.notYetForSaleItems,self.equipedBullet,self.purchasedBullets,
                                 self.forSaleBullets,self.notYetForSaleBullets,self.orderedBullets]
                    for i1 in range(len(itemstuff)):
                        for i in range(len(itemstuff[i1])):
                            if itemstuff[i1][i] == 'none':
                                itemstuff[i1][i] = '\'none\''
                            if itemstuff[i1][i] == self.heartPowerup:
                                itemstuff[i1][i] = 'self.heartPowerup'
                            if itemstuff[i1][i] == self.speedPowerup:
                                itemstuff[i1][i] = 'self.speedPowerup'
                            if itemstuff[i1][i] == self.meleePowerup:
                                itemstuff[i1][i] = 'self.meleePowerup'
                            if itemstuff[i1][i] == self.shootingPowerup:
                                itemstuff[i1][i] = 'self.shootingPowerup'
                            if itemstuff[i1][i] == self.valentinesPowerup:
                                itemstuff[i1][i] = 'self.valentinesPowerup'
                            if itemstuff[i1][i] == self.steelPowerup:
                                itemstuff[i1][i] = 'self.steelPowerup'
                            if itemstuff[i1][i] == self.quickPowerup:
                                itemstuff[i1][i] = 'self.quickPowerup'
                            if itemstuff[i1][i] == self.firePowerup:
                                itemstuff[i1][i] = 'self.firePowerup'
                            if itemstuff[i1][i] == self.C4Powerup:
                                itemstuff[i1][i] = 'self.C4Powerup'
                            if itemstuff[i1][i] == self.deanPowerup:
                                itemstuff[i1][i] = 'self.deanPowerup'
                            if itemstuff[i1][i] == self.blockPowerup:
                                itemstuff[i1][i] = 'self.blockPowerup'
                            if itemstuff[i1][i] == self.normalBullet:
                                itemstuff[i1][i] = 'self.normalBullet'
                            if itemstuff[i1][i] == self.dualBullet:
                                itemstuff[i1][i] = 'self.dualBullet'
                            if itemstuff[i1][i] == self.snowBullet:
                                itemstuff[i1][i] = 'self.snowBullet'
                            if itemstuff[i1][i] == self.sniperBullet:
                                itemstuff[i1][i] = 'self.sniperBullet'
                            if itemstuff[i1][i] == self.antiBullet:
                                itemstuff[i1][i] = 'self.antiBullet'
                            if itemstuff[i1][i] == self.batteryBullet:
                                itemstuff[i1][i] = 'self.batteryBullet'
                            if itemstuff[i1][i] == 0:
                                itemstuff[i1][i] = '0'
                    for i in itemstuff:
                        i = ','.join(i)
                        file.write(i+'\n')
                    file.write(str(self.unlockedSlots)+'\n')
                    file.write(str(self.boosterValue)+'\n')
                    file.write(str(self.currentBooster)+'\n')
                    file.write(str(self.talkedToDean)+'\n')
                    for i in range(len(self.bagsStolen)):
                        self.bagsStolen[i] = str(self.bagsStolen[i])
                    x = ','.join(self.bagsStolen)
                    file.write(x+'\n')
                    for i in range(len(self.bagsStolen)):
                        self.bagsStolen[i] = int(self.bagsStolen[i])
                        
                    for i in range(len(self.bulletTime)):
                        self.bulletTime[i] = str(self.bulletTime[i])
                    x = ','.join(self.bulletTime)
                    file.write(x+'\n')
                    for i in range(len(self.bulletTime)):
                        self.bulletTime[i] = float(self.bulletTime[i])

                    for i in range(len(self.bulletLevel)):
                        self.bulletLevel[i] = str(self.bulletLevel[i])
                    x = ','.join(self.bulletLevel)
                    file.write(x+'\n')
                    for i in range(len(self.bulletLevel)):
                        self.bulletLevel[i] = int(self.bulletLevel[i])

                    for i in range(len(self.powerupLevel)):
                        self.powerupLevel[i] = str(self.powerupLevel[i])
                    x = ','.join(self.powerupLevel)
                    file.write(x+'\n')
                    for i in range(len(self.powerupLevel)):
                        self.powerupLevel[i] = int(self.powerupLevel[i])
                    file.write(self.mode+'\n')
                    file.close()
                    for i1 in range(len(itemstuff)):
                        for i in range(len(itemstuff[i1])):
                            if itemstuff[i1][i] == '\'none\'':
                                itemstuff[i1][i] = 'none'
                            elif itemstuff[i1][i] == 'self.heartPowerup':
                                itemstuff[i1][i] = self.heartPowerup
                            elif itemstuff[i1][i] == 'self.speedPowerup':
                                itemstuff[i1][i] = self.speedPowerup
                            elif itemstuff[i1][i] == 'self.meleePowerup':
                                itemstuff[i1][i] = self.meleePowerup
                            elif itemstuff[i1][i] == 'self.shootingPowerup':
                                itemstuff[i1][i] = self.shootingPowerup
                            elif itemstuff[i1][i] == 'self.valentinesPowerup':
                                itemstuff[i1][i] = self.valentinesPowerup
                            elif itemstuff[i1][i] == 'self.steelPowerup':
                                itemstuff[i1][i] = self.steelPowerup
                            elif itemstuff[i1][i] == 'self.quickPowerup':
                                itemstuff[i1][i] = self.quickPowerup
                            elif itemstuff[i1][i] == 'self.firePowerup':
                                itemstuff[i1][i] = self.firePowerup
                            elif itemstuff[i1][i] == 'self.C4Powerup':
                                itemstuff[i1][i] = self.C4Powerup
                            elif itemstuff[i1][i] == 'self.blockPowerup':
                                itemstuff[i1][i] = self.blockPowerup
                            elif itemstuff[i1][i] == 'self.deanPowerup':
                                itemstuff[i1][i] = self.deanPowerup
                            elif itemstuff[i1][i] == 'self.normalBullet':
                                itemstuff[i1][i] = self.normalBullet
                            elif itemstuff[i1][i] == 'self.dualBullet':
                                itemstuff[i1][i] = self.dualBullet
                            elif itemstuff[i1][i] == 'self.snowBullet':
                                itemstuff[i1][i] = self.snowBullet
                            elif itemstuff[i1][i] == 'self.sniperBullet':
                                itemstuff[i1][i] = self.sniperBullet
                            elif itemstuff[i1][i] == 'self.antiBullet':
                                itemstuff[i1][i] = self.antiBullet
                            elif itemstuff[i1][i] == 'self.batteryBullet':
                                itemstuff[i1][i] = self.batteryBullet
                            elif itemstuff[i1][i] == '0':
                                itemstuff[i1][i] = 0
                            else: itemstuff[i1] = []
                    break
                if index == 1:
                    break
            py.display.flip()
    
    def printText(self,openFile,black = False):#print text from file/npcs standard talking
        try:
            self.player.vel.x = 0
            self.player.animate()
            self.draw()
        except AttributeError:
            pass
        try:
            with open(path.join(text_folder,openFile),'r') as file:
                all_lines = file.readlines()
        except:
            all_lines = [openFile]
        for line in all_lines:
             print_text_topleft(line,black)
            
                
def print_text_topleft(string, black):
    global jumpKey
    letter = 0  # Index of string 
    text_section = 1  # used for while true loop
    counter = 4  # frames to print a single letter
    counter2 = 20
    output_text = ""  # First string of text
    output_text2 = "" # second string of text
    output_text3 = "" # third string of text
    text = list(string)
    try:
        g.player.canMove = False  # Replace this with what you want. This is to prevent movement while talking
        g.player.update()  # Update the player only once to look natural
    except: pass
    temp_surface = pygame.Surface((WIDTH,120))  # temporary surface
    canExit = False
    while text_section == 1:
        clock.tick(FPS)  # Tick at normal framerate
        if counter > 0:  # Counter for when to print each letter
            counter -= 1
        else:
            counter = 1  # Resets counter
            if text[letter] == "^":
                del text[letter]
                counter = 24
            elif text[letter] == "~":
                del text[letter]
                remaining_text = "".join(text[letter+1:])
                return print_text_topleft(remaining_text,black)
            elif text[letter] == "`":
                del text[letter]
                remaining_text = "".join(text[letter+1:])
                text_section = 2
            else:
                if letter <= 41:
                    output_text += text[letter]  # prints to first line
                elif letter > 41:
                    if letter > 82:
                        output_text3 += text[letter]  # prints to second
                    else:
                        output_text2 += text[letter]  # prints to third
                
                if letter == len(text) - 1:  # End of string
                    text_section = 2
                else:
                    letter += 1
	# Update section
        temp_surface.fill((0,0,0))
        screen.fill((0,0,0))
        message, rect = font24.render(output_text, (255,255,255))  # Gamefont is a font with a size of 24
        message2, rect2 = font24.render(output_text2, (255,255,255))
        message3, rect3 = font24.render(output_text3, (255,255,255))
        rect.topleft = (20,10)
        rect2.topleft = (20,50)
        rect3.topleft = (20,90) 
        temp_surface.blit(message,rect)  # All strings are drawn to the screen
        temp_surface.blit(message2,rect2)
        temp_surface.blit(message3,rect3)
        for i in g.bossenemies:
            i.animate()
        try:#draw everything to screen if the player is in level
            if not black:
                screen.blit(g.map[g.area][g.openTo][1],g.mapTL)
                g.all_sprites.remove(g.player)
                for i in g.otherImg:
                    g.all_sprites.remove(i)
                for i in g.doors:
                    g.all_sprites.remove(i)
                g.all_sprites.draw(screen)
                for e in g.enemies:  
                    if e.newAlert:
                        e.newAlertTimer +=1
                        if e.newAlertTimer==35:
                            e.newAlertTimer = 0
                            e.newAlert = False
                        screen.blit(g.exclamationMark[0],(e.rect.x,e.rect.y-64))
                for i in g.otherImg:
                    g.all_sprites.add(i)
                g.otherImg.draw(screen)
                for i in g.doors:
                    if i.direction == 'right':
                        curImg = i.image.get_rect()
                        screen.blit(i.image,(i.rect.x-curImg.width+15,i.rect.y))
                    else:
                        screen.blit(i.image,(i.rect.x,i.rect.y))
                    g.all_sprites.add(i)
                g.all_sprites.add(g.player)
                
                if g.player.direction == 1:
                    if not g.player.wallJump:
                        screen.blit(g.player.image,(g.player.rect.x-8,g.player.rect.y-20))
                    else:screen.blit(g.player.image,(g.player.rect.x,g.player.rect.y-20))
                else:
                    if not g.player.wallJump:
                        screen.blit(g.player.image,(g.player.rect.x-24,g.player.rect.y-20))
                    else: screen.blit(g.player.image,(g.player.rect.x,g.player.rect.y-20))
                
                g.otherImg.draw(screen)
        except: pass
        screen.blit(temp_surface, (0,0))  # The surface is drawn to the screen
        pygame.display.update()  # and the screen is updated
        #able to skip text printing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and (event.key == jumpKey or event.key == py.K_RETURN):  # If you come to a stop
                    while text_section == 1:
                        if letter <= 41:
                            output_text += text[letter]  # prints to first line
                        elif letter > 41:
                            if letter > 82:
                                output_text3 += text[letter]  # prints to second
                            else:
                                output_text2 += text[letter]  # prints to third
                        
                        if letter == len(text) - 1:  # End of string
                            text_section = 2
                        else:
                            letter += 1

    while text_section == 2:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and (event.key == jumpKey or event.key == py.K_RETURN)and canExit:  # If you come to a stop
                if letter == len(text) - 1:   # You exit the conversation
                    text_section = 3
                    try:
                        g.player.canMove = True
                    except: pass
                    
                else:
                    return print_text_topleft(remaining_text,black)  # or a new string is printed 
                    
        temp_surface.fill((0,0,0))
        screen.fill((0,0,0))
        if counter2 > 0:
            counter2 -= 1

        else:
            pygame.draw.rect(temp_surface, (255,255,255), [992, 95, 10, 10], 5)  # Draws button to indicate that you can continue
            canExit = True
            
        message, rect = font24.render(output_text, (255,255,255))  # Gamefont is a font with a size of 24
        message2, rect2 = font24.render(output_text2, (255,255,255))
        message3, rect3 = font24.render(output_text3, (255,255,255))
        rect.topleft = (20,10)
        rect2.topleft = (20,50)
        rect3.topleft = (20,90) 
        temp_surface.blit(message,rect)  # All strings are drawn to the screen
        temp_surface.blit(message2,rect2)
        temp_surface.blit(message3,rect3)
        for i in g.bossenemies:
            i.animate()
        try:#draw everything to the screen if the player is in level
            if not black:
                screen.blit(g.map[g.area][g.openTo][1],g.mapTL)
                g.all_sprites.remove(g.player)
                for i in g.otherImg:
                    g.all_sprites.remove(i)
                for i in g.doors:
                    g.all_sprites.remove(i)
                g.all_sprites.draw(screen)
                for e in g.enemies:  
                    if e.newAlert:
                        e.newAlertTimer +=1
                        if e.newAlertTimer==35:
                            e.newAlertTimer = 0
                            e.newAlert = False
                        screen.blit(g.exclamationMark[0],(e.rect.x,e.rect.y-64))
                for i in g.otherImg:
                    g.all_sprites.add(i)
                g.otherImg.draw(screen)
                for i in g.doors:
                    if i.direction == 'right':
                        curImg = i.image.get_rect()
                        screen.blit(i.image,(i.rect.x-curImg.width+15,i.rect.y))
                    else:
                        screen.blit(i.image,(i.rect.x,i.rect.y))
                    g.all_sprites.add(i)
                g.all_sprites.add(g.player)
                
                if g.player.direction == 1:
                    if not g.player.wallJump:
                        screen.blit(g.player.image,(g.player.rect.x-8,g.player.rect.y-20))
                    else:screen.blit(g.player.image,(g.player.rect.x,g.player.rect.y-20))
                else:
                    if not g.player.wallJump:
                        screen.blit(g.player.image,(g.player.rect.x-24,g.player.rect.y-20))
                    else: screen.blit(g.player.image,(g.player.rect.x,g.player.rect.y-20))
                
                g.otherImg.draw(screen)
        except: pass
        screen.blit(temp_surface, (0,0))  # The surface is drawn to the screen
        pygame.display.update()
            

def displaytext(text,x,y,color,fontR):
    #display text to screen
    rendering,text_rect = fontR.render(text,color)
    text_rect.center =(x,y)
    screen.blit(rendering,text_rect)

def displaytextTL(text,x,y,color,fontR):
    global font
    #display text to screen
    rendering,text_rect = fontR.render(text,color)
    text_rect.topleft =(x,y)
    screen.blit(rendering,text_rect)

def returnText(text,color,fontR):#used to return text with rect
    global font
    rendering,text_rect = fontR.render(text,color)
    return rendering,text_rect

def events(area):
    #this loop will contain all event checks, with variable area
    #controlling other checks needed for each individual need
    #depending on where loop is called
    a=0#for main menu, to see if update
    for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                py.mixer.quit()
                sys.exit()
                
            if area==1:#for main menu, button detection
                titleScreen = 1
                change = 0#change to index position
                if event.type == py.KEYDOWN and event.key == py.K_DOWN:
                    change = 1
                    selectSound.play()
                if event.type == py.KEYDOWN and event.key == py.K_UP:
                    change = -1
                    selectSound.play()
                if event.type == py.KEYDOWN and event.key == py.K_RETURN:
                    #for if player selects this option
                    #x is throwaway var, just to transer out of if statement
                    x=1
                else: x=0
                return change,x
            if area == 2:#for if screen needs to quit loop
                if event.type == py.KEYDOWN and event.key in pygameKeys:
                    return event.key
                elif event.type == py.KEYDOWN: return 1
            if area==5:#for main menu, button detection
                titleScreen = 1
                change = 0#change to index position
                if event.type == py.KEYDOWN and event.key == py.K_RIGHT:
                    change = 1
                    selectSound.play()
                if event.type == py.KEYDOWN and event.key == py.K_LEFT:
                    change = -1
                    selectSound.play()
                if event.type == py.KEYDOWN and event.key == py.K_RETURN:
                    #for if player selects this option
                    #x is throwaway var, just to transer out of if statement
                    x=1
                else: x=0
                return change,x
            if area==6:#for main menu, button detection
                titleScreen = 1
                change = 0#change to index position
                if event.type == py.KEYDOWN and event.key == py.K_RIGHT:
                    change = 1
                    selectSound.play()
                if event.type == py.KEYDOWN and event.key == py.K_LEFT:
                    change = -1
                    selectSound.play()
                if event.type == py.KEYDOWN and event.key == py.K_DOWN:
                    change = 6
                    selectSound.play()
                if event.type == py.KEYDOWN and event.key == py.K_UP:
                    change = -6
                    selectSound.play()
                if event.type == py.KEYDOWN and event.key == py.K_RETURN:
                    #for if player selects this option
                    #x is throwaway var, just to transer out of if statement
                    x=1
                else: x=0
                return change,x

    if (a == 0 and area==1) or (a==0 and area == 5) or (a == 0 and area == 6):
        return 0,0
    if area==2:
        return 0


def how_to_play():
    index2 = 0
    global jumpKey
    global shootKey
    global reloadKey
    global drawGunKey
    global moveLeftKey
    global moveRightKey
    global enterDoorKey
    global skillKey
    #this is the loop for the player changing what keys do what
    while True:
        clock.tick(FPS)
        screen.fill(black)
        displaytext("Change the keys for each command.",WIDTH/2,100,white,font30)
        displaytext('Select the key you wish to change,',WIDTH/2,140,white,font30)
        displaytext('Then press the new key.',WIDTH/2,180,white,font30)
        displaytext('You can also automatically switch your bullet ',WIDTH/2,HEIGHT-50,white,font18)
        displaytext('by pressing < or >',WIDTH/2,HEIGHT-25,white,font18)
        screen.blit(Sbutton1,Srect_1)
        screen.blit(Sbutton2,Srect_2)
        screen.blit(Sbutton3,Srect_3)
        screen.blit(Sbutton4,Srect_4)
        screen.blit(Sbutton5,Srect_5)
        screen.blit(Sbutton6,Srect_6)
        screen.blit(Sbutton7,Srect_7)
        screen.blit(Sbutton8,Srect_8)
        screen.blit(Sbutton9,Srect_9)
        for i in range(len(pygameKeys)):
            if jumpKey == pygameKeys[i]:
                screen.blit(returnText(pygameLetters[i],white,font24)[0],(WIDTH/2+40,Srect_1.y))
            if shootKey == pygameKeys[i]:
                screen.blit(returnText(pygameLetters[i],white,font24)[0],(WIDTH/2+40,Srect_2.y))
            if reloadKey == pygameKeys[i]:
                screen.blit(returnText(pygameLetters[i],white,font24)[0],(WIDTH/2+40,Srect_3.y))
            if drawGunKey == pygameKeys[i]:
                screen.blit(returnText(pygameLetters[i],white,font24)[0],(WIDTH/2+40,Srect_4.y))
            if moveLeftKey == pygameKeys[i]:
                screen.blit(returnText(pygameLetters[i],white,font24)[0],(WIDTH/2+40,Srect_5.y))
            if moveRightKey == pygameKeys[i]:
                screen.blit(returnText(pygameLetters[i],white,font24)[0],(WIDTH/2+40,Srect_6.y))
            if enterDoorKey == pygameKeys[i]:
                screen.blit(returnText(pygameLetters[i],white,font24)[0],(WIDTH/2+40,Srect_7.y))
            if skillKey == pygameKeys[i]:
                screen.blit(returnText(pygameLetters[i],white,font24)[0],(WIDTH/2+40,Srect_8.y))
        
        py.draw.rect(screen, white, [SrectsList[index2].x - 30,(Srect_1.centery-3)+(50*index2),6,6],5)
        change,select = events(1)
        index2+=change
        if index2>8:
            index2=0
        if index2<0:
            index2=8
        if select!=0:
            #changing the keys to what they want
            if index2 == 0:
                while True:
                    clock.tick(20)
                    newKey = events(2)
                    if newKey != 0:
                        if newKey != 1:
                            jumpKey = newKey
                        break
            if index2 == 1:
                while True:
                    clock.tick(20)
                    newKey = events(2)
                    if newKey != 0:
                        if newKey != 1:
                            shootKey = newKey
                        break
            if index2 == 2:
                while True:
                    clock.tick(20)
                    newKey = events(2)
                    if newKey != 0:
                        if newKey != 1:
                            reloadKey = newKey
                        break
            if index2 == 3:
                while True:
                    clock.tick(20)
                    newKey = events(2)
                    if newKey != 0:
                        if newKey != 1:
                            drawGunKey = newKey
                        break
            if index2 == 4:
                while True:
                    clock.tick(20)
                    newKey = events(2)
                    if newKey != 0:
                        if newKey != 1:
                            moveLeftKey = newKey
                        break
            if index2 == 5:
                while True:
                    clock.tick(20)
                    newKey = events(2)
                    if newKey != 0:
                        if newKey != 1:
                            moveRightKey = newKey
                        break
            if index2 == 6:
                while True:
                    clock.tick(20)
                    newKey = events(2)
                    if newKey != 0:
                        if newKey != 1:
                            enterDoorKey = newKey
                        break
            if index2 == 7:
                while True:
                    clock.tick(20)
                    newKey = events(2)
                    if newKey != 0:
                        if newKey != 1:
                            skillKey = newKey
                        break
            
            if index2 == 8:
                break
        py.display.flip()    

#initialize pygame, set game running to true
py.init()
py.mixer.init()
running=True


#find out how much needs to be visible for playable screen
screenInfo=py.display.Info()
screenW=screenInfo.current_w
screenH=screenInfo.current_h

#set up the actual display
screen = py.display.set_mode((WIDTH,HEIGHT),py.FULLSCREEN)

py.display.set_caption(TITLE)
clock = py.time.Clock()

#initializing all different font sizes that would be needed
font24 = py.freetype.SysFont(font,24)
font30 = py.freetype.SysFont(font,30)
font18 = py.freetype.SysFont(font,18)
font36 = py.freetype.SysFont(font,36)

#creating all the different buttons that will be needed in the level or title screen
button1,rect_1 = returnText('Start a new game',white,font24)
button2,rect_2 = returnText('Continue a game',white,font24)
button3,rect_3 = returnText('Settings',white,font24)
button4,rect_4 = returnText('Exit Game',white,font24)
rect_1.center = (WIDTH/2,250)
rect_2.center = (WIDTH/2,300)
rect_3.center = (WIDTH/2,350)
rect_4.center = (WIDTH/2,400)
rectsList = [rect_1,rect_2,rect_3,rect_4]

Dbutton1,Drect_1 = returnText('Retry Level',white,font24)
Dbutton2,Drect_2 = returnText('Go to Level Selector',white,font24)
Dbutton3,Drect_3 = returnText('Main Menu',white,font24)
Drect_1.center = (WIDTH/2,300)
Drect_2.center = (WIDTH/2,350)
Drect_3.center = (WIDTH/2,400)
DrectsList = [Drect_1,Drect_2,Drect_3]

Pbutton1,Prect_1 = returnText('Continue Game',white,font24)
Pbutton2,Prect_2 = returnText('Powerup Menu',white,font24)
Pbutton3,Prect_3 = returnText('Bullets Menu',white,font24)
Pbutton4,Prect_4 = returnText('Settings',white,font24)
Pbutton5,Prect_5 = returnText('Main Menu',white,font24)
Prect_1.center = (WIDTH/2,300)
Prect_2.center = (WIDTH/2,350)
Prect_3.center = (WIDTH/2,400)
Prect_4.center = (WIDTH/2,450)
Prect_5.center = (WIDTH/2,500)
PrectsList = [Prect_1,Prect_2,Prect_3,Prect_4,Prect_5]

Sbutton1,Srect_1 = returnText('Jump: ',white,font24)
Sbutton2,Srect_2 = returnText('Attacking: ',white,font24)
Sbutton3,Srect_3 = returnText('Reload: ',white,font24)
Sbutton4,Srect_4 = returnText('Draw Gun: ',white,font24)
Sbutton5,Srect_5 = returnText('Move Left: ',white,font24)
Sbutton6,Srect_6 = returnText('Move Right: ',white,font24)
Sbutton7,Srect_7 = returnText('Encounter Object: ',white,font24)
Sbutton8,Srect_8 = returnText('Use skill:',white,font24)
Sbutton9,Srect_9 = returnText('EXIT',white,font24)
Srect_1.topleft = (WIDTH/8,250)
Srect_2.topleft = (WIDTH/8,300)
Srect_3.topleft = (WIDTH/8,350)
Srect_4.topleft= (WIDTH/8,400)
Srect_5.topleft= (WIDTH/8,450)
Srect_6.topleft= (WIDTH/8,500)
Srect_7.topleft= (WIDTH/8,550)
Srect_8.topleft= (WIDTH/8,600)
Srect_9.topleft= (WIDTH/8,650)
SrectsList = [Srect_1,Srect_2,Srect_3,Srect_4,Srect_5,Srect_6,Srect_7,Srect_8,Srect_9]

Leavebutton1,Leaverect_1 = returnText('YES',white,font24)
Leavebutton2,Leaverect_2 = returnText('NO',white,font24)
Leaverect_1.center = (WIDTH/2-100,HEIGHT/2)
Leaverect_2.center = (WIDTH/2+100,HEIGHT/2)
LeaverectsList = [Leaverect_1,Leaverect_2]

savebutton1,saverect_1 = returnText('Save',white,font24)
savebutton2,saverect_2 = returnText('Go back',white,font24)
saverect_1.center = (WIDTH/2,250)
saverect_2.center = (WIDTH/2,350)
saverectsList = [saverect_1,saverect_2]

modebutton1,moderect_1 = returnText('Easy Mode',white,font24)
modebutton2,moderect_2 = returnText('Normal Mode',white,font24)
moderect_1.center = (WIDTH/2,250)
moderect_2.center = (WIDTH/2,350)
moderectsList = [moderect_1,moderect_2]

ubutton1,urect_1 = returnText('Upgrade',white,font24)
ubutton2,urect_2 = returnText('ENHANCE',white,font24)
ubutton1d,urect_1d = returnText('Upgrade',darkGrey,font24)
ubutton2d,urect_2d = returnText('ENHANCE',darkGrey,font24)
ubutton3,urect_3 = returnText('Upgrade',white,font24)
ubutton4,urect_4 = returnText('ENHANCE',white,font24)
ubutton5,urect_5 = returnText('Cancel',white,font24)
urect_1.midleft = (115,HEIGHT-60)
urect_2.midleft = (365,HEIGHT-60)
urect_1d.midleft = (115,HEIGHT-60)
urect_2d.midleft = (365,HEIGHT-60)
urect_3.center = (WIDTH/2-150,HEIGHT/2+75)
urect_4.center = (WIDTH/2-150,HEIGHT/2+75)
urect_5.center = (WIDTH/2+150,HEIGHT/2+75)
mainRectList = [[urect_1,urect_2d],[urect_1d,urect_2]]
upgradeRectList = [urect_3,urect_5]

itemDescriptions = ['Go into battle with an extra heart and theconfidence that you will persist.','Run twice as fast after taking enough     damage. No need to be mad at your failure',
                    'Chance that bullets are not used when     shooting','Enemies have a chance of instantly dying  when hit with a melee attack. Something   worth investing in.',
                    'Contains a series of complicated          instructions to transform a bullet into a heart. Rarely works though.',
                    'Shoot bullets at a faster rate with this  gadget. Side effects include sore fingers and a higher kill count',
                    'Designed to walk over metallic hazards,   these boots will get you through! But not very fast',
                    'the only reason why the cops aren\'t       following is because the flames are. But  you shouldn`t be concerned',
                    'This explosive is activated after getting hit four times. We should probably think  of a shorter name for this...',
                    'Melee attacking will deflect bullets. Not as easy as it appears',
                    'Effects unknown. You should probably wear it for good luck']
itemCosts = [1500,5000,3000,8000,8000,7000,1000,4000,5000,3000,100]
itemNames = ['Helpful heart','Adrenaline rush','Recycler','Brass Knuckles','Valentines Card',
             'Quicker Trigger','Steel Boots','flame boots','See Four','BlockMaster','Deans Medallion']
itemValues = [4,6,3,8,6,5,3,6,7,4,8,12]

itemLevelCosts = [[500,1000,1500,750],[500,1000,1500,1000],[500,1000,1500,2000,2500,3000,1500],[500,1000,1500,2000,2500,3000,4000,4000,4000,2000],
                  [500,1000,1500,2000,2500,3000,4000,4000,4000,2500],[500,1000,1500,2000,1500],[500,1000,1500,2000,5000],[500,1000,1500,2000,2500,3000,3000],
                  [500,1000,1500,2000,2500,3000,4000],[5000],[]]
itemLevelText = [['Gain 1 extra heart','Gain 2 extra heart','Gain 2 extra heart','Gain 3 extra heart'],
                 ['Move 1.3x faster when low health','Move 1.5x faster when low health','Move 1.7x faster when low health','Move 2x faster when low health'],
                 ['5% chance to not consume ammo','7% chance to not consume ammo','10% chance to not consume ammo','13% chance to not consume ammo',
                  '17% chance to not consume ammo','21% chance to not consume ammo','26% chance to not consume ammo'],
                 ['2% chance for extra melee dmg','3% chance for extra melee dmg','4% chance for extra melee dmg','6% chance for extra melee dmg','8% chance for extra melee dmg',
                  '11% chance for extra melee dmg','14% chance for extra melee dmg','17% chance for extra melee dmg','21% chance for extra melee dmg','25% chance for extra melee dmg'],
                 ['1% chance to activate','2% chance to activate','2% chance to activate','3% chance to activate','3% chance to activate','4% chance to activate','4% chance to activate',
                  '5% chance to activate','6% chance to activate','7% chance to activate'],
                 ['Shooting cooldown -10%','Shooting cooldown -15%','Shooting cooldown -20%','Shooting cooldown -25%','Shooting cooldown -30%'],
                 ['Speed also goes down -40%','Speed also goes down -35%','Speed also goes down -30%','Speed also goes down -20%','Speed also goes down -10%'],
                 ['Flames last 3 seconds','Flames last 3 seconds','Flames last 3 seconds','Flames last 4 seconds','Flames last 4 seconds','Flames last 4 seconds','Flames last 5 seconds'],
                 ['5 hits to activate, 10 damage','5 hits to activate, 12 damage','5 hits to activate, 15 damage','5 hits to activate, 19 damage','4 hits to activate, 24 damage',
                  '4 hits to activate, 30 damage','3 hits to activate, 37 damage'],
                 ['Melee attacks stop bullets'],[' ']]
itemEnhanceText = ['Heart pickups Restore 1.5 hearts','Skill meter charges 3x at low     health, and 1.5x at higher health','Melee attack deals 2x damage if   the clip is full',
                   'Melee damage is doubled','1/4 heart recovered every 15      seconds','Shooting cooldown -45%','Negates all knockback',
                   'Killing enemies increases SWAT    timer by 5s','Blast wave released every other   time you get hit','Release weak blast wave when you  block bullets','Enhancement Unknown']
itemEnhanceTextMod = ['Heart pickups Restore 1.5 hearts','Skill meter charges 3x at low health, and 1.5x at higher health','Melee attack deals 2x damage if the   clip is full',
                   'Melee damage is doubled','1/4 heart recovered every 15 seconds','Shooting cooldown -45%','Negates all knockback',
                   'Killing enemies increases SWAT timer  by 5s','Blast wave released every other time  you get hit, 37 damage per blast','Release weak blast wave when you blockbullets','Enhancement Unknown']

bulletDescriptions = ['Medium damage and quick bullets. Perfect  to start off with',
                      'Shoot two smaller bullets at a time',
                      'Shoots weak snowballs that slow down      enemies',
                      'Very quick and high damage bullets that   penetrate through enemies.',
                      'These bullets will instantly destroy a    non-boss enemy that it comes into contact with. Upon contact, an explosion is       created from where the enemy was.',
                      'Hold shoot for longer to release a        stronger attack. Very weak when uncharged']
bulletCosts = [1,2000,4000,7000,20000,8000]
bulletNames = ['Standard Bullets','Dual Bullets','Snowballs','Sniper Bullets','AntiMatter bullets','Battery Bullets']

bulletLevelText = [['8 damage per shot','10 damage per shot','12 damage per shot','15 damage per shot','18 damage per shot'],
                   ['5 damage per bullet','6 damage per bullet','7 damage per bullet','8 damage per bullet','9 damage per bullet'],
                   ['6 damage per shot','7 damage per shot','8 damage per shot','9 damage per shot','10 damage per shot','12 damage per shot','16 damage per shot'],
                   ['15 damage per bullet','17 damage per bullet','20 damage per bullet','24 damage per bullet','28 damage per bullet','33 damage per bullet','39 damage per bullet'],
                   ['45 sec charge, blast does 20 dmg','43 sec charge, blast does 22 dmg','41 sec charge, blast does 24 dmg',
                    '39 sec charge, blast does 27 dmg','37 sec charge, blast does 30 dmg','35 sec charge, blast does 33 dmg',
                    '32 sec charge, blast does 37 dmg','29 sec charge, blast does 40 dmg','26 sec charge, blast does 44 dmg',
                    '22 sec charge, blast does 49 dmg'],
                   ['20 damage when fully charged','23 damage when fully charged','26 damage when fully charged','30 damage when fully charged','34 damage when fully charged',
                    '38 damage when fully charged','42 damage when fully charged','47 damage when fully charged','53 damage when fully charged','60 damage when fully charged']]
bulletLevelCosts = [[100,200,500,3000,1500],[100,200,500,3000,2500],[100,200,500,1000,2000,3000,5000],[100,200,500,1000,2000,3000,6000],
                    [100,200,500,1000,2000,3000,4000,5000,5000,8000],[100,200,500,1000,2000,3000,4000,5000,5000,10000]]
bulletEnhanceText = ['Bullets deal extra 5 damage when 8 or less bullets are loaded','Shield meter charges slightly     faster','Slowed enemies deal less damage',
                    'Bullets damage increases by 5     after each enemy pierced','Blast waves can be absorbed to    heal 3/4 hearts per  blast wave','Speed increases by 1.5 times while bullet is charged']
bulletEnhanceTextMod = ['Bullets deal extra 5 damage when 8 or less bullets are loaded','Shield meter charges slightly faster','Slowed enemies deal less damage',
                    'Bullets damage increases by 5 after   each enemy pierced','Blast waves can be absorbed to heal   3/4 hearts per  blast wave','Speed increases by 1.5 times while    bullet is charged']
bulletUsage = ['1','2','3','6','12','4']
            
#loading all the files that will ever be needed
def find_data_file(filename):
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = path.dirname(__file__)
    return path.join(datadir, filename)

map_folder = find_data_file('maps')
img_folder = find_data_file('images')
text_folder = find_data_file('text')
music_folder = find_data_file('music')

gameIcon = py.image.load(path.join(img_folder,'icon.png'))
py.display.set_icon(gameIcon)

#loading all the maps and info
#multi-dimensional - 1st layer is which bank. second layer is which setion. 3rd layer is file or map
mapsL = []
bank1mapsOnly = [TiledMap(path.join(map_folder,'b1Entrance.tmx')),
                 TiledMap(path.join(map_folder,'b1Main.tmx')),
                 TiledMap(path.join(map_folder,'b1Corridors3.tmx')),
                 TiledMap(path.join(map_folder,'b1Corridors4.tmx')),
                 TiledMap(path.join(map_folder,'b1Corridors5.tmx')),
                 TiledMap(path.join(map_folder,'b1Corridors6.tmx')),
                 TiledMap(path.join(map_folder,'b1Boss.tmx')),
                 TiledMap(path.join(map_folder,'b1Vault.tmx')),
                 TiledMap(path.join(map_folder,'b1Corridors7.tmx')),
                 TiledMap(path.join(map_folder,'b1Corridors8.tmx'))]
bank1 = []
for i in bank1mapsOnly:
    bank1.append([i,i.make_map()])

bank2mapsOnly = [TiledMap(path.join(map_folder,'b2Entrance.tmx')),
                 TiledMap(path.join(map_folder,'b2Main.tmx')),
                 TiledMap(path.join(map_folder,'b2Corridors1.tmx')),
                 TiledMap(path.join(map_folder,'b2Corridors2.tmx')),
                 TiledMap(path.join(map_folder,'b2Boss.tmx')),
                 TiledMap(path.join(map_folder,'b2Vault.tmx')),
                 TiledMap(path.join(map_folder,'b2Corridors3.tmx')),
                 TiledMap(path.join(map_folder,'b2Corridors4.tmx'))]
bank2 = []
for i in bank2mapsOnly:
    bank2.append([i,i.make_map()])

bank3mapsOnly = [TiledMap(path.join(map_folder,'b3Entrance.tmx')),
                 TiledMap(path.join(map_folder,'b3Main.tmx')),
                 TiledMap(path.join(map_folder,'b3Corridors1.tmx')),
                 TiledMap(path.join(map_folder,'b3Corridors2.tmx')),
                 TiledMap(path.join(map_folder,'b3Corridors3.tmx')),
                 TiledMap(path.join(map_folder,'b3Boss.tmx')),
                 TiledMap(path.join(map_folder,'b3Vault.tmx')),
                 TiledMap(path.join(map_folder,'b3Corridors4.tmx'))]
bank3 = []
for i in bank3mapsOnly:
    bank3.append([i,i.make_map()])

bank4mapsOnly = [TiledMap(path.join(map_folder,'b4Entrance.tmx')),
                 TiledMap(path.join(map_folder,'b4Main.tmx')),
                 TiledMap(path.join(map_folder,'b4Corridors1.tmx')),
                 TiledMap(path.join(map_folder,'b4Corridors2.tmx')),
                 TiledMap(path.join(map_folder,'b4Boss.tmx')),
                 TiledMap(path.join(map_folder,'b4Vault.tmx')),
                 TiledMap(path.join(map_folder,'b4Corridors3.tmx'))]
bank4 = []
for i in bank4mapsOnly:
    bank4.append([i,i.make_map()])

bank5mapsOnly = [TiledMap(path.join(map_folder,'b5Entrance.tmx')),
                 TiledMap(path.join(map_folder,'b5Main.tmx')),
                 TiledMap(path.join(map_folder,'b5Corridors1.tmx')),
                 TiledMap(path.join(map_folder,'b5Corridors2.tmx')),
                 TiledMap(path.join(map_folder,'b5Corridors3.tmx')),
                 TiledMap(path.join(map_folder,'b5Corridors4.tmx')),
                 TiledMap(path.join(map_folder,'b5Boss.tmx')),
                 TiledMap(path.join(map_folder,'b5Corridors5.tmx'))]
bank5 = []
for i in bank5mapsOnly:
    bank5.append([i,i.make_map()])

HomeMap = [TiledMap(path.join(map_folder,'Home Base.tmx'))]
homeMap = []
for i in HomeMap:
    homeMap.append([i,i.make_map()])
mapsL.append(homeMap)
mapsL.append(bank1)#infor for bank1Entrance
mapsL.append(bank2)
mapsL.append(bank3)
mapsL.append(bank4)
mapsL.append(bank5)

#set up general variables, including the player and camera
newgame = True
titleScreen = True
index = 0
index2 = 0
all_sprites = py.sprite.Group()#handle sprites updates etc
sureExit = False
fromSave = False
selectSound = py.mixer.Sound(path.join(music_folder,'newSelect.wav'))
mode = None
while running:
    index = 0
    fromsave = False
    while titleScreen:#automatically starts in title screen
        clock.tick(FPS)
        screen.fill(black)
        #draw 5 buttons for: new game, continue, how to play, settings and exit
        screen.blit(button1,rect_1)
        screen.blit(button2,rect_2)
        screen.blit(button3,rect_3)
        screen.blit(button4,rect_4)
        
        py.draw.rect(screen, white, [rectsList[index].x - 30,(rect_1.centery-3)+(50*index),6,6],5)
        #check events
        change,select = events(1)
        index +=change
        #making sure the selector stays in range
        if index >3:
            index = 0
        if index < 0:
            index = 3
        #when you select, determining what to do
        if select !=0:
            if index == 0:
                sureExit = False
                titleScreen=False
                modeIndex = 0
                while True:
                    clock.tick(FPS)
                    screen.fill(black)
                    screen.blit(modebutton1,moderect_1)
                    screen.blit(modebutton2,moderect_2)
                    
                    py.draw.rect(screen, white, [moderectsList[modeIndex].x - 30,(moderectsList[modeIndex].centery-3),6,6],5)
                    #check events
                    change,select = events(1)
                    modeIndex +=change
                    if modeIndex >1:
                        modeIndex = 0
                    if modeIndex <0:
                        modeIndex = 1
                    if select!= 0:
                        if modeIndex == 0:
                            mode = 'easy'
                            break
                        if modeIndex == 1:
                            mode = 'normal'
                            break
                    py.display.flip()
                    
            if index ==1:
                sureExit = False
                fromsave = True
                titleScreen=False
            if index == 2:
                how_to_play()
            if index == 3:
                py.quit()
                py.mixer.quit()
                sys.exit()
        py.display.flip()
        
    #################################################################
    #run game loop at start, with tutorial mode.
    g=Game(mapsL)
    g.mode = mode
    if mode == 'easy':
        g.hearts +=1
        
    if fromsave:
        g.newGame = False
        with open(path.join(text_folder,'gameStat.txt')) as file:
            allsaves = file.readlines()
        allsaves = [word.strip() for word in allsaves]
        g.totalGold = int(allsaves[0])
        g.hearts = int(allsaves[1])
        g.unlocked = int(allsaves[2])
        allsaves[3] = allsaves[3].split(',')
        allsaves[4] = allsaves[4].split(',')
        allsaves[5] = allsaves[5].split(',')
        allsaves[6] = allsaves[6].split(',')
        allsaves[7] = allsaves[7].split(',')
        allsaves[8] = allsaves[8].split(',')
        allsaves[9] = allsaves[9].split(',')
        allsaves[10] = allsaves[10].split(',')
        allsaves[11] = allsaves[11].split(',')
        for i1 in range(3,12):
            for i in range(len(allsaves[i1])):
                if allsaves[i1][i] == '\'none\'':
                    allsaves[i1][i]='none'
                elif allsaves[i1][i] == 'self.heartPowerup':
                    allsaves[i1][i] = g.heartPowerup
                elif allsaves[i1][i] == 'self.speedPowerup':
                    allsaves[i1][i] = g.speedPowerup
                elif allsaves[i1][i] == 'self.meleePowerup':
                    allsaves[i1][i] = g.meleePowerup
                elif allsaves[i1][i] == 'self.shootingPowerup':
                    allsaves[i1][i] = g.shootingPowerup
                elif allsaves[i1][i] == 'self.valentinesPowerup':
                    allsaves[i1][i] = g.valentinesPowerup
                elif allsaves[i1][i] == 'self.steelPowerup':
                    allsaves[i1][i] = g.steelPowerup
                elif allsaves[i1][i] == 'self.quickPowerup':
                    allsaves[i1][i] = g.quickPowerup
                elif allsaves[i1][i] == 'self.firePowerup':
                    allsaves[i1][i] = g.firePowerup
                elif allsaves[i1][i] == 'self.C4Powerup':
                    allsaves[i1][i] = g.C4Powerup
                elif allsaves[i1][i] == 'self.blockPowerup':
                    allsaves[i1][i] = g.blockPowerup
                elif allsaves[i1][i] == 'self.deanPowerup':
                    allsaves[i1][i] = g.deanPowerup
                elif allsaves[i1][i] == 'self.normalBullet':
                    allsaves[i1][i] = g.normalBullet
                elif allsaves[i1][i] == 'self.dualBullet':
                    allsaves[i1][i] = g.dualBullet
                elif allsaves[i1][i] == 'self.snowBullet':
                    allsaves[i1][i] = g.snowBullet
                elif allsaves[i1][i] == 'self.sniperBullet':
                    allsaves[i1][i] = g.sniperBullet
                elif allsaves[i1][i] == 'self.antiBullet':
                    allsaves[i1][i] = g.antiBullet
                elif allsaves[i1][i] == 'self.batteryBullet':
                    allsaves[i1][i] = g.batteryBullet
                elif allsaves[i1][i] == '0':
                    allsaves[i1][i] = 0
                else: allsaves[i1] = []
        g.purchasedItems = allsaves[3]
        g.equipedItems = allsaves[4]
        for i in g.equipedItems:
            if i == g.steelPowerup:
                g.speedPercent = .8
        g.forSaleItems = allsaves[5]
        g.notYetForSaleItems = allsaves[6]
        g.equipedBullet = allsaves[7]
        g.purchasedBullets = allsaves[8]
        g.forSaleBullets = allsaves[9]
        g.notYetForSaleBullets = allsaves[10]
        g.orderedBullets = allsaves[11]
        g.unlockedSlots = int(allsaves[12])
        g.boosterValue = int(allsaves[13])
        g.currentBooster = int(allsaves[14])
        g.talkedToDean = int(allsaves[15])
        x = allsaves[16]
        x = x.split(',')
        for i in range(len(x)):
            x[i] = int(x[i])
        g.bagsStolen = x
        allsaves[17] = allsaves[17].split(',')
        for i in range(len(allsaves[17])):
           allsaves[17][i] = float(allsaves[17][i])
        g.bulletTime = allsaves[17]
        
        allsaves[18] = allsaves[18].split(',')
        for i in range(len(allsaves[18])):
           allsaves[18][i] = int(allsaves[18][i])
        g.bulletLevel = allsaves[18]

        allsaves[19] = allsaves[19].split(',')
        for i in range(len(allsaves[19])):
           allsaves[19][i] = int(allsaves[19][i])
        g.powerupLevel = allsaves[19]
        g.mode = allsaves[20]
        
        for i in g.equipedItems:
            if i != 'none':
                g.purchasedItems.append(i)
        for i in range(len(g.purchasedItems)):
            if g.purchasedItems[i] == g.heartPowerup:
                itemNum = 0
            if g.purchasedItems[i] == g.speedPowerup:
                itemNum = 1
            if g.purchasedItems[i] == g.shootingPowerup:
                itemNum = 2
            if g.purchasedItems[i] == g.meleePowerup:
                itemNum = 3
            if g.purchasedItems[i] == g.valentinesPowerup:
                itemNum = 4
            if g.purchasedItems[i] == g.quickPowerup:
                itemNum = 5
            if g.purchasedItems[i] == g.steelPowerup:
                itemNum = 6
            if g.purchasedItems[i] == g.firePowerup:
                itemNum = 7
            if g.purchasedItems[i] == g.C4Powerup:
                itemNum = 8
            if g.purchasedItems[i] == g.blockPowerup:
                itemNum = 9
            if g.purchasedItems[i] == g.deanPowerup:
                itemNum = 10
            
            if g.powerupLevel[itemNum]>=(len(itemLevelCosts[itemNum])):
                if g.purchasedItems[i] == g.heartPowerup:
                    
                    for section in range(len(g.equipedItems)):
                        if g.equipedItems[section] == g.heartPowerup:
                            g.equipedItems[section] = g.maxedList[0]
                    g.heartPowerup = g.maxedList[0]
                    g.purchasedItems[i] = g.heartPowerup
                    continue
                if g.purchasedItems[i] == g.speedPowerup:
                    
                    for section in range(len(g.equipedItems)):
                        if g.equipedItems[section] == g.speedPowerup:
                            g.equipedItems[section] = g.maxedList[1]
                    g.speedPowerup = g.maxedList[1]
                    g.purchasedItems[i] = g.speedPowerup
                    continue
                if g.purchasedItems[i] == g.shootingPowerup:
                    
                    for section in range(len(g.equipedItems)):
                        if g.equipedItems[section] == g.shootingPowerup:
                            g.equipedItems[section] = g.maxedList[2]
                    g.shootingPowerup = g.maxedList[2]
                    g.purchasedItems[i] = g.shootingPowerup
                    continue
                if g.purchasedItems[i] == g.meleePowerup:
                    
                    for section in range(len(g.equipedItems)):
                        if g.equipedItems[section] == g.meleePowerup:
                            g.equipedItems[section] = g.maxedList[3]
                    g.meleePowerup = g.maxedList[3]
                    g.purchasedItems[i] = g.meleePowerup
                    continue
                if g.purchasedItems[i] == g.valentinesPowerup:
                    
                    for section in range(len(g.equipedItems)):
                        if g.equipedItems[section] == g.valentinesPowerup:
                            g.equipedItems[section] = g.maxedList[4]
                    g.valentinesPowerup = g.maxedList[4]
                    g.purchasedItems[i] = g.valentinesPowerup
                    continue
                if g.purchasedItems[i] == g.quickPowerup:
                    
                    for section in range(len(g.equipedItems)):
                        if g.equipedItems[section] == g.quickPowerup:
                            g.equipedItems[section] = g.maxedList[5]
                    g.quickPowerup = g.maxedList[5]
                    g.purchasedItems[i] = g.quickPowerup
                    continue
                if g.purchasedItems[i] == g.steelPowerup:
                    
                    for section in range(len(g.equipedItems)):
                        if g.equipedItems[section] == g.steelPowerup:
                            g.equipedItems[section] = g.maxedList[6]
                    g.steelPowerup = g.maxedList[6]
                    g.purchasedItems[i] = g.steelPowerup
                    continue
                if g.purchasedItems[i] == g.firePowerup:
                    
                    for section in range(len(g.equipedItems)):
                        if g.equipedItems[section] == g.firePowerup:
                            g.equipedItems[section] = g.maxedList[7]
                    g.firePowerup = g.maxedList[7]
                    g.purchasedItems[i] = g.firePowerup
                    g.movingFire = g.movingFireG
                    continue
                    
                if g.purchasedItems[i] == g.C4Powerup:
                    
                    for section in range(len(g.equipedItems)):
                        if g.equipedItems[section] == g.C4Powerup:
                            g.equipedItems[section] = g.maxedList[8]
                    g.C4Powerup = g.maxedList[8]
                    g.purchasedItems[i] = g.C4Powerup
                if g.purchasedItems[i] == g.blockPowerup:
                    
                    for section in range(len(g.equipedItems)):
                        if g.equipedItems[section] == g.blockPowerup:
                            g.equipedItems[section] = g.maxedList[9]
                    g.blockPowerup = g.maxedList[9]
                    g.purchasedItems[i] = g.blockPowerup
                    continue
                if g.purchasedItems[i] == g.deanPowerup:
                    
                    for section in range(len(g.equipedItems)):
                        if g.equipedItems[section] == g.deanPowerup:
                            g.equipedItems[section] = g.maxedList[10]
                    g.deanPowerup = g.maxedList[10]
                    g.purchasedItems[i] = g.deanPowerup
                    continue



        for i in g.equipedItems:
            if i != 'none':
                g.purchasedItems.remove(i)
    
    g.run()
    if g.goToTitle:
        titleScreen = True
    index = 0
    while not sureExit:
        clock.tick(FPS)
        screen.fill(black)
        #draw 5 buttons for: new game, continue, how to play, settings and exit
        displaytext('Are you sure you want to exit to the main menu?',WIDTH/2,HEIGHT/2-200,white,font18)
        displaytext('All process from the last save will be lost',WIDTH/2,HEIGHT/2-150,white,font18)
        screen.blit(Leavebutton1,Leaverect_1)
        screen.blit(Leavebutton2,Leaverect_2)
        
        py.draw.rect(screen, white, [LeaverectsList[index].centerx,HEIGHT/2-30,6,6],5)
        #check events
        change,select = events(5)
        index +=change
        #making sure the selector stays in range
        if index >1:
            index = 0
        if index < 0:
            index = 1
        #when you select, determining what to do
        if select !=0:
            if index == 0:
                titleScreen = True
                sureExit = True
                break
            if index == 1:
                g.goToTitle = False
                if g.wasPaused:
                    g.paused()
                    g.running = True
                    g.wasPaused = False
                else:
                    g.levelMenu = True
                g.run()
        py.display.flip()
    del g

py.quit()
py.mixer.quit()
