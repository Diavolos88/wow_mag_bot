import cv2
import pyautogui as pg
from matplotlib import pyplot as plt
import numpy as np
import identical
import time

pixelX_ENEMY = 368
pixelY_ENEMY = 33

pixelX_HP = 169
pixelY_HP = 49

pixelX_center = 693
pixelY_center = 351

pixelX_enemy_hp = 298
pixelY_enemy_hp = 50

pixelX_ENEMY_Range = 974
pixelY_ENEMY_Range = 670

pixelX_cast = 603
pixelY_cast = 599

spell_fireball = 'q'
fireball_cast = 1.9

spell_fenix = 't'
fireball_fenix = 0.5

spell_burn = 'e'
fireball_burn = 0.5

spell_fire_bang = '2'
fire_bang = 0.5

spell_sheald_1 = 'shiftleft'
spell_sheald_2 = '2'

def findeEnemy() :
    start = time.perf_counter()
    while True:
        pg.keyDown('w')
        pg.press('space')
        pg.sleep(0.2)
        pg.keyUp('w')
        pg.press('c')
        try:
            if (time.perf_counter() - start > 25):
                pg.moveTo(pixelX_center, pixelY_center)
                pg.dragTo(pixelX_center - 250, pixelY_center, button='right')
                start = time.perf_counter()
            if (pg.pixel(pixelX_ENEMY, pixelY_ENEMY)[0] <= 255 and pg.pixel(pixelX_ENEMY, pixelY_ENEMY)[0] >= 180):
                print("Enemy finded")
                break
        except WindowsError:
            findeEnemy()

def castFireBall ():
    pg.press(spell_fireball)
    pg.sleep(0.6)
    try:
        if (not (pg.pixel(pixelX_cast, pixelY_cast)[0] == 177 and pg.pixel(pixelX_cast, pixelY_cast)[1] >= 122)):
            start = time.perf_counter()
            while (not (pg.pixel(pixelX_cast, pixelY_cast)[0] == 177 and pg.pixel(pixelX_cast, pixelY_cast)[1] >= 122)):
                if (not(pg.pixel(pixelX_ENEMY, pixelY_ENEMY)[0] <= 255 and pg.pixel(pixelX_ENEMY, pixelY_ENEMY)[0] >= 180)):
                    break
                pg.moveTo(pixelX_center, pixelY_center)
                pg.dragTo(pixelX_center - 150, pixelY_center, button='right')
                pg.press(spell_fireball)
                pg.sleep(0.2)
                if (time.perf_counter() - start > 8):
                    break
            pg.sleep(fireball_cast - 0.2)
            return 0
        pg.sleep(fireball_cast - 0.6)
        return 0
    except WindowsError:
        return 0

def castFireBang():
    pg.press(spell_fire_bang)
    pg.sleep(1)

def castFenix():
    pg.press(spell_fenix)
    pg.sleep(1)

def castBurn():
    pg.press(spell_burn)
    pg.sleep(0.2)
    if (not (pg.pixel(pixelX_cast, pixelY_cast)[0] == 177 and pg.pixel(pixelX_cast, pixelY_cast)[1] >= 122)):
        start = time.perf_counter()
        while (not (pg.pixel(pixelX_cast, pixelY_cast)[0] == 177 and pg.pixel(pixelX_cast, pixelY_cast)[1] >= 122)):
            if (not (pg.pixel(pixelX_ENEMY, pixelY_ENEMY)[0] <= 255 and pg.pixel(pixelX_ENEMY, pixelY_ENEMY)[0] >= 180)):
                break
            pg.moveTo(pixelX_center, pixelY_center)
            pg.dragTo(pixelX_center - 150, pixelY_center, button='right')
            pg.press(spell_burn)
            pg.sleep(0.2)
            if (time.perf_counter() - start > 8):
                break
    pg.sleep(0.3)

def fight():
    start = time.perf_counter()
    try:
        i = 0
        while (pg.pixel(pixelX_ENEMY, pixelY_ENEMY)[0] <= 255 and pg.pixel(pixelX_ENEMY, pixelY_ENEMY)[0] >= 180):
            i += 1
            if (pg.pixel(pixelX_enemy_hp, pixelY_enemy_hp)[1] >= 160):
                cast_fire_fire()
                castFireBall()
                cast_fire_fire()
                if (i % 2 == 1):
                    castFenix()
                if (time.perf_counter() - start > 25):
                    return 0
            else:
                cast_fire_fire()
                castBurn()
                if (i % 2 == 1):
                    castBurn()
                    pg.press('1')
                else:
                    cast_fire_fire()
        return 1
    except WindowsError:
        fight()

def killEnemy():
    start = time.perf_counter()
    try:
        while (pg.pixel(pixelX_ENEMY_Range, pixelY_ENEMY_Range)[0] <= 255 and pg.pixel(pixelX_ENEMY_Range, pixelY_ENEMY_Range)[0] >= 200):
            pg.keyDown('w')
            pg.press('space')
            pg.sleep(0.2)
            pg.keyUp('w')
            if (time.perf_counter() - start > 25):
                return 0
        pg.keyDown('w')
        pg.sleep(0.4)
        pg.keyUp('w')
        pg.hotkey(spell_sheald_1, spell_sheald_2)
        return fight()
    except WindowsError:
        killEnemy()
def cast_fire_fire():

    pixelX_buf_start = 840
    pixelY_buf_start = 13

    pixelX_buf_end = 1175
    pixelY_buf_end = 154

    i = 0
    for i in range (3):
        pg.screenshot("sc1.png", region=(pixelX_buf_start, pixelY_buf_start, pixelX_buf_end, pixelY_buf_end))
        img_rgb = cv2.imread('sc1.png')
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('hand.png', 0)

        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where( res >= threshold)
        for pt in zip(*loc[::-1]):
            pg.press('2')
            pg.sleep(0.5)
            pg.press('1')
            return 0
        i += 1

res = 0
while True:
    pg.press('l')
    findeEnemy()
    res += killEnemy()
    print("Enemy killed num:", res)
