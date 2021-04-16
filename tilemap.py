import pygame as py
import pytmx,random
from settings import *

def collide_hit_rect(one,two):
    return one.hit_rect.colliderect(two.rect)

class TiledMap:
    def __init__(self,filename):
        tm = pytmx.load_pygame(filename,pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self,surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x,y, gid in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x*self.tmxdata.tilewidth,
                                                y*self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = py.Surface((self.width,self.height))
        self.render(temp_surface)
        return temp_surface

class CameraBound(py.sprite.Sprite):
    def __init__(self,direction,x,y,width,height,create):
        py.sprite.Sprite.__init__(self)
        self.rect = py.Rect(x,y,width,height)
        self.direction = int(direction)
        self.image = py.Surface((1,1))
        self.image.set_colorkey(black)
        self.create = create
        if self.create == -1:
            self.showing = True
        else: self.showing = False


class TextTime(py.sprite.Sprite):
    def __init__(self,center,w,h,textType,neededKeys):
        py.sprite.Sprite.__init__(self)
        self.image = py.Surface((w,h))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.text = textType
        self.neededKeys = neededKeys


class EndLevel(py.sprite.Sprite):
    def __init__(self,center,w,h,textFile):
        py.sprite.Sprite.__init__(self)
        self.image = py.Surface((w,h))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.textFile = textFile


class menu(py.sprite.Sprite):
    def __init__(self,center):
        py.sprite.Sprite.__init__(self)
        self.image = py.Surface((64,64))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.center = center


class Particles(py.sprite.Sprite):
    def __init__(self,game,color,x,y,yvel,xvel,changingVel,alphaDec,pSize,velrange = 5):
        py.sprite.Sprite.__init__(self)
        self.game = game
        self.image = py.Surface(pSize)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.changingVel = changingVel
        self.rect.x = x
        self.rect.y = y
        self.yvel = yvel
        self.xvel = xvel
        self.alpha = random.randint(200,255)
        self.alphaDecrease = alphaDec
        self.image.set_alpha(self.alpha)
        self.changeCounter = 0
        self.velrange = 5
        
    def update(self):
        if self.changeCounter == 0:
            if self.changingVel == 'x':
                self.xvel = random.randint(-self.velrange,self.velrange)
            elif self.changingVel == 'y':
                self.yvel = random.randint(-self.velrange,self.velrange)
            self.changeCounter = 60
        self.rect.x +=self.xvel
        self.rect.y +=self.yvel
        self.alpha -=self.alphaDecrease
        self.image.set_alpha(self.alpha)
        if self.alpha <=0:
            self.kill()
        self.changeCounter -=1
    
