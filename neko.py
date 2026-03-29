import pygame as pg
import os 

class neko(pg.sprite.Sprite):
    def __init__(self, coordinate, map_array, blood) : #地圖上97位置座標   地圖的矩陣
        pg.sprite.Sprite.__init__(self)
        self.img =  [pg.image.load(os.path.join('./img/meow knight','Meow_Knight%d.png'%i)).convert_alpha() for i in range(1,70)]
        self.left_img = [pg.transform.flip(i,1,0) for i in self.img]
        self.image = self.img[0]
        self.mo = [1,1,0,0,0,0,0,0,1,0, 0, 0, 0, 0] #狀態標籤 : stop right left up down z x c 是否為自然落下 左邊是否有牆 右邊是否有牆 上方是否有牆 hit death
                #  0,1,2,3,4,5,6,7,8,9,10,11,12,13               0    1     2   3   4  5 6 7      8             9         10            11     12   13
        self.rect = self.image.get_rect()
        self.rect.center = (80*coordinate[0]+45, 80*coordinate[1]+30)
        self.anime_time = 0   # 動畫初始化用
        self.jump_time = 0    # 跳躍用
        self.x_twice = 0      # 二次 X
        self.speed = 7
        self.g = 0.4
        self.anime_speed_control = 5
        self.col_map = map_array[1]
        self.x ,self.y = 0,0
        self.cd_c = [0, 30]   # 計算時間用 / cd時長(fps)
        self.cd_x = [0, 45]
        self.damage = [6, 2, 10] # z x down 
        self.blood = blood
        self.hit_cd = 45
        self.anime_time_hit = 0
        self.over = 0

    def update(self, time, keys, map, mon_spr = None):
        self.anime(time, keys, mon_spr)
        self.colli(time, map[0])
        self.rect.x += self.x
        self.rect.y += self.y
        if (self.rect.centery - map[0].rect.y)//80 > len(self.col_map)+5 or self.blood <= 0:
            self.blood = 0
        pg.draw.line(self.image, (255, 255, 255), (165,150), (225,150), 6)
        pg.draw.line(self.image, (230, 0, 0), (165,150), (165 + (self.blood / 200)*(225-165),150), 6)
    def anime(self, time, keys, mon_spr): 
        
        if self.mo[2]:
            img = self.left_img[:]
        else : img = self.img[:] 

        ####################不動#################################

        if self.mo[0] and sum(self.mo[1:8])==1:
            self.image = img[8:14][int((time/self.anime_speed_control)%6)]
        
        #####################跳及墜落################################

        if keys[pg.K_DOWN] and self.mo[3] and not self.mo[5] or self.mo[4]:
            self.anime_time_hit = time
            if not self.mo[4] or self.image == img[54]:
                self.anime_time_down = time
            self.mo[4] = 1
            self.image = img[52:55][int(((time - self.anime_time_down)/self.anime_speed_control)%3)]
            self.y = 15                #下降速度
            if not self.mo[3] :
                self.image = img[55:60][int(((time - self.anime_time_down)/self.anime_speed_control)%5)]
                for monster in mon_spr:
                    if pg.sprite.collide_mask(self, monster):
                        monster.hit(time,self.damage[2])
                self.y = 0
            if self.image == img[59]:
                self.mo[0],self.mo[4] = 1,0

        elif self.mo[3] and not self.mo[4] and self.mo[8]:
            self.mo[0]= 0
            
            if  (time - self.jump_time) * self.g > 0 and not self.mo[6] : 
                if self.image in img[21:23]:
                    self.image = img[21:23][int(((time - self.anime_time)/self.anime_speed_control)%2)]
                else:self.image = img[19:23][int(((time - self.anime_time)/self.anime_speed_control)%4)]
            elif not self.mo[6]: self.image = img[14:21][int(((time - self.anime_time)/self.anime_speed_control)%7)]
            self.y = (time - self.jump_time) * self.g
        
        elif keys[pg.K_UP] and not self.mo[4] and not self.mo[7] and not self.mo[5] or self.mo[3] :
            self.mo[8],self.mo[0] = 0,0
            if not self.mo[3]:
                self.anime_time_up = time
                self.jump_time = time
            if self.image == img[20] and self.y <= 0 :
                self.image = img[20]
            elif  self.y > 0 and not self.mo[6]: 
                self.image = img[21:23][int(((time - self.anime_time_up)/self.anime_speed_control)%2)]
            elif not self.mo[6]: self.image = img[14:21][int(((time - self.anime_time_up)/self.anime_speed_control)%7)]

            self.y = (-(self.speed+6))+((time - self.jump_time) * self.g)
            
        else : self.y = 0
        
                
        ####################翻滾及移動#################################

        if keys[pg.K_c] and not self.mo[4] and not self.mo[3] and not self.mo[5] and time - self.cd_c[0] > self.cd_c[1] or self.mo[7]:
            self.anime_time_hit = time
            self.cd_c[0] = time
            if not self.mo[7]:
                self.anime_time_c = time
            self.mo[7] = 1
            self.image = img[36:44][int(((time - self.anime_time_c)/(self.anime_speed_control)*1.5)%8)]
            if self.image == img[43]:
                self.mo[7] = 0

            if self.mo[1]:
                self.x = self.speed + 2
            else : self.x = -(self.speed + 3)
        
        elif keys[pg.K_RIGHT] and not self.mo[4] and not self.mo[10] and not self.mo[13]:
            self.mo[0] ,self.mo[1] ,self.mo[2] = 0 ,1 ,0
            if not self.mo[3] and not self.mo[5] and not self.mo[6]:
                self.image = img[0:8][int((time/self.anime_speed_control)%8)]
            self.x = self.speed
        elif keys[pg.K_LEFT] and not self.mo[4] and not self.mo[9] and not self.mo[13]:
            self.mo[0] ,self.mo[1] ,self.mo[2] = 0 ,0 ,1
            if not self.mo[3] and not self.mo[5] and not self.mo[6]:
                self.image = img[0:8][int((time/self.anime_speed_control)%8)]
            self.x = -self.speed
        else: 
            self.mo[0],self.x = 1,0 
        #################### z 攻擊 #################################
        
        if keys[pg.K_z] and not self.mo[7] and not self.mo[4] and not self.mo[6] or self.mo[5]:
            self.anime_time_hit = time -30
            if not self.mo[5]:
                self.anime_time_z = time
                
            self.mo[5] = 1
            self.image = img[26:36][int(((time - self.anime_time_z)/(self.anime_speed_control))%10)]
            if self.image == img[35]:
                self.mo[5] = 0
            if self.image in img[30:36]:
                for monster in mon_spr:
                    if pg.sprite.collide_mask(self, monster):
                        monster.hit(time, self.damage[0], repel = True)
            if not self.mo[3]:
                self.x = 0
        #################### x 攻擊 #################################
        if keys[pg.K_x] and not self.mo[7] and not self.mo[5] and not self.mo[4] and time - self.cd_x[0] > self.cd_x[1] or self.mo[6] :
            self.anime_time_hit = time -30
            if not self.mo[6]:
                self.x_up = 0
                self.anime_time_x = time
                self.cd_x[0] = time
            self.mo[6] = 1

            if self.x_twice and self.image == img[47] or self.image in img[48:52]:
                if self.image == img[47]:
                    self.anime_time_x = time
                self.image = img[48:52][int(((time - self.anime_time_x)/(self.anime_speed_control))%4)]
                for monster in mon_spr:           
                    if pg.sprite.collide_mask(self, monster):
                        monster.hit(time, self.damage[1], reset= True)
            else:
                self.image = img[44:48][int(((time - self.anime_time_x)/(self.anime_speed_control))%4)]
                if self.image != img[44]:
                    for monster in mon_spr:
                        if pg.sprite.collide_mask(self, monster):
                            monster.hit(time,self.damage[1])
            if self.image == img[51] or (not self.x_twice and self.image == img[47]) or self.mo[5] or self.mo[7] or self.mo[4]:
                self.mo[6] = 0
                self.x_twice = 0
            
            if not keys[pg.K_x] :
                self.x_up = 1
            elif self.x_up and keys[pg.K_x]:
                self.x_twice = 1
        #################### 受傷 #################################        
        if self.mo[12] and not self.mo[13] and not self.mo[4] and not self.mo[5] and not self.mo[6] and not self.mo[7]  :
            anime = int(((time - self.anime_time_hit)/(self.anime_speed_control))%3)
            self.image = img[60:63][anime]
            if anime == 2:
                self.mo[12] = 0

            if self.repel:
                a = ((-1)**self.mo[1]) * 10
                b = ( -1 * ((-1)**self.mo[1]) * (time-self.anime_time_hit) * 0.5 )
                self.x = a + b 
                if abs(a) <= abs(b):
                    self.x = 0
        if self.y >=20:
            self.y = 20
        #################### 死亡 #################################     
        if self.blood <= 0 or self.mo[13]:
            if not self.mo[13]: 
                self.time_death = time
                self.anime_speed_control = 20
            self.mo[13] = 1
            
            self.image = img[63:69][int(((time - self.time_death) /self.anime_speed_control)%6)]
            if self.image == img[68] or self.over:
                self.image = img[68]
                self.over = 1

            self.x, self.y  = 0, 0

    def colli(self, time, map):
        wall = (1,2,3,4,5,6,7,8,13,14,15,16,17,18,19,20,25,26,27,28,29,30,31,32,33,34,35,37,38,39,40,41,42,43,44,45,49,50,51,52,53)
        YNotOverScreen = (self.rect.centery - map.rect.y)//80+1 < len(self.col_map)
        #踩地碰撞
        if self.rect.centery >=0 \
            and self.rect.centery+self.y >= ((self.rect.centery - map.rect.y)//80)*80 +30 + map.rect.y \
            and YNotOverScreen \
            and ((self.col_map[(self.rect.centery - map.rect.y)//80+1][(self.rect.centerx-15 - map.rect.x)//80] in wall) \
            or (self.col_map[(self.rect.centery - map.rect.y)//80+1][(self.rect.centerx+15 - map.rect.x)//80] in wall)):
            
            self.y = 0
            self.rect.centery = ((self.rect.centery - map.rect.y)//80)*80 +30 + map.rect.y
            
            self.anime_time = 0
            self.mo[3],self.mo[8] = 0,1
            self.jump_time = time
        else: 
            self.mo[3] = 1
            self.mo[7] = 0
        #天花板碰撞
        if (self.rect.centery+45)//80 > 0 \
            and YNotOverScreen\
            and ((self.col_map[(self.rect.centery+45 - map.rect.y)//80-1][(self.rect.centerx-15 - map.rect.x)//80] in wall)\
            and self.y <= 0\
            or self.col_map[(self.rect.centery+45 - map.rect.y)//80-1][(self.rect.centerx+15 - map.rect.x)//80] in wall) :

            self.mo[11] = 1
            if self.y < 0 :self.y =0
        else : self.mo[11] =0
        #左右碰撞
        if ((self.rect.centery+45)//80 > 0 \
            and YNotOverScreen\
            and (self.col_map[(self.rect.centery - map.rect.y)//80][((self.rect.centerx-50 - map.rect.x)//80)+1] in wall)) \
            or (self.rect.centerx-30 - map.rect.x)//80 == len(self.col_map[0])-1:
            
            self.mo[10] = 1
            if self.x > 0 : self.x = 0
        else : self.mo[10] = 0 

        if ((self.rect.centery+45)//80 > 0 \
            and YNotOverScreen\
            and (self.col_map[(self.rect.centery - map.rect.y)//80][((self.rect.centerx+50 - map.rect.x)//80)-1] in wall) )\
            or (self.rect.centerx+50 - map.rect.x)//80 == 0:
            
            self.mo[9] = 1
            if self.x < 0 : self.x = 0
        else: self.mo[9] =  0
        
    def hit(self, time, damage, repel = False):
        self.repel = repel
        if  time - self.anime_time_hit >= self.hit_cd :
            self.anime_time_hit = time
            self.mo[12] = 1
            self.blood -= damage
