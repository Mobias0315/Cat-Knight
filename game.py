import pygame as pg
import os 
from Role import *
from neko import *
import colorsys

screen = pg.display.set_mode((1024,640))
pg.display.set_caption('Cat Knight')
pg.display.set_icon(pg.image.load(os.path.join('./img','icon.png')))
bg = pg.image.load(os.path.join('./img/background/Clouds/Clouds 1','bg.png')).convert_alpha()
screen.blit(bg, (0,0))
clock = pg.time.Clock()
fps = 60
pg.display.update()

def camera(keys, time, map, neko_list = None):

    if neko_list:
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
    pg.init()
    pg.font.init()
    bg_image = [pg.image.load(os.path.join('./img/title',f'title-export{i}.png')).convert_alpha() for i in range(1,7)]
    button_images = [pg.image.load(os.path.join('./img/title/Buttons', f'button{i}.png')).convert_alpha() for i in [1,2]]
    button_images = [pg.transform.scale(i, (200, 100)) for i in button_images]
    time = 0
    button_rect = pg.Rect(410, 400, button_images[0].get_width(), button_images[0].get_height())
    font = pg.font.Font('./ttf/Pixel.ttf', 58)
    titlefont = pg.font.Font('./ttf/AniMe_Matrix_Font_-_AIO.otf', 145)
    hue = 0
    title_turn = 1
    while title_turn:
        time += 1
        clock.tick(fps)  #偵率
        keys = pg.key.get_pressed()
        # 計算下一個色相
        hue = (hue + 1) % 360
        # 轉換色相為 RGB 值
        rgb = colorsys.hsv_to_rgb(hue / 360, 1, 1)
        color_value = tuple(int(i * 255) for i in rgb)
        title_font = text_image = titlefont.render('Cat Knight', True, color_value)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                close = 1
            # 檢測滑鼠點擊事件
            elif event.type == pg.MOUSEBUTTONDOWN:
                # 如果滑鼠點擊在按鈕上
                if button_rect.collidepoint(event.pos):
                    title_turn = 0
            if keys[pg.K_ESCAPE]:
                close = 1
        if close:
            break

        bg = bg_image[int(time / 6 %6)]
        screen.blit(bg, (0,-120))
        
        # 繪製按鈕
        if button_rect.collidepoint(pg.mouse.get_pos()):
            screen.blit(button_images[1], button_rect)
            text_image = font.render('開始', True, (200, 200, 200))
            screen.blit(text_image, (460, 425))
        else:
            screen.blit(button_images[0], button_rect)
            text_image = font.render('開始', True, (255, 255, 255))
            screen.blit(text_image, (460, 410))
        screen.blit(title_font, (60,20))
        pg.display.flip()
        pg.display.update()
def death(screen):
    global step
    alpha = 0
    fade_surface = pg.Surface(screen.get_size())
    fade_surface.fill((0, 0, 0))
    fade_surface.set_alpha(alpha)
    screen.blit(fade_surface, (0, 0))
    pg.display.flip()
    for i in range(180):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                close = 1
                break
        alpha += 1
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pg.time.wait(20)
        if i >= 100:
            font = pg.font.Font('./ttf/Pixel.ttf', 150)
            text = font.render("死亡", True, (255, 255, 255))
            text_rect = text.get_rect(center=screen.get_rect().center)
            screen.blit(text, text_rect)
        pg.display.flip()
    pg.time.wait(4000)
    step = 0
def pause_game():
    global close,step
    # 載入字型
    font = pg.font.Font('./ttf/Pixel.ttf', 58)
    text_image = font.render('継続', True, (255, 255, 255))
    text_image2 = font.render('退出', True, (255, 255, 255))
    text_rect = text_image.get_rect(center=screen.get_rect().center)
    text_rect2 = text_image2.get_rect(center=screen.get_rect().center)
    button_images = [pg.image.load(os.path.join('./img/title/Buttons', f'button{i}.png')).convert_alpha() for i in [1,2]]
    button_images = [pg.transform.scale(i, (200, 100)) for i in button_images]
    button_rect = pg.Rect(0, 0, button_images[0].get_width(), button_images[0].get_height())
    button_rect.center = screen.get_rect().center
    button_rect2 = pg.Rect(0, 0, button_images[0].get_width(), button_images[0].get_height())
    button_rect2.center = (screen.get_rect().centerx,screen.get_rect().centery+150)
    pause_bg = screen.copy()
    while 1:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                close = 1
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return
        screen.blit(pause_bg, (0,0))
        if button_rect.collidepoint(pg.mouse.get_pos()):
            screen.blit(button_images[1], button_rect)
            text_image = font.render('継続', True, (200, 200, 200))
            screen.blit(text_image, (text_rect[0]+8, text_rect[1]))
            if pg.mouse.get_pressed()[0]:
                return
        else:
            screen.blit(button_images[0], button_rect)
            text_image = font.render('継続', True, (255, 255, 255))
            screen.blit(text_image, (text_rect[0]+8, text_rect[1]-15))

        if button_rect2.collidepoint(pg.mouse.get_pos()):
            screen.blit(button_images[1], button_rect2)
            text_image = font.render('退出', True, (200, 200, 200))
            screen.blit(text_image, (text_rect[0]+8, text_rect[1]+150))
            if pg.mouse.get_pressed()[0]:
                step = 0
                break
        else:
            screen.blit(button_images[0], button_rect2)
            text_image = font.render('退出', True, (255, 255, 255))
            screen.blit(text_image, (text_rect[0]+8, text_rect[1]-15+150))
        if close : break
        pg.display.flip()
        pg.display.update()
step = 0
def game_turn():
    global step,time
    if step == 0:
        for i in all_spr.sprites():
            i.kill()
        time = 0
        title()
        step+=1
    elif step == 1:
        map_ = map()
        all_spr.add(map_)
        for i in map_.role_list:
            box = i
            all_spr.add(box) 
            mon_spr.add(box)
        for i in map_.play_list:
            box = i
            all_spr.add(box)
            play_spr.add(box)
        map_spr.add(map_)
        step+=1
    elif step == 2:
        for i in play_spr:
            if i.over:
                death(screen)
    elif step == 3:
        print(1)
def change_map(neko, map):
    if neko and map:
        neko = neko[0]
        map = map[0]
        coor = ((neko.rect.centerx+50 - map.rect.x)//80, (neko.rect.centery - map.rect.y)//80)
        if map.map_name == 'map1':
            if coor[0] == len(map.a[0][0]) and coor[1] in range(0,7):
                return 'map2', [1, 18], (0, -13*80) 
            
        elif map.map_name == 'map2':
            if coor[0] == 0 and coor[1] in range(10,19):
                return 'map1', [44, 6], (-(44-11)*80, -80)
            elif coor[0] == 0 and coor[1] in range(5):
                return 'map3', [11, 5], (0, 0)
            elif coor[0] == 19 and coor[1] in range(13,15):
                return 'map5', [1, 10], (0, -5*80)
            elif coor[0] == 19 and coor[1] == 16:
                return 'map5', [1, 12], (0, -5*80)
            
        elif map.map_name == 'map3':
            if coor[0] in range(15) and coor[1] == 8:
                return 'map1', [coor[0], 0], (0, 80)
            elif coor[0] == 13 and coor[1] in range(6):
                return 'map2', [1, 3], (0, 0) 
            elif coor[0] in range(14) and coor[1] == 0:
                return 'map4', [6, 7], (0,0)
            
        elif map.map_name == 'map4':
            if coor[0] == 0 and coor[1] in range(12):
                return 'map4', [14, coor[1]], (-80, 0)
            elif coor[0] in range(13) and coor[1] == 9:
                return 'map3', [4, 1], (0, 0)
            # elif coor[0] in range(14) and coor[1] == 0:
            #     return 'map4', [6, 7], (0,0)
        elif map.map_name == 'map5':
            if coor[0] == 0 and coor[1] in range(11):
                return 'map2', [17, 14], (-4*80, -12*80)
            elif coor[0] == 0 and coor[1] == 12:
                return 'map2', [17, 16], (-4*80, -12*80)
            elif coor[0] == 27 and coor[1] in range(6):
                return 'map6', [1, 6], (0, 0)
            elif coor[0] in range(10,15) and coor[1] == 13:
                return 'map7', [coor[0]-10, 0], (0, 0)
            
        elif map.map_name == 'map6':
            if coor[0] == 0 and coor[1] in range(7):
                return 'map5', [25, 5], (-15*80, 0)
            elif coor[0] == 0 and coor[1] in range(7):
                return 'map5', [25, 5], (-15*80, 0)
            elif coor[0] == 13 and coor[1] in range(7):
                return 'map8', [1, 6], (0, 0)
            
        elif map.map_name == 'map7':
            if coor[0] == 33 and coor[1] == 0:
                return 'map8', [12, 9], (0, -80)
            
        elif map.map_name == 'map8':
            if coor[0] == 0 and coor[1] in range(7):
                return 'map6', [11, 6], (0, 0)
            elif coor[0] in range(13) and coor[1] == 10:
                return 'map7', [20+coor[0], 0], (-20*80, 0)

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
    game_turn()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            close = True
            pg.quit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_F5:
                step = 0
            elif event.key == pg.K_ESCAPE:
                pause_game()
    if close : break

    map_next = change_map([i for i in play_spr], [i for i in map_spr])
    if map_next:
        neko_blood = [i.blood for i in play_spr]
        for i in all_spr.sprites():
            i.kill()
        map_ = map(map_name = map_next[0], neko_next = map_next[1],neko_blood = neko_blood[0])
        all_spr.add(map_)
        for i in map_.role_list:
            box = i
            all_spr.add(box) 
            mon_spr.add(box)
        for i in map_.play_list:
            box = i
            all_spr.add(box)
            play_spr.add(box)
        map_spr.add(map_)
        step = 2
        for i in all_spr.sprites():
            i.rect.centerx += map_next[2][0]
            i.rect.centery += map_next[2][1]
    camera(keys, time, [i for i in map_spr], [i for i in play_spr])
    screen.blit(bg, (0,0))
    if not map_next:
        mon_spr.update( time, keys, [i for i in map_spr], [i for i in play_spr] )
        all_spr.update( time, keys, [i for i in map_spr], mon_spr = mon_spr )
        all_spr.draw(screen)
    pg.display.flip()
    pg.display.update()
    