import pyautogui as pya
import time, asyncio
import pygame as pg
import pygame.display as pgd

version = '0.1.2'

all_lock = False
roses = 0; rose_6_lock = False; rose_30_lock = False
mush = 0; mush_lock = False
time_points = 0; time_point_lock = False
rosevines = 0; rosevine_lock = False
goodybags = 0; goodybag_lock = False
match_timer = 0; letter_timer = 0

match_check = False; minigame = [[None, None, None, None],
                                 [None, None, None, None],
                                 [None, None, None, None]]

async def rose_check():
    global roses, rose_6_lock, rose_30_lock, minigame
    pos = pya.locateOnScreen('a\\rose.png', confidence = 0.7)
    if pos is not None and rose_30_lock == False:
        amount_pos = pya.locateOnScreen('a\\thirty.png', confidence = 0.6, region = (0, 0, 250, pya.size()[1]))
        if amount_pos is not None:
            print("Gained 30 roses."); roses += 30; rose_30_lock = True
            match_check = False; await letter_check()
            minigame = [[None, None, None, None],
                        [None, None, None, None],
                        [None, None, None, None]]
            render()
            await asyncio.sleep(2.25); rose_30_lock = False
        else:
            amount_pos = pya.locateOnScreen('a\\six.png', confidence = 0.6)
            if amount_pos is not None:
                print("Gained 6 roses."); roses += 6; rose_6_lock = True
                render()
                await asyncio.sleep(2.25); rose_6_lock = False

async def mush_check():
    global mush, mush_lock
    pos = pya.locateOnScreen('a\\mush.png', confidence = 0.7, region = (0, 0, 250, pya.size()[1]))
    if pos is not None and mush_lock == False:
        print("Gained 5 mush."); mush += 5; mush_lock = True
        render()
        await asyncio.sleep(2.25); mush_lock = False

async def time_point_check():
    global time_points, time_point_lock
    pos = pya.locateOnScreen('a\\timepoint.png', confidence = 0.7, region = (0, 0, 250, pya.size()[1]))
    if pos is not None and time_point_lock == False:
        print("Gained 1 time point."); time_points += 1; time_point_lock = True
        render()
        await asyncio.sleep(2.25); time_point_lock = False

async def rosevine_check():
    global rosevines, rosevine_lock
    pos = pya.locateOnScreen('a\\rosevine.png', confidence = 0.7, region = (0, 0, 250, pya.size()[1]))
    if pos is not None and rosevine_lock == False:
        print("Gained 1 Rosevine Plush."); rosevines += 1; rosevine_lock = True
        render()
        await asyncio.sleep(2.25); rosevine_lock = False

async def goodybag_check():
    global goodybags, goodybag_lock
    pos = pya.locateOnScreen('a\\goodybag.png', confidence = 0.7, region = (0, 0, 250, pya.size()[1]))
    if pos is not None and goodybag_lock == False:
        print("Gained 1 Valentine's Goody Bag Token."); goodybags += 1; goodybag_lock = True
        render()
        await asyncio.sleep(2.25); goodybag_lock = False

def rose_garden():
    global match_check, minigame, match_timer
    pos = pya.locateOnScreen('a\\match.png', confidence = 0.7)
    if pos is not None and match_check == False:
        match_check = True
    if match_check == True:
        end_pos = pya.locateOnScreen('a\\match_end_1.png', confidence = 0.5)
        leave_pos = pya.locateOnScreen('a\\match_end_2.png', confidence = 0.5)
        if end_pos is not None or leave_pos is not None:
            match_check = False; match_timer = time.time() + 299
            minigame = [[None, None, None, None],
                        [None, None, None, None],
                        [None, None, None, None]]

def find_relative_box_pos(pos):
    if pos is None: pass
    else:
        x, y = 0, 0
        if pos[0] > int(pya.size()[0]//(1920/835)) and pos[0] < int(pya.size()[0]//(1920/850)): x = 1
        elif pos[0] > int(pya.size()[0]//(1920/970)) and pos[0] < int(pya.size()[0]//(1920/990)): x = 2
        elif pos[0] > int(pya.size()[0]//(1920/1105)) and pos[0] < int(pya.size()[0]//(1920/1115)): x = 3
        if pos[1] > int(pya.size()[1]//(1080/528)) and pos[1] < int(pya.size()[1]//(1080/536)): y = 1
        elif pos[1] > int(pya.size()[1]//(1080/660)) and pos[1] < int(pya.size()[1]//(1080/674)): y = 2
        return (x, y)

def match_box():
    global minigame
    pos_w = pya.locateOnScreen('a\\wave.png', confidence = 0.9, grayscale=True)
    pos_b = pya.locateOnScreen('a\\berry.png', confidence = 0.9, grayscale=True)
    pos_d = pya.locateOnScreen('a\\dragon.png', confidence = 0.9, grayscale=True)
    pos_m = pya.locateOnScreen('a\\meat.png', confidence = 0.9, grayscale=True)
    pos_s = pya.locateOnScreen('a\\sonar.png', confidence = 0.9, grayscale=True)
    pos_u = pya.locateOnScreen('a\\sun.png', confidence = 0.96, grayscale=True)
    j = 0
    pos_list = [pos_w, pos_b, pos_d, pos_m, pos_s, pos_u]
    for i in pos_list:
        if i is not None:
            coords = find_relative_box_pos(i)
            names_dict = {0:'wave', 1:'berry', 2:'dragon', 3:'meat',
                          4:'sonar', 5:'sun'}
            minigame[coords[1]][coords[0]] = names_dict[j]
        j += 1

async def letter_check():
    global letter_timer
    pos = pya.locateOnScreen('a\\letter_end.png', confidence = 0.5)
    if pos is not None and letter_timer == 0:
        letter_timer = time.time() + 60

def update_counters():
    global all_lock, match_check
    try:
        rose_garden()
        if all_lock == False:
            all_lock = True
            asyncio.run(rose_check())
            asyncio.run(mush_check())
            asyncio.run(time_point_check())
            asyncio.run(rosevine_check())
            if match_check: match_box()
            time.sleep(0.05); all_lock = False
    except Exception as e: print(e)

def render():
    global match_check, minigame, letter_timer, match_timer
    (x, y) = (300, 50)
    screen.fill((255, 255, 255))
    screen.blit(credit_font.render(f'CoSCounter v{version} by oreli name by willow', True, (0,0,0)), (10, height - 10))
    screen.blit(font.render(f'{roses} Roses', True, (0, 0, 0)), (20, 50))
    screen.blit(font.render(f'{mush} Mush', True, (0, 0, 0)), (20, 20))
    screen.blit(font.render(f'{time_points} Time Points', True, (0, 0, 0)), (20, 80))
    screen.blit(font.render(f'{rosevines} Rosevine Plushies', True, (0, 0, 0)), (20, 150))
    screen.blit(font.render(f'{goodybags} Goody Bag Tokens', True, (0, 0, 0)), (20, 180))
    for i in minigame:
        x = 300
        for j in i:
            if j is None: screen.blit(pg.image.load('a\\blank icon.png'), (x, y))
            elif j == 'wave': screen.blit(pg.image.load('a\\wave icon.png'), (x, y))
            elif j == 'dragon': screen.blit(pg.image.load('a\\dragon icon.png'), (x, y))
            elif j == 'berry': screen.blit(pg.image.load('a\\berry icon.png'), (x, y))
            elif j == 'sun': screen.blit(pg.image.load('a\\sun icon.png'), (x, y))
            elif j == 'sonar': screen.blit(pg.image.load('a\\sonar icon.png'), (x, y))
            elif j == 'meat': screen.blit(pg.image.load('a\\meat icon.png'), (x, y))
            x += 50
        y += 50
    if letter_timer == 0:
        screen.blit(font.render(f'Letter is available!', True, (0, 0, 0)), (50, 230))
    else:
        screen.blit(font.render(f'Letter will be available again in: {round(letter_timer - time.time(), 2)}s', True, (0, 0, 0)), (50, 230))
    if match_timer == 0:
        screen.blit(font.render(f'Rose garden minigame is available!', True, (0, 0, 0)), (50, 260))
    else:
        screen.blit(font.render(f'Rose garden will be available again in: {round(match_timer - time.time(), 2)}s', True, (0, 0, 0)), (50, 260))
    pgd.flip()

pg.init()
(width, height) = (600, 400)
screen = pgd.set_mode((width, height))
font = pg.font.Font('a\Bolgart.ttf', 18); credit_font = pg.font.Font('a\Bolgart.ttf', 11)
pgd.set_caption('CoSCounter')
running = True


while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False; pg.quit()
    if match_timer != 0:
        if match_timer - time.time() < 0: match_timer = 0
    if letter_timer != 0:
        if letter_timer - time.time() < 0: letter_timer = 0
    render()
    update_counters()