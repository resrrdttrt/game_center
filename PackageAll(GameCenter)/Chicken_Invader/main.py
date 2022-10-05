import pygame
import sys
import random


pygame.init()

class chicken():
    def __init__(self):
        self.X=random.randint(0,1000)
        self.Y=random.randint(50,240)
        self.icon=pygame.image.load('Chicken_Invader/Picture/chicken.png')
        self.speed=1
        self.birth_X=random.randint(self.X,1000)
        self.birth_Y=random.randint(self.Y,240)
        self.pregnancy=True
    @property
    def hitbox(self):
        return pygame.Rect(self.X+16,self.Y,64-32,64)
    

class player():
    def __init__(self):
        self.X=320
        self.Y=420
        self.icon=pygame.image.load('Chicken_Invader/Picture/player.png')
        self.X_speed=1
        self.Y_speed=1
    @property
    def hitbox(self):
        return pygame.Rect(self.X+10,self.Y,64-20,64)

class bullet():
    def __init__(self):
        self.icon=pygame.image.load('Chicken_Invader/Picture/bullet.png')
        self.X=0
        self.Y=0
        self.speed=2.5
        self.state='on'
    @property
    def hitbox(self):
        return pygame.Rect(self.X+10,self.Y,32-20,32)


class egg():
    def __init__(self,chicken):
        self.icon=pygame.image.load('Chicken_Invader/Picture/egg.png')
        self.X=chicken.birth_X
        self.Y=chicken.birth_Y
        self.speed=1
    @property
    def hitbox(self):
        return pygame.Rect(self.X,self.Y,24,24)


def is_collided(ob1,ob2):
    if ob1.hitbox.colliderect(ob2.hitbox):
        return True
    return False

def print_text(surface,string,x,y,size,color):
    font=pygame.font.SysFont('comicsans',size)
    render=font.render(string,True,color)
    font.set_bold(True)
    surface.blit(render,(x,y))

#set up display
X_size=800
Y_size=800  



#set up music
pygame.mixer.music.load('Chicken_Invader/Sound_Effect/Feeling Blue Over You.mp3')
shoot=pygame.mixer.Sound('Chicken_Invader/Sound_Effect/shoot.wav')
explosion=pygame.mixer.Sound('Chicken_Invader/Sound_Effect/explo.wav')
gameover=pygame.mixer.Sound('Chicken_Invader/Sound_Effect/gameover.wav')
winning=pygame.mixer.Sound('Chicken_Invader/Sound_Effect/winning.wav')


# #set up font
# ending_font=pygame.font.SysFont('arial',100)
# ending1=ending_font.render('GAME OVER',True,(255,255,255))
# ending2=ending_font.render('YOU WON',True,(255,255,255))
# score_font=pygame.font.SysFont('arial',32)
# ending_font.set_bold(True)


#set up gameplay



def main(surface):
    pygame.mixer.music.play(-1)
    chicken_nums=10
    b=bullet()
    p=player()
    e=[]
    c=[]
    for i in range(chicken_nums):
        c.append(chicken())
    score_value=0
    score_font=pygame.font.SysFont('comicsan',32)
    score=score_font.render(f'Score:{score_value}',True,(255,255,255))
    back=pygame.image.load('Chicken_Invader/Picture/back.jpg')
    running=False
    while not running:
        surface.blit(back,(0,0))
        for event in pygame.event.get():
            if event.type==pygame.QUIT: 
                running=True
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    if b.state=='on':
                        shoot.play()
                        b.state='off'
                        b.X=p.X+16
                        b.Y=p.Y-10


        #control
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and p.X>0:
            p.X-=p.X_speed
        if keys[pygame.K_RIGHT] and p.X<X_size-64:
            p.X+=p.X_speed
        if keys[pygame.K_UP] and p.Y>0:
            p.Y-=p.Y_speed
        if keys[pygame.K_DOWN] and p.Y<Y_size-64:
            p.Y+=p.Y_speed



        #fire bullet
        if b.state=='off':
            # pygame.draw.rect(screen,(255,0,0),b.hitbox)
            surface.blit(b.icon,(b.X,b.Y))
            b.Y-=b.speed
        if b.Y<0:
            b.state='on'

        #chicken move
        for i in range(chicken_nums):
            if c[i].X<0:
                c[i].speed=-c[i].speed
                c[i].Y+=70
            if c[i].X>X_size-64:
                c[i].speed=-c[i].speed
                c[i].Y+=70
            if c[i].Y>Y_size:
                c.pop(i)
                c.append(chicken())
            if c[i].X>c[i].birth_X and c[i].Y>c[i].birth_Y and c[i].pregnancy==True:
                c[i].pregnancy=False
                e.append(egg(c[i]))

        #collision
        for i in range(chicken_nums):
            if is_collided(c[i],b):
                b.X=0
                b.Y=0
                explosion.play()
                b.state='on'
                score_value+=1
                score=score_font.render(f'Score:{score_value}',True,(255,255,255))
                c.pop(i)
                c.append(chicken())
    
        for value in c:
            if is_collided(value,p):
                running=1

        for value in e:
            if is_collided(value,p):
                running=1


        for i in range(len(e)):
            e[i].Y+=e[i].speed
            # pygame.draw.rect(g.screen,(255,0,0),e[i].hitbox)
            surface.blit(e[i].icon,(e[i].X,e[i].Y))

        for val in e:
            if val.Y>Y_size-32:
                e.remove(val)


        #winning
        if score_value==40:
            running=2

        #screen blit
        for i in range(chicken_nums):
            c[i].X+=c[i].speed
            # pygame.draw.rect(screen,(255,0,0),c[i].hitbox)
            surface.blit(c[i].icon,(c[i].X,c[i].Y))

        
        # pygame.draw.rect(screen,(255,0,0),p.hitbox)
        surface.blit(p.icon,(p.X,p.Y))
        surface.blit(score,(0,0))
        
        pygame.display.update()


    pygame.mixer.music.stop()
    if running==1:
        gameover.play()
        print_text(surface,'GAME OVER',200,Y_size//2-100,100,(255,255,255))
    if running==2:
        winning.play()
        print_text(surface,'YOU WON',250,Y_size//2-100,100,(255,255,255))

    print_text(surface,'PRESS TO PLAY',150,Y_size//2,100,(255,255,255))
    print_text(surface,'AGAIN',300,Y_size//2+100,100,(255,255,255))




def main_menu():
    screen=pygame.display.set_mode((X_size,Y_size))
    icon=pygame.image.load('Chicken_Invader/Picture/launch.png')
    pygame.display.set_caption('Chicken Invader')
    pygame.display.set_icon(icon)
    background=pygame.image.load('Chicken_Invader/Picture/background.jpg')
    screen.blit(background,(0,0))
    print_text(screen,'PRESS TO PLAY',150,Y_size//2,100,(255,255,255))
    run=True
    while run:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.KEYDOWN:
                main(screen)
        pygame.display.update()


if __name__ == '__main__':
    main_menu()