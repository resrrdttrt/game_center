import pygame
import sys
import random
pygame.init()

I=[ [ [1,0,0,0],
      [1,0,0,0],
      [1,0,0,0],
      [1,0,0,0] ],
    [ [1,1,1,1],
      [0,0,0,0],
      [0,0,0,0],
      [0,0,0,0] ] ]
J=[ [ [0,1,0,0],
      [0,1,0,0],
      [1,1,0,0],
      [0,0,0,0] ],
    [ [1,0,0,0],
      [1,1,1,0],
      [0,0,0,0],
      [0,0,0,0] ],
    [ [1,1,0,0],
      [1,0,0,0],
      [1,0,0,0],
      [0,0,0,0] ],
    [ [1,1,1,0],
      [0,0,1,0],
      [0,0,0,0],
      [0,0,0,0] ] ]
L=[ [ [1,0,0,0],
      [1,0,0,0],
      [1,1,0,0],
      [0,0,0,0] ],
    [ [1,1,1,0],
      [1,0,0,0],
      [0,0,0,0],
      [0,0,0,0] ],
    [ [1,1,0,0],
      [0,1,0,0],
      [0,1,0,0],
      [0,0,0,0] ],
    [ [0,0,1,0],
      [1,1,1,0],
      [0,0,0,0],
      [0,0,0,0] ] ]
O=[ [ [1,1,0,0],
      [1,1,0,0],
      [0,0,0,0],
      [0,0,0,0] ] ]
S=[ [ [0,1,1,0],
      [1,1,0,0],
      [0,0,0,0],
      [0,0,0,0] ],
    [ [1,0,0,0],
      [1,1,0,0],
      [0,1,0,0],
      [0,0,0,0] ] ]
Z=[ [ [1,1,0,0],
      [0,1,1,0],
      [0,0,0,0],
      [0,0,0,0] ],
    [ [0,1,0,0],
      [1,1,0,0],
      [1,0,0,0],
      [0,0,0,0] ] ]
T=[ [ [0,1,0,0],
      [1,1,1,0],
      [0,0,0,0],
      [0,0,0,0] ],
    [ [1,0,0,0],
      [1,1,0,0],
      [1,0,0,0],
      [0,0,0,0] ],
    [ [1,1,1,0],
      [0,1,0,0],
      [0,0,0,0],
      [0,0,0,0] ],
    [ [0,1,0,0],
      [1,1,0,0],
      [0,1,0,0],
      [0,0,0,0] ] ]

piece_shape=[I,J,L,O,S,Z,T]
piece_color=[(223,0,41),(82,9,108),(32,90,167),(91,189,43),(249,244,0),(0,255,255),(236,135,14)]
window_width=800
window_height=800
block_size=32
play_width=block_size*10
play_height=block_size*20
top_left_x=(window_width-play_width)//2
top_left_y=(window_height-play_height)//2+50
width=play_width//block_size
height=play_height//block_size

def create_grid(locked_pos):
    grid=[[(255,255,255) for i in range(width)] for j in range(height)]

    for i in range(width):
        for j in range(height):
            if (j,i) in locked_pos:
                grid[j][i]=locked_pos[(j,i)]
    return grid


class piece():
    def __init__(self,shape,x,y):
        self.x=x
        self.y=y
        self.shape=shape
        self.color=piece_color[piece_shape.index(shape)]
        self.rotation=0
    @property
    def current_shape(self):
        return self.shape[self.rotation % len(self.shape)]

def convert_piece(piece):
    pos=[]
    for i in range(4):
        for j in range(4):
            if piece.current_shape[i][j]==1:
                pos.append((piece.x+j,piece.y+i))
    return pos


def print_board(surface, grid):
    for i in range(width):
        for j in range(height):
            pygame.draw.rect(surface,grid[j][i],(top_left_x+i*block_size,\
                top_left_y+j*block_size,block_size,block_size))
    


def print_grid(surface):
    for i in range(width+1):
        pygame.draw.line(surface,(0,0,0),(top_left_x+i*block_size,top_left_y),\
            (top_left_x+i*block_size,top_left_y+play_height),2)
    for j in range(height+1):
        pygame.draw.line(surface,(0,0,0),(top_left_x,top_left_y+j*block_size),\
        (top_left_x+play_width,top_left_y+j*block_size),2)

def get_piece():
    return piece(random.choice(piece_shape),4,0)

def valid_pos(piece,grid):
    valid_position=[]
    for i in range(width):
        for j in range(height):
            if grid[j][i] == (255,255,255):
                valid_position.append((i,j))
    pos=convert_piece(piece)
    for i in pos:
        if i not in valid_position:
            return False
    return True

def delete_row(grid,locked_pos):
    row=0
    for i in range(height-1,-1,-1):
        if (255,255,255) not in grid[i]:
            row+=1
            for j in range(width):
                try:
                    del locked_pos[(i,j)]
                except:
                    continue
        if (255,255,255) in grid[i] and row!=0:
            for keys in sorted(list(locked_pos.keys()),key=lambda x:x[0],reverse=True):
                x,y=keys
                if x<=i:
                    locked_pos[(x+row,y)]=locked_pos.pop((keys))
    return row


def print_next_piece(surface,piece_):
    current_piece=piece(piece_.shape,0,0)
    grid_=[[(255,255,255) for i in range(4)] for j in range(4)]
    shape_pos=convert_piece(current_piece)
    for i in range(len(shape_pos)):
        x,y=shape_pos[i]
        grid_[y][x]=current_piece.color
    for i in range(4):
        for j in range(4):
            if grid_[j][i]!=(255,255,255):
                pygame.draw.rect(surface,grid_[j][i],(50+i*block_size,\
                top_left_y+100+j*block_size,block_size,block_size))
                pygame.draw.rect(surface,(255,255,255),(50+i*block_size,\
                top_left_y+100+j*block_size,block_size,block_size),2)

def print_text(surface,string,x,y,size,color):
    font=pygame.font.SysFont('comicsans',size)
    render=font.render(string,True,color)
    font.set_bold(True)
    surface.blit(render,(x,y))
    

def main(screen):
    background=pygame.image.load('Tetris/image/background.jpg')
    change_piece=False
    locked_pos={}
    current_piece=get_piece()
    next_piece=get_piece()
    fall_time=0
    fall_speed=1000
    score=0
    run=True
    clock=pygame.time.Clock()
    replay=pygame.image.load('Tetris/Image/replay.png')
    replay1=pygame.image.load('Tetris/Image/replay1.png')
    while run:
        screen.blit(background,(0,0))
        screen.blit(replay,(20,20))
        x,y=pygame.mouse.get_pos()
        if 20<x<84 and 20<y<84:
            screen.blit(replay1,(20,20))
        else:
            screen.blit(replay,(20,20))
        print_text(screen,'NEXT PIECE',40,top_left_y+60,40,(255,255,255))
        print_text(screen,f'SCORE:{score}',window_width-200,top_left_y+60,40,(255,255,255))
        grid=create_grid(locked_pos)
        clock.tick()
        fall_time+=clock.get_time()
        print_next_piece(screen,next_piece)
        if fall_time>(fall_speed/(score//10+1)):
            fall_time=0
            current_piece.y+=1
            if not valid_pos(current_piece,grid):
                current_piece.y-=1
                change_piece=True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 20<x<84 and 20<y<84:
                    change_piece=False
                    locked_pos={}
                    current_piece=get_piece()
                    next_piece=get_piece()
                    fall_time=0
                    fall_speed=1000
                    score=0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    current_piece.x+=1
                    if not valid_pos(current_piece,grid):
                        current_piece.x-=1
                if event.key == pygame.K_LEFT:
                    current_piece.x-=1
                    if not valid_pos(current_piece,grid):
                        current_piece.x+=1
                if event.key == pygame.K_DOWN:
                    current_piece.y+=1
                    if not valid_pos(current_piece,grid):
                        current_piece.y-=1
                if event.key == pygame.K_UP:
                    current_piece.rotation+=1
                    if not valid_pos(current_piece,grid):
                        current_piece.rotation-=1
                if event.key == pygame.K_SPACE:
                    while valid_pos(current_piece,grid):
                        current_piece.y+=1
                    if not valid_pos(current_piece,grid):
                        current_piece.y-=1

        shape_pos=convert_piece(current_piece)
        for i in range(len(shape_pos)):
            x,y=shape_pos[i]
            if grid[y][x]==(255,255,255):
                grid[y][x]=current_piece.color
            else:
                run=False
        if change_piece:
            for i in range(len(shape_pos)):
                x,y=shape_pos[i]
                locked_pos[(y,x)]=current_piece.color
            score+=delete_row(grid,locked_pos)
            current_piece=next_piece
            next_piece=get_piece()
            change_piece=False
        print_board(screen,grid)
        print_grid(screen)
        pygame.display.update()
    screen.blit(background,(0,0))
    print_text(screen,f'SCORE:{score}',250,window_height//2-200,100,(255,255,255))
    print_text(screen,'PRESS TO PLAY',150,window_height//2,100,(255,255,255))
    print_text(screen,'AGAIN',300,window_height//2+100,100,(255,255,255))
    

def main_menu():
    screen=pygame.display.set_mode((window_width,window_height))
    icon=pygame.image.load('Tetris/image/tetris.png')
    background=pygame.image.load('Tetris/image/back.jpg')
    run=True
    screen.blit(background,(0,0))
    pygame.display.set_icon(icon)
    pygame.display.set_caption('TETRIS')
    print_text(screen,'PRESS TO PLAY',150,window_height//2,100,(255,255,255))
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
            if event.type == pygame.KEYDOWN:
                main(screen)
        pygame.display.update()


if __name__ == '__main__':
    main_menu()