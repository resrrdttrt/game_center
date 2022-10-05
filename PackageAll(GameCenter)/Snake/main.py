import pygame
import random
pygame.init()


window_width=800
window_height=800
block_size=32
play_width=block_size*20
play_height=block_size*20
top_left_x=(window_width-play_width)//2
top_left_y=(window_height-play_height)//2+50
width=play_width//block_size
height=play_height//block_size




class Snake():
    def __init__(self,x,y):
        self.head = [x,y]
        self.pos=[[x,y],[x-1,y],[x-2,y]]
        self.turn=[1,0]
        self.length=3
        self.mobile=True
    def move(self):
        self.head=[self.head[0]+self.turn[0],self.head[1]+self.turn[1]]
        if self.head[0]==width:
            self.head[0]=0
        elif self.head[0]==-1:
            self.head[0]=width-1
        if self.head[1]==height:
            self.head[1]=0
        elif self.head[1]==-1:
            self.head[1]=height-1
        if self.head in self.pos:
            self.mobile=False
        else:
            self.pos.insert(0,self.head)
            try:
                self.pos.pop(self.length)
            except:
                pass



def print_eyes(snake,surface):
    if snake.turn[0] in (-1,1):
        pygame.draw.circle(surface,(0,0,0),(top_left_x+(snake.head[0]+0.5)*block_size,\
            top_left_y+snake.head[1]*block_size+12),4)
        pygame.draw.circle(surface,(0,0,0),(top_left_x+(snake.head[0]+0.5)*block_size,\
            top_left_y+snake.head[1]*block_size+22),4)
    if snake.turn[1] in (-1,1):
        pygame.draw.circle(surface,(0,0,0),(top_left_x+snake.head[0]*block_size+12,\
            top_left_y+(snake.head[1]+0.5)*block_size),4)
        pygame.draw.circle(surface,(0,0,0),(top_left_x+snake.head[0]*block_size+22,\
            top_left_y+(snake.head[1]+0.5)*block_size),4)

    


def spawn_food(snake):
    choice=[]
    for i in range(width):
        for j in range(height):
            if [i,j] not in snake.pos:
                choice.append([i,j])
    return random.choice(choice)


def print_text(surface,string,x,y,size,color):
    font=pygame.font.SysFont('comicsans',size)
    render=font.render(string,True,color)
    font.set_bold(True)
    surface.blit(render,(x,y))
    

def print_grid(surface):
    for i in range(width+1):
        pygame.draw.line(surface,(0,0,0),(top_left_x+i*block_size,top_left_y),\
            (top_left_x+i*block_size,top_left_y+play_height),2)
    for j in range(height+1):
        pygame.draw.line(surface,(0,0,0),(top_left_x,top_left_y+j*block_size),\
        (top_left_x+play_width,top_left_y+j*block_size),2)


def print_board(surface, grid):
    for i in range(width):
        for j in range(height):
            pygame.draw.rect(surface,grid[j][i],(top_left_x+i*block_size,\
                top_left_y+j*block_size,block_size,block_size))


def main(screen):
    back=pygame.image.load('Snake/Image/back.jpg')
    player=Snake(9,9)
    [a,b]=spawn_food(player)
    spawn_next=False
    clock=pygame.time.Clock()
    fall_time=0
    fall_speed=100
    while player.mobile:
        screen.blit(back,(0,0))
        print_text(screen,f'SCORE:{player.length-3}',10,10,50,(255,255,255))
        grid=[[(255,255,255) for i in range(width)] for j in range(height)]
        grid[b][a]=(249,244,0)
        clock.tick()
        fall_time+=clock.get_time()
        if fall_time >(fall_speed//(player.length/10+1)):
            fall_time=0
            player.move()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                player.mobile=False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if player.turn!=[0,1]:
                        player.turn=[0,-1]
                if event.key == pygame.K_DOWN:
                    if player.turn!=[0,-1]:
                        player.turn=[0,1]
                if event.key == pygame.K_RIGHT:
                    if player.turn!=[-1,0]:
                        player.turn=[1,0]
                if event.key == pygame.K_LEFT:
                    if player.turn!=[1,0]:
                        player.turn=[-1,0]
                if event.key == pygame.K_SPACE:
                    player.length+=1
        if player.head==[a,b]:
            player.length+=1
            spawn_next=True
        for i in player.pos:
            x,y=i
            grid[y][x]=(255,0,0)
        if spawn_next:
            [a,b]=spawn_food(player)
            spawn_next=False
        print_board(screen,grid)
        print_grid(screen)
        print_eyes(player,screen)
        pygame.display.update()
    screen.blit(back,(0,0))
    print_text(screen,f'SCORE:{player.length-3}',250,window_height//2-200,100,(255,255,255))
    print_text(screen,'PRESS TO PLAY',150,window_height//2,100,(255,255,255))
    print_text(screen,'AGAIN',300,window_height//2+100,100,(255,255,255))
    pygame.display.update()

def main_menu():
    screen=pygame.display.set_mode((window_width,window_height))
    background=pygame.image.load('Snake/Image/background.jpg')
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
        
