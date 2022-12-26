import pygame
import os
import random

pygame.init()
pygame.font.init()
pygame.mixer.init()

SCORE_FONT=pygame.font.SysFont('agency fb', 20)
SCORE_FONT_END=pygame.font.SysFont('agency fb', 100, bold=True)

screen=pygame.display.set_mode((800, 600))
clock=pygame.time.Clock()
running=True
flap=False
score=0
gameOver=False
menu=True
vel=7
num=0
gamePaused=True

flap_sound=pygame.mixer.Sound(os.path.join('assets', 'flap.wav'))
flap_sound.set_volume(0.7)
music=pygame.mixer.music.load(os.path.join('assets', 'music.mp3'))
pygame.mixer.music.set_volume(0.2)
crash_sound=pygame.mixer.Sound(os.path.join('assets', 'crash.wav'))

bg_img=pygame.image.load(os.path.join('assets', 'bg.png'))

platform_img=pygame.image.load(os.path.join('assets', 'floor.png'))

pipe_img=pygame.image.load(os.path.join('assets', 'pipe.png'))
pipe_img=pygame.transform.scale(pipe_img, (100, 290))

pipe_op_img=pygame.transform.rotate(pipe_img, 180)
platform_x=0

pipes_list=[]
score_lines=[]

plane_img=pygame.image.load(os.path.join('assets', 'plane.png'))
plane_img=pygame.transform.scale(plane_img, (40, 30))
plane_img_up=pygame.transform.rotate(plane_img, 20)
plane_img_down=pygame.transform.rotate(plane_img, -10)
plane=pygame.Rect(300, 150, 30, 20)

menu=pygame.image.load(os.path.join('assets', 'menu.png'))
go=pygame.image.load(os.path.join('assets', 'go.png'))

pygame.display.set_caption('Fly High')
pygame.display.set_icon(plane_img_down)

def wait():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or (event.type == pygame.MOUSEBUTTONDOWN):
                return

def draw_platform():
    global platform_x
    screen.blit(platform_img, (platform_x, 536))
    platform_x-=2
    if platform_x+1024<=800:
        platform_x=0

def draw_pipes():
    global plane
    global gameOver
    global score
    for pipe in pipes_list:
        screen.blit(pipe_op_img, (pipe.x, pipe.y))
        screen.blit(pipe_img, (pipe.x, pipe.y+430))
        pipe2=pygame.Rect(pipe.x, pipe.y+430, 100, 290)
        pipe.x-=2
        if pipe.x<=400 and len(pipes_list)<2:
            pipes_list.append(pygame.Rect(800, random.randint(-150, 0), 100, 290))
            score_lines.append(pygame.Rect(849, 0, 2, 600))
        if pipe.x<=-100:
            pipes_list.remove(pipe)
        if pipe.colliderect(plane) or pipe2.colliderect(plane):
            gameOver=True
    
    for line in score_lines:
        line.x-=2
        if line.colliderect(plane) and not gameOver:
            score+=1
            score_lines.remove(line)

def draw_plane():
    global vel
    global num
    global gameOver
    global plane_img
    global flap
    screen.blit(plane_img, (plane.x, plane.y))
    if flap and not gameOver and plane.y-5>=0:
        flap_sound.play()
        vel=-7
        flap=False
        num=28
    if num>=1:
        plane_img=plane_img_up
        vel+=0.5
        num-=1
    else:
        plane_img=plane_img_down
    plane.y += vel
    if plane.y+15>=536:
        gameOver=True

def draw_score():
    score_text=SCORE_FONT.render(f"Score: {score}", 1, (0,0,0))
    screen.blit(score_text, (10, 10))

while menu:
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play()
    screen.blit(menu, (0,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
            menu=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                menu=False
    pygame.display.update()

while running:
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play()
    clock.tick(60)
    screen.blit(bg_img, (0,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if (event.type==pygame.MOUSEBUTTONDOWN) or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            flap=True

    if len(pipes_list)<1:
        pipe=pygame.Rect(800, random.randint(-150, 0), 100, 290)
        pipes_list.append(pipe)
        score_lines.append(pygame.Rect(849, 0, 2, 600))

    draw_plane()
    draw_pipes()
    draw_platform()
    draw_score()

    if gamePaused:
        text=SCORE_FONT.render("Press 'SPACE' or 'LMB' to Start", 1, (0, 0, 0))
        screen.blit(text, (200, 200))
        pygame.display.update()
        wait()
        gamePaused=False
    if gameOver:
        crash_sound.play()
        pygame.mixer.music.stop()
        screen.blit(go, (0, 0))
        score_text=SCORE_FONT_END.render(f'Score: {score}', 1, (255, 255, 255))
        screen.blit(score_text, (400-score_text.get_width()/2, 400))
        pygame.display.update()
        wait()
    else:
        pygame.display.update()

pygame.quit()