import pygame
import random

pygame.init()

class bird():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.vel_x=0
        self.vel_y=0
        self.height=12
        self.icon=pygame.transform.scale(pygame.image.load('Flappy_Bird/Image/bird.png'),(80,60))

    @property
    def center(self):
        return self.icon.get_rect(center=(self.x,self.y))

class pipe():
    def __init__(self,height):
        self.x = window_width
        self.height = height

    @property
    def bot_pipe_top(self):
        return pygame.Rect(self.x,window_height-self.height,100,40)
    @property
    def bot_pipe_bot(self):
        return pygame.Rect(self.x+5,window_height-self.height+40,90,self.height-40)
    @property
    def up_pipe_top(self):
        return pygame.Rect(self.x,window_height-self.height-125-100,100,40)
    @property
    def up_pipe_bot(self):
        return pygame.Rect(self.x+5,0,90,window_height-self.height-125-100)



window_width=800
window_height=800

def rotation(surface,angle):
    rotated_surface=pygame.transform.rotozoom(surface,angle,1)
    return rotated_surface

def draw_pipe(surface,pipe):
    pygame.draw.rect(surface,(0,255,0),pipe.up_pipe_top)
    pygame.draw.rect(surface,(0,0,0),pipe.up_pipe_top,5)
    pygame.draw.rect(surface,(0,255,0),pipe.up_pipe_bot)
    pygame.draw.rect(surface,(0,0,0),pipe.up_pipe_bot,5)
    pygame.draw.rect(surface,(0,255,0),pipe.bot_pipe_top)
    pygame.draw.rect(surface,(0,0,0),pipe.bot_pipe_top,5)
    pygame.draw.rect(surface,(0,255,0),pipe.bot_pipe_bot)
    pygame.draw.rect(surface,(0,0,0),pipe.bot_pipe_bot,5)

def get_pipe():
    x=random.randint(300,500)
    return pipe(x)

def print_text(surface,string,x,y,size,color):
    font=pygame.font.SysFont('comicsans',size)
    render=font.render(string,True,color)
    font.set_bold(True)
    surface.blit(render,(x,y))
    

def main(screen):
    back=pygame.image.load('Flappy_Bird/Image/back.jpg')
    player=bird(400,400)
    run=True
    angle=0
    speed=5
    score=0
    pipe=get_pipe()
    while run:
        screen.blit(back,(0,0))
        pipe.x-=speed
        print_text(screen,f'SCORE:{score}',10,10,50,(255,255,255))
        draw_pipe(screen,pipe)
        angle=player.vel_y*(45/player.height)
        rotated_icon=rotation(player.icon,angle)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.vel_y=player.height
        player.y-=player.vel_y
        if player.vel_y>-player.height:
            player.vel_y-=1
        if pipe.x<0:
            pipe=get_pipe()
        if player.x==pipe.x:
            score+=1
        if player.y>window_height or player.y<0:
            run=False
        for i in (pipe.bot_pipe_bot,pipe.bot_pipe_top,pipe.up_pipe_bot,pipe.up_pipe_top):
            if player.center.colliderect(i):
                run=False
        screen.blit(rotated_icon,player.center)
        pygame.time.delay(15)
        pygame.display.update()
    screen.blit(back,(0,0))
    print_text(screen,f'SCORE:{score}',250,window_height//2-200,100,(255,255,255))
    print_text(screen,'PRESS TO PLAY',150,window_height//2,100,(255,255,255))
    print_text(screen,'AGAIN',300,window_height//2+100,100,(255,255,255))

        
def main_menu():
    screen=pygame.display.set_mode((window_width,window_height))
    background=pygame.image.load('Flappy_Bird/Image/background.jpg')
    screen.blit(background,(0,0))
    print_text(screen,'PRESS TO PLAY',150,window_height//2,100,(255,255,255))
    run=True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(screen)
        pygame.display.update()


        
if __name__ == '__main__':
    main_menu()