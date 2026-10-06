import os
import sys
import pygame as pg
import random
import time

WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))
 
def gameover(screen: pg.Surface) -> None: 
    bk_img = pg.Surface((WIDTH, HEIGHT)) # 1. 黒いSurfaceを作る
    bk_img.fill((0, 0, 0))

    bk_img.set_alpha(200)  # 2. 透明度を設定する
  
    screen.blit(bk_img, (0, 0))  # 3. 黒いSurfaceを画面に重ねて暗くする

    fonto = pg.font.Font(None, 50) # 4. Game Overの文字を作る
    txt = fonto.render("Game Over", True, (255, 255, 255))
    txt_rct = txt.get_rect()
    txt_rct.center = (WIDTH // 2, HEIGHT // 2)

    cry_img = pg.image.load("fig/8.png")  # 5. 泣いているこうかとんを左右に表示する
    cry_img = pg.transform.rotozoom(cry_img, 0, 0.4)

    cry_rct1 = cry_img.get_rect()
    cry_rct1.centery = HEIGHT // 2
    cry_rct1.right = txt_rct.left - 10

    cry_rct2 = cry_img.get_rect()
    cry_rct2.centery = HEIGHT // 2
    cry_rct2.left = txt_rct.right + 10

    screen.blit(cry_img, cry_rct1)
    screen.blit(txt, txt_rct)
    screen.blit(cry_img, cry_rct2)

    pg.display.update()  # 6. 画面を更新して5秒間表示する
    time.sleep(5)

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs=[]
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0,0,0))
        bb_imgs.append(bb_img)
    bb_accs = [a for a in range(1, 11)]
    return bb_imgs, bb_accs  

def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    kk_imgs = {}
    kk_img = pg.image.load("fig/3.png")

    kk_imgs[(0, 0)] = pg.transform.rotozoom(kk_img, 0, 0.9)
    kk_imgs[(0, -5)] = pg.transform.rotozoom(kk_img, 0, 0.9)
    kk_imgs[(0, 5)] = pg.transform.rotozoom(kk_img, 0, 0.9)
    kk_imgs[(-5, 0)] = pg.transform.rotozoom(kk_img, 0, 0.9)
    kk_imgs[(5, 0)] = pg.transform.rotozoom(kk_img, 0, 0.9)

    return kk_imgs
def check_bound(rct):
    yoko, tate = True, True

    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False

    return yoko, tate
def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr = 0
    bb_imgs, bb_accs = init_bb_imgs()
    DELTA ={
        pg.K_UP: (0,-5),
        pg.K_DOWN: (0, 5),
        pg.K_LEFT: (-5, 0),
        pg.K_RIGHT: (5, 0)
    }
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))  
    bb_rct = bb_img.get_rect()
    bb_rct.x = random.randint(0, WIDTH)
    bb_rct.y = random.randint(0, HEIGHT)

    bb_imgs, bb_accs = init_bb_imgs()

    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()
    bb_rct.x = random.randint(0, WIDTH - bb_rct.width)
    bb_rct.y = random.randint(0, HEIGHT - bb_rct.height)

    
    vx = 5
    vy = 5

    while True:
        
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        
        screen.blit(bg_img, [0, 0]) 
        
        yoko, tate = check_bound(bb_rct)
        if not yoko:
           vx = -vx
        if not tate:
           vy = -vy
        screen.blit(bb_img, bb_rct)
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        yoko, tate = check_bound(kk_rct)

        if not yoko:
           kk_rct.move_ip(-sum_mv[0], 0)
        if not tate:
           kk_rct.move_ip(0, -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        
        if kk_rct.colliderect(bb_rct):
           gameover(screen)
           return
        pg.display.update()
        tmr += 1
        clock.tick(50)
        avx = vx * bb_accs[min(tmr//500, 9)]
        avy = vy * bb_accs[min(tmr//500, 9)]

        bb_img = bb_imgs[min(tmr//500, 9)]

        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height

        bb_rct.move_ip(avx, avy)
        

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
