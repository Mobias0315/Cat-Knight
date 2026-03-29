import pygame as pg
import os 
from Role import *
from neko import *
pg.init()
screen = [1024,640]
screen[0] += 200
screen = pg.display.set_mode(screen)
pg.display.set_caption('creat map')
bg = pg.image.load(os.path.join('./img/background/Clouds/Clouds 1','bg.png')).convert_alpha()
screen.blit(bg, (0,0))
clock = pg.time.Clock()
fps = 60
pg.display.update()

def camera(keys, time, map, neko_list = None):
    if neko_list and not close:
        
        map = map[0]
        neko = neko_list[0] 
        
        if (neko.rect.centerx >= 1024*0.7 and neko.x>0 and (len(map.a[0][0]) -0.1) * 80 + map.rect.x > 1024)\
            or (neko.rect.centerx <= 1024*0.3 and neko.x<0 and map.rect.x < 0): 
            for i in all_spr:
                i.rect.centerx -= neko.x
        elif (neko.rect.centerx >= 1024*0.7) and (len(map.a[0][0]) -0.1) * 80 + map.rect.x > 1024:
            for i in all_spr:
                i.rect.centerx -= 10
                
        if (neko.rect.centery >= screen.get_rect()[3]*0.7 and neko.y > 0 and (len(map.a[0]) -0.1) * 80 + map.rect.y > screen.get_rect()[3])\
            or (neko.rect.centery <= screen.get_rect()[3]*0.3 and neko.y < 0 and map.rect.y < 0): 
            for i in all_spr:
                i.rect.centery -= neko.y
        elif (neko.rect.centery >= screen.get_rect()[3]*0.7 and (len(map.a[0]) -0.1) * 80 + map.rect.y > screen.get_rect()[3]):
            for i in all_spr:
                i.rect.centery -= 10 
def title() :
    global close
    while 1:
        clock.tick(fps)  #偵率
        keys = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                close = 1
        if close:break

        
        screen.blit(bg, (0,0))

        pg.display.update()

step = 0
now_array = None
def game_turn():
    global step,time,map_put, map_se,now_array,map_spr
    if step ==0:
        [i.kill() for i in all_spr]
        chose_map_spr.empty()
        map_put = put_map(now_array)
        map_se = chose_map()
        chose_map_spr.add(map_put, map_se)
        map_put.DrawOnbd()
        maker()
        time = 0
    elif step == 1: 
        step+=1
    elif step == 2:
        now_array = map_put.array
        map_spr.empty()
        map_ = map(now_array)
        map_spr.add(map_)
        all_spr.add(map_)
        for i in map_.role_list:
            box = i
            all_spr.add(box) 
            mon_spr.add(box)
        for i in map_.play_list:
            box = i
            all_spr.add(box)
            play_spr.empty()
            play_spr.add(box)
        

        step+=1
    elif step == 3:
        for i in play_spr:
            if i.over:
                step += 1
    elif step == 4:
        pass
def maker_camera(keys):
    if (keys[pg.K_LEFT] or keys[pg.K_a]) and map_put.rect.left < 0:
        map_put.x = 10
    elif (keys[pg.K_RIGHT] or keys[pg.K_d]) and map_put.rect.right > 1024:
        map_put.x = -10
    else: map_put.x = 0 

    if map_put.rect.left > 0 :
        map_put.rect.left = 0
    elif map_put.rect.right < 1024:
        map_put.rect.right = 1024

    if (keys[pg.K_UP] or keys[pg.K_w])and map_put.rect.top < 0:
        map_put.y = 10
    elif (keys[pg.K_DOWN] or keys[pg.K_s]) and map_put.rect.bottom >640:
        map_put.y = -10
    else: map_put.y = 0 

    if map_put.rect.top > 0 :
        map_put.rect.top = 0
    elif map_put.rect.bottom < 640:
        map_put.rect.bottom = 640
def stockpile(text = None, read = None):
    global map_put, menu_items, now_array
    if text is not None and text is not '':
        with open(f'map\{text}.txt','w',encoding='utf-8') as w:
            a = ''
            for i in map_put.array:
                for j in i :
                    a += str(j)+', '
                a = a[:-2] + '\n'
            w.write(a[:-1])
        menu_items = [i.replace('.txt','') if '.txt' in i else i for i in os.listdir('./map')]
    if read is not None:
        with open(f'map\{read}.txt','r',encoding='utf-8') as r:
            a = [list(eval(i)) for i in r.read().split('\n')]
            map_put.arr_chance(a)
            now_array = a

def maker():
    global close, step, menu_items
    text = '檔案名稱'
    textcopy = text
    input_rect = pg.Rect(1024, 550, 140, 32)
    font = pg.font.SysFont('SimSun', 24)
    color_inactive = pg.Color('lightskyblue3')
    color_active = pg.Color('dodgerblue2')
    color = color_inactive

    menu_items = [i.replace('.txt','') if '.txt' in i else i for i in os.listdir('./map')]
    menu_rect = pg.Rect(1024, 580, 140, 32)
    menu_font = pg.font.SysFont('SimSun', 24)
    menu_color = pg.Color('lightskyblue3')
    menu_active_color = pg.Color('dodgerblue2')
    menu_active = False
    menu_selection = None
    item_rects = []
    selected_item = None

    arrow_img = pg.transform.scale(pg.image.load('./img/arrow.png'),(40,40))
    arrow_rect = arrow_img.get_rect()
    arrow_rect.center = (1200, 580)
    font = pg.font.SysFont('SimSun', 24)
    text_color = pg.Color('white')
    maker_loop = 1
    time = 0
    while maker_loop:
        time += 1
        keys = pg.key.get_pressed()
        mouses = pg.mouse.get_pressed()
        maker_camera(keys)
        clock.tick(fps)  #偵率 
        if time % 600==0 and text != '檔案名稱' and text != '':
            stockpile(text)
            
        for event in pg.event.get():
            mousepos = pg.mouse.get_pos()
            if mousepos[0] in range(1024,1225):
                if event.type == pg.MOUSEWHEEL and  -(61*12 -200) <= map_se.x <= 0:
                    map_se.x += event.y *50
                if -(61*12-200) > map_se.x:
                    map_se.x = -(61*12-200)
                elif map_se.x > 0:
                    map_se.x = 0
                if event.type == pg.MOUSEBUTTONDOWN:
                    map_put.img_id( map_se.chose(mousepos))

            if mousepos[0] < 1024:
                map_put.preview(mousepos)
                if 1 in keys and 1 in mouses:
                    map_put.array_modify(keys , mouses, event)
                elif mouses[0]:
                    map_put.chose( mousepos )
                elif mouses[2]:
                    map_put.right_mou( mousepos )
        
            if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
                close = True
            ##########輸入#########
            if event.type == pg.MOUSEBUTTONDOWN:
                color = color_active if input_rect.collidepoint(event.pos) else color_inactive
                text = '' if input_rect.collidepoint(event.pos) else text
                
            if event.type == pg.KEYDOWN and color == color_active:
                if event.key == pg.K_RETURN:
                    stockpile(text = text)
                    textcopy = text
                elif event.key == pg.K_BACKSPACE:
                    text = text[:-1]
                else:
                    time = 0
                    text += event.unicode
            elif color == color_inactive : 
                text = textcopy

            ##########式玩#########
            if event.type == pg.MOUSEBUTTONDOWN:
                if arrow_rect.collidepoint(event.pos):
                    step += 1
                    maker_loop = 0
            #########選單##########
                if menu_rect.collidepoint(event.pos):
                    menu_active = not menu_active
                else:
                    menu_active = False
                for i, item_rect in enumerate(item_rects):
                    if item_rect.collidepoint(event.pos):
                        menu_selection = i
                        menu_active = False
                        selected_item = menu_items[menu_selection]
                        stockpile(read = selected_item)
                        textcopy = '檔案名稱'
                if not menu_active:
                    menu_selection = None
                    item_rects = []

        if close:break
        #########畫面更新
        screen.blit(bg, (0,0))
        chose_map_spr.update()
        chose_map_spr.draw(screen)
        #########輸入
        pg.draw.rect(screen, color, input_rect, 2)
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        #########式玩
        screen.blit(arrow_img, arrow_rect)
        #########選單
        pg.draw.rect(screen, menu_color, menu_rect, 2)
        if selected_item is not None:
            menu_text = menu_font.render(selected_item, True, menu_color)
        else:
            menu_text = menu_font.render('請選擇...', True, menu_color)
        screen.blit(menu_text, (menu_rect.x + 5, menu_rect.y + 5))
        if menu_active:
            item_rects = []
            for i, item in enumerate(menu_items):
                item_rect = pg.Rect(menu_rect.x, menu_rect.y - (len(menu_items) - i) * menu_rect.height, menu_rect.width, menu_rect.height)
                pg.draw.rect(screen, menu_active_color if i == menu_selection else menu_color, item_rect)
                item_text = menu_font.render(item, True, pg.Color('white'))
                screen.blit(item_text, (item_rect.x + 5, item_rect.y + 5))
                item_rects.append(item_rect)
        

        pg.display.flip()
        pg.display.update()
class chose_map(pg.sprite.Sprite):
    def __init__(self) :
        pg.sprite.Sprite.__init__(self)
        self.img =  [pg.transform.scale(i, (60,60)) for i in [pg.image.load(os.path.join('./img/Green World - Tileset/map','Green World - Tileset%d.png'%i)).convert_alpha() for i in range(1,109)]]
        self.bg = pg.Surface((200,640))
        self.bg2 = pg.Surface((61*12,640))
        self.bg2.fill((255,255,255))
        self.bg.fill((255,255,255))
        try:
            for j in range(80):
                for i in range(0 + 12 *j  ,0 + 12 *(j+1) ):
                    self.bg2.blit(self.img[i], (0+61*(i%12),0 + 61*j) )
        except:
            pass
        self.bg.blit(self.bg2,(0,0))
        self.image = self.bg
        self.rect = self.image.get_rect()
        self.rect.x , self.rect.y = 1024,0
        self.x ,self.y =0, 0
        
    def update(self):
        self.bg.blit(self.bg2,(self.x, self.y))
    
    def chose(self, pos):
        self.bg2.fill((255,255,255))
        try:
            for j in range(80):
                for i in range(0 + 12 *j  ,0 + 12 *(j+1) ):
                    self.bg2.blit(self.img[i], (0+61*(i%12),0 + 61*j) )
        except:
            pass
        pos = list(pos)
        pos[0] -= self.rect.x
        if pos[1] < 61 * 9:
            self.bg2.blit(self.img[9],(((pos[0] - self.x) // 61)*61, ((pos[1] // 61))*61))
            return (pos[1] // 61)*12 + ((pos[0] - self.x) // 61)
    
class put_map(pg.sprite.Sprite):
    def __init__(self, now_array):
        pg.sprite.Sprite.__init__(self)
        self.img =  [i for i in [pg.image.load(os.path.join('./img/Green World - Tileset/map','Green World - Tileset%d.png'%i)).convert_alpha() for i in range(1,109)]]
        self.array = [[0 for _ in range(13)] for _ in range(8*3)]
        if now_array is not None:
            self.array = now_array
        self.bg = pg.Surface((80 * len(self.array[0]) ,  len(self.array)//3*80 )).convert_alpha()
        self.bg.set_colorkey((0,0,0))
        # self.bg.blit(self.background, (0, 0))
        self.image = self.bg
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0
        self.x, self.y = 0, 0
        self.id = 1
        self.copy_map = self.bg.copy()
    def update(self):
        self.rect.x += self.x
        self.rect.y += self.y
        self.image = self.bg

    def chose(self, pos):
        if (self.id in (1,2,3,4,5,6,7,8,13,14,15,16,17,18,19,20,21,25,26,27,28,29,30,31,32,33,34,35,37,38,39,40,41,42,43,44,45,49,50,51,52,53) or self.id in range(97,108) ) and self.id != 105:
            self.array[(pos[1]-self.rect[1]) // 80 + len(self.array)//3][(pos[0]-self.rect[0]) // 80] = self.id
        elif self.id in (61, 62, 63, 64, 65, 73, 74, 75, 76, 77, 85, 86, 87, 88, 89) :
            self.array[(pos[1]-self.rect[1]) // 80 ][(pos[0]-self.rect[0]) // 80] = self.id
        elif self.id in (9, 21, 47, 54, 55, 56, 57, 59, 60, 66, 67, 68, 71, 72, 78, 79, 80, 81, 82, 83, 84, 90, 91, 92, 93, 94, 95, 96):
            self.array[(pos[1]-self.rect[1]) // 80 + len(self.array)//3*2][(pos[0]-self.rect[0]) // 80] = self.id
        elif self.id in range(22,25):
            self.array[(pos[1]-self.rect[1]) // 80 + len(self.array)//3*(self.id - 22)][(pos[0]-self.rect[0]) // 80] = 0
        elif self.id == 10:
            for i in range(3):
                self.array[(pos[1]-self.rect[1]) // 80 + len(self.array)//3*i][(pos[0]-self.rect[0]) // 80] = 0
        self.DrawOnbd()
    def img_id(self, id):
        try:
            self.id = id+1
        except:
            pass
    def preview(self, pos):
        self.bg = self.copy_map.copy()
        self.bg.blit(self.img[self.id-1],( ((pos[0]-self.rect[0]) // 80 )*80 ,((pos[1]-self.rect[1]) // 80 )*80 ))

    def DrawOnbd(self):
        self.bg = pg.Surface((80 * len(self.array[0]) , 80 * (len(self.array)//3))).convert_alpha()
        self.bg.set_colorkey((0,0,0))
        self.a = [ self.array[0:len(self.array)//3] ,self.array[len(self.array)//3:(len(self.array)//3)*2] ,self.array[(len(self.array)//3)*2:] ]
        for i in range(len(self.a)):
            for j in range(len(self.a[i])):
                for k in range(len(self.a[i][j])):
                    if self.a[i][j][k] == 0 : continue
                    else:
                        self.bg.blit(self.img[self.a[i][j][k]-1],(k*80,j*80))
        self.copy_map = self.bg.copy()
    def right_mou( self, pos):
        if (self.id in (1,2,3,4,5,6,7,8,13,14,15,16,17,18,19,20,21,25,26,27,28,29,30,31,32,33,34,35,37,38,39,40,41,42,43,44,45,49,50,51,52,53) or self.id in range(97,108) ) and self.id != 105:
            self.array[(pos[1]-self.rect[1]) // 80 + len(self.array)//3][(pos[0]-self.rect[0]) // 80] = 0
        elif self.id in (61, 62, 63, 64, 65, 73, 74, 75, 76, 77, 85, 86, 87, 88, 89) :
            self.array[(pos[1]-self.rect[1]) // 80 ][(pos[0]-self.rect[0]) // 80] = 0
        elif self.id in (9, 21, 47, 54, 55, 56, 57, 59, 60, 66, 67, 68, 71, 72, 78, 79, 80, 81, 82, 83, 84, 90, 91, 92, 93, 94, 95, 96):
            self.array[(pos[1]-self.rect[1]) // 80 + len(self.array)//3*2][(pos[0]-self.rect[0]) // 80] = 0
        self.DrawOnbd()
    def array_modify(self, keys , mouses , event):

        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                for i in self.array:
                    i.append(0)
            elif keys[pg.K_LEFT] or keys[pg.K_a]:
                for i in self.array:
                    i.insert(0,0)
            elif keys[pg.K_UP] or keys[pg.K_w]:
                z = len(self.array) // 3
                for i in range(2,-1,-1):
                    self.array.insert(z * i, [0 for _ in range(len(self.array[0]))])
            elif keys[pg.K_DOWN] or keys[pg.K_s]:
                z = len(self.array) // 3
                for i in range(3,0,-1):
                    self.array.insert(z * i, [0 for _ in range(len(self.array[0]))])
        if event.type == pg.MOUSEBUTTONUP and event.button == 3:
            if (keys[pg.K_RIGHT] or keys[pg.K_d])and len(self.array[0])>13:
                for i in self.array:
                    i.pop(-1)
            elif (keys[pg.K_LEFT] or keys[pg.K_a])and len(self.array[0])>13:
                for i in self.array:
                    i.pop(0)
            elif (keys[pg.K_UP] or keys[pg.K_w])and len(self.array)//3>8:
                z = len(self.array) // 3
                for i in range(2,-1,-1):
                    self.array.pop(z * i)
            elif (keys[pg.K_DOWN] or keys[pg.K_s])and len(self.array)//3>8:
                z = len(self.array) // 3
                for i in range(3,0,-1):
                    self.array.pop(z * i-1)
        x,y = self.rect.x,self.rect.y
        self.bg = pg.Surface((80 * len(self.array[0]) , 80 * (len(self.array)//3))).convert_alpha()
        self.bg.set_colorkey((0,0,0))
        self.image = self.bg
        self.rect = self.image.get_rect()
        self.rect.x ,self.rect.y = x,y
        self.DrawOnbd()
    def arr_chance(self,a):
        self.array = a
        self.DrawOnbd()
        self.bg = pg.Surface((80 * len(self.array[0]) , 80 * (len(self.array)//3))).convert_alpha()
        self.bg.set_colorkey((0,0,0))
        self.image = self.bg
        self.rect = self.image.get_rect()
        self.rect.x ,self.rect.y = 0,0
chose_map_spr = pg.sprite.Group()


#########################################
all_spr = pg.sprite.Group()
play_spr = pg.sprite.Group()
map_spr = pg.sprite.Group()
mon_spr = pg.sprite.Group()

close = 0
time = 0
while 1:
    time +=1
    keys = pg.key.get_pressed()
    clock.tick(fps)  #偵率 
    
    if keys[pg.K_F5]:
        step = 0
    
    game_turn()
    for event in pg.event.get():
        if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
            close = 1
            pg.quit()
    if close:break
    camera(keys, time, [i for i in map_spr], [i for i in play_spr])
    
    screen.blit(bg, (0,0))
    
    mon_spr.update(time, keys, [i for i in map_spr], [i for i in play_spr])
    all_spr.update(time, keys, [i for i in map_spr], mon_spr = mon_spr)
    all_spr.draw(screen)
    screen.blit(map_se.bg,(1024,0))
    pg.display.flip()
    pg.display.update()
    