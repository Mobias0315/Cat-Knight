import pygame as pg
import os 
from neko import *

class map(pg.sprite.Sprite):
    def __init__(self, array = None, map_name = 'map1', neko_next = (1,15), neko_blood = 200) :
        pg.sprite.Sprite.__init__(self)
        self.img = [pg.image.load(os.path.join('./img/Green World - Tileset/map','Green World - Tileset%d.png'%i)).convert_alpha() for i in range(1,97)]
        self.map_name = map_name
        with open(f'./map/{map_name}.txt','r',encoding='utf-8') as r:
            a = [list(eval(i)) for i in r.read().split('\n')] 
            self.a = [ a[0:len(a)//3] ,a[len(a)//3:(len(a)//3)*2] ,a[(len(a)//3)*2:] ]
        if array is not None:
            self.a = [ array[0:len(array)//3] ,array[len(array)//3:(len(array)//3)*2] ,array[(len(array)//3)*2:] ]
        self.mapbg = pg.Surface((80*len(self.a[0][0]), 80*len(self.a[0]))).convert_alpha()
        self.mapbg.set_colorkey((0, 0, 0))
        self.role_list = []
        self.play_list = []
        for i in range(len(self.a)):
            for j in range(len(self.a[i])):
                for k in range(len(self.a[i][j])):
                    # if i == 1 and j == neko_next[1] and k == neko_next[0]: self.play_list.append( neko((k,j), self.a, neko_blood) )
                    if self.a[i][j][k] == 97: 
                        self.play_list.append( neko((k,j),self.a, neko_blood) )
                    elif self.a[i][j][k] == 0 : continue
                    elif self.a[i][j][k] in range(98,108):
                        role = [bat((k,j),self.a),
                                Mushroom((k,j),self.a),
                                Worker_Mole((k,j),self.a),
                                Smiling_Frog((k,j),self.a),
                                UFO_Tako((k,j),self.a),
                                Bear((k,j),self.a),
                                Ghost((k,j),self.a),
                                Golem((k,j),self.a),
                                Shark((k,j),self.a),
                                Man_Eater_Plant((k,j),self.a) ]
                        self.role_list.append( role[self.a[i][j][k]-98] )
                    else:
                        self.mapbg.blit(self.img[self.a[i][j][k]-1],(k*80,j*80))
        self.image = self.mapbg
        self.rect = self.image.get_rect()
    def update(self, time, keys, map, mon_spr = None):
        pass

    

####################################################
class monster(pg.sprite.Sprite):
    def __init__(self,name,map_array,coordinate) :
        pg.sprite.Sprite.__init__(self)
        folder = os.listdir('./img/monster/%s'%name)
        if 'Idle' in folder :
            self.img_idle = [pg.image.load(os.path.join('./img/monster/%s/Idle/Frames/%s Idle%s.png'%(name,name,i))).convert_alpha() for i in range(1,len(os.listdir('./img/monster/%s/Idle/Frames'%name))+1)]
            self.right_img_idle = [pg.transform.flip(i,1,0) for i in self.img_idle]        
        if 'Move' in folder :
            self.img_move = [pg.image.load(os.path.join('./img/monster/%s/Move/Frames/%s Move%s.png'%(name,name,i))).convert_alpha() for i in range(1,len(os.listdir('./img/monster/%s/Move/Frames'%name))+1)]
            self.right_img_move = [pg.transform.flip(i,1,0) for i in self.img_move]     
        if 'Death' in folder :
            self.img_death =  [pg.image.load(os.path.join('./img/monster/%s/Death/Frames/%s Death%s.png'%(name,name,i))).convert_alpha() for i in range(1,len(os.listdir('./img/monster/%s/Death/Frames'%name))+1)]
            self.right_img_death = [pg.transform.flip(i,1,0) for i in self.img_death]     
        if 'Hit' in folder :
            self.img_hit = [pg.image.load(os.path.join('./img/monster/%s/Hit/Frames/%s Hit%s.png'%(name,name,i))).convert_alpha() for i in range(1,len(os.listdir('./img/monster/%s/Hit/Frames'%name))+1)]
            self.right_img_hit = [pg.transform.flip(i,1,0) for i in self.img_hit]
        self.image = self.img_idle[0]
        self.rect = self.image.get_rect()
        self.radius = 150 #圓圈偵測範圍
        self.blood = int
        self.speed = int
        self.anime_speed_control = 5
        self.anime_time_hit = 0
        self.x , self.y = 0,0
        self.col_map = map_array[1] # 地圖
        self.sleep = 1  # 等待玩家靠近
        self.mo = [0,0,0,0,0,0]  #stop right left up death hit  
                                 #  0    1    2   3    4    5
        self.bott = int  # 角色底部位置加成
        self.side = 50  # 角色邊位置加成
        self.hit_cd = 30  # 受傷無敵時間
        self.reset_hit_cd = 1 # 立即重製受傷
        self.damage_num = 50
    def update(self, time, keys, map, neko = None , mon_spr = None):
        if neko != None:
            self.neko = neko[0]
            self.damage(time, neko[0])
        else:
            self.anime(time)
            self.colli_look()
            self.colli_wall(map[0])
            if not self.x :
                self.mo[0] = 1
            else: self.mo[0] = 0
            self.rect.x += self.x
            self.rect.y += self.y
        
    def anime(self, time):
        if self.mo[1] :
            img_idle = self.right_img_idle[:]
            img_move = self.right_img_move[:]
            img_death = self.right_img_death[:]
            img_hit = self.right_img_hit[:]
        else: 
            img_idle = self.img_idle[:]
            img_move = self.img_move[:]
            img_death = self.img_death[:]
            img_hit = self.img_hit[:]
        
        if not self.sleep and not self.mo[5]:
            
            distance = ((self.rect.centerx - self.neko.rect.centerx)**2 + (self.rect.centery - self.neko.rect.centery)**2)**0.5
            if distance != 0 :
                move_distance = distance
            else :move_distance = 0.1
            move_x = (self.rect.center[0] - self.neko.rect.center[0]) / move_distance #X移動方向
            self.x = -(move_x * self.speed)
            self.image = img_move[0:len(img_move)][int((time/self.anime_speed_control)%len(img_move))]
            if self.mo[0] :
                self.image = img_idle[0:len(img_idle)][int((time/self.anime_speed_control)%len(img_idle))]
    #####################不動###################
        elif not self.mo[5] :
            self.image = img_idle[0:len(img_idle)][int((time/self.anime_speed_control)%len(img_idle))]
            
        
    ######################死亡#####################
        if self.blood <= 0 or self.mo[4]:
            if not self.mo[4]: 
                self.time_death = time
            self.mo[4] = 1
            self.image = img_death[0:len(img_death)][int(((time - self.time_death) /self.anime_speed_control)%len(img_death))]
            if self.image == img_death[-1]:
                self.kill()
            self.x, self.y  = 0, 0
    ######################受傷##################### 
        if self.mo[5] and not self.mo[4]:
            self.image = img_hit[0:len(img_hit)][int(((time - self.anime_time_hit) /self.anime_speed_control)%len(img_hit))]
            if self.image == img_hit[-1]:
                self.mo[5] = 0
                self.reset_hit_cd = 1

            if self.repel:
                a = ((-1)**self.mo[1]) * 10
                b = ( -1 * ((-1)**self.mo[1]) * (time-self.anime_time_hit) * 0.5 )
                self.x = a + b 
                if abs(a) <= abs(b):
                    self.x = 0
            else : self.x = 0
        if self.x > 0 and not self.mo[5]:
            self.mo[1], self.mo[2] = 1,0
        elif self.x < 0 and not self.mo[5]:
            self.mo[1], self.mo[2] = 0,1


    def colli_look(self):
        if pg.sprite.collide_circle(self, self.neko):
            self.sleep = 0

    def colli_wall(self, map):
        wall = (1,2,3,4,5,6,7,8,13,14,15,16,17,18,19,20,25,26,27,28,29,30,31,32,33,34,35,37,38,39,40,41,42,43,44,45,49,50,51,52,53)
        YNotOverScreen = (self.rect.centery - map.rect.y)//80+1 < len(self.col_map)
        
        #踩地碰撞
        if self.rect.centery - map.rect.y>=0 \
            and self.rect.centery+self.y >= ((self.rect.centery - map.rect.y)//80)*80 +30 + map.rect.y \
            and YNotOverScreen \
            and ((self.col_map[(self.rect.centery - map.rect.y)//80+1][(self.rect.centerx-15 - map.rect.x)//80] in wall) \
            or (self.col_map[(self.rect.centery - map.rect.y)//80+1][(self.rect.centerx+15 - map.rect.x)//80] in wall)):
            
            self.y = 0
            # self.rect.centery = (self.rect.centery//80)*80 +30
            
            
        else: pass
        #天花板碰撞
        if (self.rect.centery+45)//80 > 0 \
            and YNotOverScreen\
            and ((self.col_map[(self.rect.centery+45 - map.rect.y)//80-1][(self.rect.centerx-15 - map.rect.x)//80] in wall)\
            and self.y <= 0\
            or self.col_map[(self.rect.centery+45 -map.rect.y)//80-1][(self.rect.centerx+15 - map.rect.x)//80] in wall) :
            # and pg.sprite.collide_mask(self,self.map) :

            if self.y < 0 :self.y =0
        else : pass
        #左右碰撞
        if ((self.rect.centery+45)//80 > 0 \
            and YNotOverScreen\
            and (self.col_map[(self.rect.centery - map.rect.y)//80][((self.rect.centerx - self.side - 20 - map.rect.x)//80)+1] in wall)) \
            or ((self.rect.centerx - self.side - map.rect.x)//80+1 < len(self.col_map[0]) 
            and self.col_map[ (self.rect.centery - map.rect.y)//80+1 ][ (self.rect.centerx - self.side -20 - map.rect.x)//80+1 ] not in wall )\
            or (self.rect.centerx - self.side - map.rect.x)//80 == len(self.col_map[0])-1:
            
            if self.x > 0 : 
                self.x = 0
        else : pass

        if ((self.rect.centery+45)//80 > 0 \
            and YNotOverScreen\
            and (self.col_map[(self.rect.centery - map.rect.y)//80][((self.rect.centerx + self.side +20 - map.rect.x)//80)-1] in wall) )\
            or self.col_map[ (self.rect.centery - map.rect.y)//80+1 ][ (self.rect.centerx + self.side + 20 - map.rect.x)//80-1 ] not in wall \
            or (self.rect.centerx + self.side - map.rect.x)//80 == 0:
            
            if self.x < 0 : self.x = 0
        else: pass

    def hit(self, time, damage, reset = False, repel=False):
        self.repel = repel
        if  time - self.anime_time_hit >= self.hit_cd or (reset and self.reset_hit_cd ):
            self.anime_time_hit = time
            if reset:
                self.reset_cd = 0
            self.mo[5] = 1
            self.blood -= damage
    
    def damage(self, time, player):
        if pg.sprite.collide_mask(self, player):
            player.hit(time,self.damage_num)
class bat(monster):
    def __init__(self,coordinate,map_array):
        monster.__init__(self,'Bat',map_array,coordinate)
        self.bott =  30
        self.rect.center = (80*coordinate[0],80*coordinate[1])
        self.speed = 3
        self.blood = 1
        self.damage_num = 3
    def anime(self, time):
        if self.mo[1] :
            img_idle = self.right_img_idle[:]
            img_move = self.right_img_move[:]
            img_death = self.right_img_death[:]

        else: 
            img_idle = self.img_idle[:]
            img_move = self.img_move[:]
            img_death = self.img_death[:]


        if not self.sleep :
            distance = ((self.rect.centerx - self.neko.rect.centerx)**2 + (self.rect.centery - self.neko.rect.centery)**2)**0.5
            if distance != 0 :
                move_distance = distance
            else :move_distance = 0.1
            move_x = (self.rect.center[0] - self.neko.rect.center[0]) / move_distance #X移動方向
            move_y = (self.rect.center[1] - self.neko.rect.center[1]) / move_distance #Y移動方向
            self.x = -(move_x * self.speed) 
            self.y = -(move_y * self.speed) 
            self.image = img_move[0:len(img_move)][int((time/self.anime_speed_control)%len(img_move))]
    #####################不動###################
        else :
            self.image = img_idle[0:len(img_idle)][int((time /self.anime_speed_control)%len(img_idle))]
        
        
    ######################死亡#####################
        if self.blood <= 0 or self.mo[4]:
            if not self.mo[4]: 
                self.time_death = time
            self.mo[4] = 1
            self.image = img_death[0:len(img_death)][int(((time-self.time_death )/self.anime_speed_control)%len(img_death))]
            self.x, self.y  = 0, 0
            if self.image == img_death[-1]:
                self.kill()
        if self.x > 0:
            self.mo[1], self.mo[2] = 1,0
        elif self.x < 0 :
            self.mo[1], self.mo[2] = 0,1

    def colli_wall(self, map):
        wall = (1,2,3,4,5,6,7,8,13,14,15,16,17,18,19,20,21,25,26,27,28,29,30,31,32,33,34,35,37,38,39,40,41,42,43,44,45,49,50,51,52,53)
        YNotOverScreen = (self.rect.centery - map.rect.y)//80+1 < len(self.col_map)
        
        if self.rect.centery- map.rect.y >=0 \
            and self.rect.centery+self.y + self.bott>= ((self.rect.centery - map.rect.y)//80+1)*80 + map.rect.y \
            and YNotOverScreen \
            and ((self.col_map[(self.rect.centery - map.rect.y)//80+1][(self.rect.centerx-self.side - map.rect.x)//80] in wall) \
            or (self.col_map[(self.rect.centery - map.rect.y)//80+1][(self.rect.centerx+self.side-10 - map.rect.x)//80] in wall)):
            
            self.y = 0
            # self.rect.centery = (self.rect.centery//80)*80 +30
            
        else: pass
        #天花板碰撞
        if (self.rect.centery+45)//80 > 0 \
            and YNotOverScreen\
            and ((self.col_map[(self.rect.centery+45 - map.rect.y)//80-1][(self.rect.centerx-15 - map.rect.x)//80] in wall)\
            and self.y <= 0\
            or self.col_map[(self.rect.centery+45 - map.rect.y)//80-1][(self.rect.centerx+15 - map.rect.x)//80] in wall) :
            # and pg.sprite.collide_mask(self,self.map) :

            if self.y < 0 :self.y =0
        else : pass
        #左右碰撞
        if ((self.rect.centery+45)//80 > 0 \
            and YNotOverScreen\
            and (self.col_map[(self.rect.centery - map.rect.y)//80][((self.rect.centerx-self.side - map.rect.x)//80)+1] in wall)) \
            or (self.rect.centerx-30 - map.rect.x)//80 == len(self.col_map[0])-1:
            
            if self.x > 0 : self.x = 0
        else : pass

        if ((self.rect.centery+45)//80 > 0 \
            and YNotOverScreen\
            and (self.col_map[(self.rect.centery - map.rect.y)//80][((self.rect.centerx + self.side - map.rect.x)//80)-1] in wall) )\
            or (self.rect.centerx+50 - map.rect.x)//80 == 0:
            
            if self.x < 0 : self.x = 0
        else: pass

class Man_Eater_Plant(monster) :
    def __init__(self,coordinate, map_array):
        monster.__init__(self, 'Man Eater Plant', map_array, coordinate)
        self.bott =  42
        self.rect.center = (80*coordinate[0],80*coordinate[1]+self.bott)
        self.speed = 3
        self.blood = 100*2
        self.side = 40
        self.damage_num = 8
class Mushroom(monster):
    def __init__(self, coordinate, map_array):
        monster.__init__(self, 'Mushroom', map_array, coordinate)
        self.bott = 42
        self.rect.center = (80*coordinate[0],80*coordinate[1]+self.bott)
        self.speed = 3
        self.blood = 40*2
        self.side = 30
        self.damage_num = 6
class Smiling_Frog(monster):
    def __init__(self, coordinate, map_array):
        monster.__init__(self, 'Smiling Frog', map_array, coordinate)
        self.bott = 64
        self.rect.center = (80*coordinate[0],80*coordinate[1]+self.bott)
        self.speed = 3
        self.blood = 30*2
        self.side = 30
        self.damage_num = 2
class UFO_Tako(monster):
    def __init__(self, coordinate, map_array):
        monster.__init__(self, 'UFO Tako', map_array, coordinate)
        self.bott = 22
        self.rect.center = (80*coordinate[0],80*coordinate[1]+self.bott)
        self.speed = 3
        self.blood = 40*2
        self.side = 15
        self.damage_num = 6
    def anime(self, time):
        if self.mo[1] :
            img_idle = self.right_img_idle[:]
            img_move = self.right_img_move[:]
            img_death = self.right_img_death[:]
            img_hit = self.right_img_hit[:]
        else: 
            img_idle = self.img_idle[:]
            img_move = self.img_move[:]
            img_death = self.img_death[:]
            img_hit = self.img_hit[:]


        if not self.sleep :
            distance = ((self.rect.centerx - self.neko.rect.centerx)**2 + (self.rect.centery - self.neko.rect.centery)**2)**0.5
            if distance != 0 :
                move_distance = distance
            else :move_distance = 0.1
            move_x = (self.rect.center[0] - self.neko.rect.center[0]) / move_distance #X移動方向
            move_y = (self.rect.center[1] - self.neko.rect.center[1]) / move_distance #Y移動方向
            self.x = -(move_x * self.speed) 
            self.y = -(move_y * self.speed) 
            self.image = img_move[0:len(img_move)][int((time/self.anime_speed_control)%len(img_move))]
    #####################不動###################
        else :
            self.image = img_idle[0:len(img_idle)][int((time /self.anime_speed_control)%len(img_idle))]
        
        
    ######################死亡#####################
        if self.blood <= 0 or self.mo[4]:
            if not self.mo[4]: 
                self.time_death = time
            self.mo[4] = 1
            self.image = img_death[0:len(img_death)][int(((time-self.time_death )/self.anime_speed_control)%len(img_death))]
            self.x, self.y  = 0, 0
            if self.image == img_death[-1]:
                self.kill()
    
    ######################受傷##################### 
        if self.mo[5] and not self.mo[4]:
            self.image = img_hit[0:len(img_hit)][int(((time - self.anime_time_hit) /self.anime_speed_control)%len(img_hit))]
            if self.image == img_hit[-1]:
                self.mo[5] = 0
                self.reset_hit_cd = 1
            if self.repel:
                a = ((-1)**self.mo[1]) * 10
                b = ( -1 * ((-1)**self.mo[1]) * (time-self.anime_time_hit) * 0.5 )
                self.x = a + b 
                if abs(a) <= abs(b):
                    self.x = 0
            else : self.x = 0
            self.y = 0
        if self.x > 0 and not self.mo[5]:
            self.mo[1], self.mo[2] = 1,0
        elif self.x < 0 and not self.mo[5]:
            self.mo[1], self.mo[2] = 0,1
    
    def colli_wall(self,map):
        wall = (1,2,3,4,5,6,7,8,13,14,15,16,17,18,19,20,21,25,26,27,28,29,30,31,32,33,34,35,37,38,39,40,41,42,43,44,45,49,50,51,52,53)
        YNotOverScreen = (self.rect.centery - map.rect.y)//80+1 < len(self.col_map)
        
        #踩地碰撞
        if self.rect.centery - map.rect.y>=0 \
            and self.rect.centery + self.y + self.bott>= ((self.rect.centery - map.rect.y)//80+1)*80 + map.rect.y \
            and YNotOverScreen \
            and ((self.col_map[(self.rect.centery - map.rect.y)//80+1][(self.rect.centerx-self.side - map.rect.x)//80] in wall) \
            or (self.col_map[(self.rect.centery - map.rect.y)//80+1][(self.rect.centerx+self.side-10 - map.rect.x)//80] in wall)):
            
            self.y = 0
            # self.rect.centery = (self.rect.centery//80)*80 +30
            
            
        else: pass
        #天花板碰撞
        if (self.rect.centery+45)//80 > 0 \
            and YNotOverScreen\
            and ((self.col_map[(self.rect.centery+45)//80-1][(self.rect.centerx-15 - map.rect.x)//80] in wall)\
            and self.y <= 0\
            or self.col_map[(self.rect.centery+45)//80-1][(self.rect.centerx+15 - map.rect.x)//80] in wall) :
            # and pg.sprite.collide_mask(self,self.map) :

            if self.y < 0 :self.y =0
        else : pass
        #左右碰撞
        if ((self.rect.centery+45)//80 > 0 \
            and YNotOverScreen\
            and (self.col_map[(self.rect.centery - map.rect.y)//80][((self.rect.centerx-self.side - map.rect.x)//80)+1] in wall)) \
            or (self.rect.centerx-30 - map.rect.x)//80 == len(self.col_map[0])-1:
            
            if self.x > 0 : self.x = 0
        else : pass

        if ((self.rect.centery+45)//80 > 0 \
            and YNotOverScreen\
            and (self.col_map[(self.rect.centery - map.rect.y)//80][((self.rect.centerx+self.side - map.rect.x)//80)-1] in wall) )\
            or (self.rect.centerx+50 - map.rect.x)//80 == 0:
            
            if self.x < 0 : self.x = 0
        else: pass

class Bear(monster):
    def __init__(self, coordinate, map_array):
        monster.__init__(self, 'Bear', map_array, coordinate)
        self.bott = 46
        self.rect.center = (80*coordinate[0],80*coordinate[1]+self.bott)
        self.speed = 3
        self.blood = 90*2
        self.side = 30
        self.damage_num = 8
class Worker_Mole(monster):
    def __init__(self,coordinate, map_array):
        monster.__init__(self, 'Worker Mole', map_array, coordinate)
        self.bott = 64
        self.rect.center = (80*coordinate[0],80*coordinate[1]+self.bott)
        self.speed = 3
        self.blood = 50*2
        self.side = 30
        self.damage_num = 4
class Ghost(monster):
    def __init__(self,coordinate, map_array):
        monster.__init__(self, 'Ghost', map_array, coordinate)
        self.bott = 64
        self.rect.center = (80*coordinate[0],80*coordinate[1]+self.bott)
        self.speed = 3
        self.blood = 30*2
        self.side = 30
        self.damage_num = 5
    def update(self, time, keys, map, neko = None , mon_spr = None):
        if neko != None:
            self.neko = neko[0]
        else:
            self.anime(time)
            self.colli_look()
            if not self.x :
                self.mo[0] = 1
            else: self.mo[0] = 0
            self.rect.x += self.x
            self.rect.y += self.y
    def anime(self, time):
        if self.mo[1] :
            img_idle = self.right_img_idle[:]
            img_move = self.right_img_move[:]
            img_death = self.right_img_death[:]
            img_hit = self.right_img_hit[:]
        else: 
            img_idle = self.img_idle[:]
            img_move = self.img_move[:]
            img_death = self.img_death[:]
            img_hit = self.img_hit[:]


        if not self.sleep :
            distance = ((self.rect.centerx - self.neko.rect.centerx)**2 + (self.rect.centery - self.neko.rect.centery)**2)**0.5
            if distance != 0 :
                move_distance = distance
            else :move_distance = 0.1
            move_x = (self.rect.center[0] - self.neko.rect.center[0]) / move_distance #X移動方向
            move_y = (self.rect.center[1] - self.neko.rect.center[1]) / move_distance #Y移動方向
            self.x = -(move_x * self.speed) 
            self.y = -(move_y * self.speed) 
            self.image = img_move[0:len(img_move)][int((time/self.anime_speed_control)%len(img_move))]
    #####################不動###################
        else :
            self.image = img_idle[0:len(img_idle)][int((time /self.anime_speed_control)%len(img_idle))]
        
        
    ######################死亡#####################
        if self.blood <= 0 or self.mo[4]:
            if not self.mo[4]: 
                self.time_death = time
            self.mo[4] = 1
            self.image = img_death[0:len(img_death)][int(((time-self.time_death )/self.anime_speed_control)%len(img_death))]
            self.x, self.y  = 0, 0
            if self.image == img_death[-1]:
                self.kill()
    
        ######################受傷##################### 
        if self.mo[5] and not self.mo[4]:
            self.image = img_hit[0:len(img_hit)][int(((time - self.anime_time_hit) /self.anime_speed_control)%len(img_hit))]
            if self.image == img_hit[-1]:
                self.mo[5] = 0
                self.reset_hit_cd = 1
            if self.repel:
                a = ((-1)**self.mo[1]) * 10
                b = ( -1 * ((-1)**self.mo[1]) * (time-self.anime_time_hit) * 0.5 )
                self.x = a + b 
                if abs(a) <= abs(b):
                    self.x = 0
            else : self.x = 0
            self.y = 0
        if self.x > 0 and not self.mo[5]:
            self.mo[1], self.mo[2] = 1,0
        elif self.x < 0 and not self.mo[5]:
            self.mo[1], self.mo[2] = 0,1

class Shark(monster):
    def __init__(self,coordinate, map_array):
        monster.__init__(self, 'Shark', map_array, coordinate)
        self.bott = 48
        self.rect.center = (80*coordinate[0],80*coordinate[1]+self.bott)
        self.speed = 3
        self.blood = 30*2
        self.side = 30
        self.damage_num = 15
class Golem(monster):
    def __init__(self,coordinate, map_array):
        monster.__init__(self, 'Golem', map_array, coordinate)
        self.bott = 48
        self.rect.center = (80*coordinate[0],80*coordinate[1]+self.bott)
        self.speed = 3
        self.blood = 1000
        self.side = 30
        self.damage_num = 8
