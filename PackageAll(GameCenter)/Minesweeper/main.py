
import pygame
import random
import sys

pygame.init()


width=800
height=800
play_width=600
play_height=600
block_size=30

top_left_x=(width-play_width)//2
top_left_y=(height-play_height)//2

dug={(-1,-1)}


imageb=pygame.image.load('Minesweeper/Image/bomb.png')
imagef=pygame.image.load('Minesweeper/Image/flag.png')
image1=pygame.image.load('Minesweeper/Image/one.png')
image2=pygame.image.load('Minesweeper/Image/two.png')
image3=pygame.image.load('Minesweeper/Image/three.png')
image4=pygame.image.load('Minesweeper/Image/four.png')
image5=pygame.image.load('Minesweeper/Image/five.png')
image6=pygame.image.load('Minesweeper/Image/six.png')
image7=pygame.image.load('Minesweeper/Image/seven.png')
image8=pygame.image.load('Minesweeper/Image/eight.png')
trophy=pygame.image.load('Minesweeper/Image/trophy.png')
skull=pygame.image.load('Minesweeper/Image/losing.png')
background=pygame.image.load('Minesweeper/Image/background.jpg')
back=pygame.image.load('Minesweeper/Image/back.jpg')
replay=pygame.image.load('Minesweeper/Image/replay.png')
replay1=pygame.image.load('Minesweeper/Image/replay1.png')
caption=pygame.image.load('Minesweeper/Image/icon.png')


icon=[None,image1,image2,image3,image4,image5,image6,image7,image8,imageb,imagef]


def print_board(screen):
    for i in range(play_width//block_size+1):
        pygame.draw.line(screen,(0,0,0),(top_left_x+i*block_size,top_left_y),\
            (top_left_x+i*block_size,top_left_y+play_height),3)
    for j in range(play_height//block_size+1):
        pygame.draw.line(screen,(0,0,0),(top_left_x,top_left_y+j*block_size),\
        (top_left_x+play_width,top_left_y+j*block_size),3)

def print_grid(screen,grid,bomb=True):
    for i in range(play_width//block_size):
        for j in range(play_height//block_size):
            pygame.draw.rect(screen,(255,255,255),(top_left_x+i*block_size,\
            top_left_y+j*block_size,block_size,block_size))
            if grid[i][j][1]!=None and grid[i][j][0]==None:
                if grid[i][j][1]==0:
                    pygame.draw.rect(screen,(105,105,105),(top_left_x+i*block_size,\
                top_left_y+j*block_size,block_size,block_size))
                else:
                    if bomb:
                        if grid[i][j][1]==9:
                            continue
                    screen.blit(icon[grid[i][j][1]],(top_left_x+i*block_size+2,\
                    top_left_y+j*block_size+4))
            if grid[i][j][0]==1:
                screen.blit(icon[10],(top_left_x+i*block_size+2,\
                    top_left_y+j*block_size+4))
    print_board(screen)

def print_text(surface,string,x,y,size,color):
    font=pygame.font.SysFont('comicsans',size)
    render=font.render(string,True,color)
    font.set_bold(True)
    surface.blit(render,(x,y))

def win_condition(grid):
    for i in range(play_width//block_size):
        for j in range(play_height//block_size):
            if grid[i][j][1]==None:
                return True
    return False

def place_mines(nums,grid):
    mines=0
    while mines<nums:
        x,y=random.randint(0,play_width//block_size-1),random.randint(0,play_height//block_size-1)
        if grid[x][y][1]!=9:
            grid[x][y][1]=9
            mines+=1

def number_mines(grid,x,y):
    if grid[x][y][1]==9:
        return 9
    number_mines=0
    for i in range(max(0,x-1),min(play_width//block_size,x+2)):
        for j in range(max(0,y-1),min(play_height//block_size,y+2)):
            if grid[i][j][1]==9:
                number_mines+=1
    return number_mines


def dig(grid,x,y):
    global dug
    dug.add((x,y))
    if number_mines(grid,x,y)!=0:
        grid[x][y][1]=number_mines(grid,x,y)
        return True
    elif number_mines(grid,x,y)==0:
        grid[x][y][1]=0
    for r in range(max(0,x-1),min(play_width//block_size,x+2)):
        for c in range(max(0,y-1),min(play_height//block_size,y+2)):
            if (r,c) in dug:
                continue
            dig(grid,r,c)
    
def main(screen):
    global dug
    final_grid=[[[None,None] for _ in range(play_width//block_size)]\
    for _ in range(play_height//block_size)]
    place_mines(20,final_grid)
    running=True
    screen.blit(background,(0,0))
    screen.blit(replay,(20,20))
    while running:
        x,y=pygame.mouse.get_pos()
        if 20<x<84 and 20<y<84:
            screen.blit(replay1,(20,20))
        else:
            screen.blit(replay,(20,20))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            if win_condition(final_grid) or running:
                if event.type==pygame.MOUSEBUTTONDOWN:
                    if 20<x<84 and 20<y<84:
                        final_grid=[[[None,None] for _ in range(play_width//block_size)]\
                        for _ in range(play_height//block_size)]
                        place_mines(20,final_grid)
                        dug={(-1,-1)}
                        running=True
                    if top_left_x<x<top_left_x+play_width and\
                        top_left_y<y<top_left_y+play_height:
                        col=(x-top_left_x)//block_size
                        row=(y-top_left_y)//block_size
                        if event.button==1:
                            if final_grid[col][row][1]==9:
                                print_grid(screen,final_grid,bomb=False)
                                running=False
                                break
                            if final_grid[col][row][0]==None:
                                dig(final_grid,col,row)
                        if event.button==3:
                            if final_grid[col][row][1] in (None,9) and final_grid[col][row][0]==None:
                                final_grid[col][row][0]=1    
                            elif final_grid[col][row][0]==1:
                                final_grid[col][row][0]=None
                print_grid(screen,final_grid)
        if not running:
            dug={(-1,-1)}
            print_grid(screen,final_grid,bomb=False)
            screen.blit(skull,(width/2-256/2,height/2-256))
        if not win_condition(final_grid):
            running=False
            dug={(-1,-1)}
            print_grid(screen,final_grid,bomb=False)
            screen.blit(trophy,(width/2-256/2,height/2-256))
        pygame.display.update()

    print_text(screen,'PRESS TO PLAY',150,height//2,100,(255,0,0))
    print_text(screen,'AGAIN',300,height//2+100,100,(255,0,0))



def main_menu():
    screen=pygame.display.set_mode((width,height))
    pygame.display.set_caption('Minesweeper')
    pygame.display.set_icon(caption)
    screen.blit(back,(0,0))
    print_text(screen,'PRESS TO PLAY',150,height//2,100,(255,255,255))
    run=True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
            if event.type == pygame.KEYDOWN:
                main(screen)
        pygame.display.update()

if __name__=='__main__':
    main_menu()




