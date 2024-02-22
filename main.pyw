import pyautogui as pya
import time, asyncio, requests
import pygame as pg
import pygame.display as pgd

version = '0.5.0'

all_lock = False
rose_lock = False
region_lock = False
match_timer = 0; letter_timer = 0
region_missions = {"algae sandbar": None, "central rockfaces":  None,
                   "coral reef":    None, "desert":             None,
                   "flower cove":   None, "grassy shoal":       None,
                   "jungle":        None, "mesa":               None,
                   "mountains":     None, "pride rocks":        None,
                   "redwoods":      None, "rocky drop":         None,
                   "seaweed depths":None, "swamp hill":         None,
                   "tundra":        None, "volcano island":     None}

match_check = False

async def letter_check():
    global letter_timer
    if letter_timer == 0:
        pos = pya.locateOnScreen('a\\letter_end.png', confidence = 0.35)
        if pos is not None and match_check == False and pya.locateOnScreen('a\\thirty.png', confidence = 0.6) is not None:
                if pya.locateOnScreen('a\\match_end_1.png', confidence = 0.7) is None:
                    letter_timer = time.time() + 60

async def rose_garden():
    global match_check, minigame, match_timer
    pos = pya.locateOnScreen('a\\match.png', confidence = 0.7)
    if pos is not None and match_check == False:
        match_check = True
    if match_check == True:
        end_pos = pya.locateOnScreen('a\\match_end_1.png', confidence = 0.5)
        leave_pos = pya.locateOnScreen('a\\match_end_2.png', confidence = 0.5)
        rose_pos = pya.locateOnScreen('a\\thirty.png', confidence = 0.6, region = (0, 0, 250, pya.size()[1]))
        if (end_pos is not None or leave_pos is not None) and \
           match_check == True and \
           (pya.locateOnScreen('a\\thirty.png', confidence = 0.6) is not None or pya.locateOnScreen('a\\one.png', confidence = 0.6) is not None):
            if pya.locateOnScreen('a\\letter_end.png', confidence = 0.7) is None:
                match_timer = time.time() + 299
                await asyncio.sleep(5); match_check = False

async def check_regions():
    global region_missions, region_lock
    refresh_pos = pya.locateOnScreen('a\\mission_refresh.png', confidence = 0.7)
    if refresh_pos is not None and region_lock == False:
        region_lock = True
        for i in region_missions:
            if region_missions[i] is None:
                if pya.locateOnScreen(f'a\\{i}.png', confidence = 0.9) is not None:
                    region_missions[i] = time.time() + 300; break
    elif refresh_pos is None: region_lock = False

def update_counters():
    global all_lock, match_check
    try:
        asyncio.run(rose_garden())
        if all_lock == False:
            all_lock = True
            asyncio.run(letter_check())
            asyncio.run(check_regions())
            time.sleep(0.05); all_lock = False
    except Exception as e: print(e)

def render():
    global match_check, minigame, letter_timer, match_timer, region_missions
    screen.fill((255, 255, 255))
    screen.blit(credit_font.render(f'CoSCounter v{version} by oreli name by willow dm me if you find issues', True, (0,0,0)), (10, height - 10))
    if letter_timer == 0:
        screen.blit(font.render(f'Letter is available!', True, (0, 0, 0)), (10, 10))
    else:
        screen.blit(font.render(f'Letter will be available again in: {round(letter_timer - time.time(), 2)}s', True, (0, 0, 0)), (10, 10))
    if match_timer == 0:
        screen.blit(font.render(f'Rose garden minigame is available!', True, (0, 0, 0)), (10, 40))
    else:
        screen.blit(font.render(f'Rose garden will be available again in: {round(match_timer - time.time(), 2)}s', True, (0, 0, 0)), (10, 40))
    x, y = 225, 50
    for i in region_missions:
        if x == 10: x = 225
        else: x = 10; y += 15
        if region_missions[i] is not None and region_missions[i] != 0:
            screen.blit(credit_font.render(f'{i.capitalize()} - {round(region_missions[i] - time.time(), 2)}s', True, (130, 24, 24)), (x, y))
        else:
            screen.blit(credit_font.render(f'{i.capitalize()} - Available!', True, (56, 130, 24)), (x, y))
    pgd.flip()

pg.init()
(width, height) = (450, 200); screen = pgd.set_mode((width, height))
font = pg.font.Font('a\Bolgart.ttf', 18); credit_font = pg.font.Font('a\Bolgart.ttf', 11)
pgd.set_caption('CoSCounter')
running = True

check_for_updates = requests.get("https://api.github.com/repos/Orelii/CoSCounter/releases/latest")
if check_for_updates.json()["name"] != f'v{version}': pgd.set_caption('CoSCounter (Update available!')

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False; pg.quit()
    if match_timer != 0:
        if match_timer - time.time() < 0: match_timer = 0
    if letter_timer != 0:
        if letter_timer - time.time() < 0: letter_timer = 0
    for i in region_missions:
        if region_missions[i] is not None:
            if region_missions[i] - time.time() < 0: region_missions[i] = 0
    update_counters()
    render()