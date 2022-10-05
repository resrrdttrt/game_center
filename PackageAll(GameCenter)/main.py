import pygame
import sys
from Chicken_Invader import main as Chicken_game
from Minesweeper import main as Mine_game
from Tetris import main as Tetris_game
from Snake import main as Snake_game
from Flappy_Bird import main as Flappy_game
pygame.init()

class game():
    def __init__(self,icon,x,y):
        self.icon = icon
        self.x = x
        self.y = y
        self.hitbox=pygame.Rect(x,y,200,200)
    
    def print_game(self,surface):
        surface.blit(self.icon,(self.x,self.y))
    
    def print_box(self,surface):
        pygame.draw.rect(surface,(255,255,255),self.hitbox,4)

tetris=game(pygame.image.load('Symbol/tetris.png'),50,250)
mine=game(pygame.image.load('Symbol/mine.png'),300,250)
chicken=game(pygame.image.load('Symbol/chicken.png'),550,250)
snake=game(pygame.image.load('Symbol/snake.png'),50,500)
flappy_bird=game(pygame.image.load('Symbol/flappy_bird.png'),300,500)
back=pygame.image.load('Symbol/back.jpg')


game_list=[tetris,mine,chicken,snake,flappy_bird]

def print_text(surface,string,x,y,size,color):
    font=pygame.font.SysFont('comicsans',size)
    render=font.render(string,True,color)
    font.set_bold(True)
    surface.blit(render,(x,y))

def main_menu():
    window_width=800
    window_height=800
    screen=pygame.display.set_mode((window_width,window_height))
    pygame.display.set_caption('Game Center')
    while True:
        screen.blit(back,(0,0))
        print_text(screen,'CHOOSE A GAME',window_width//2-300,100,100,(255,255,255))
        x,y=pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                if chicken.hitbox.collidepoint((x,y)):
                    Chicken_game.main_menu()
                if mine.hitbox.collidepoint((x,y)):
                    Mine_game.main_menu()
                if tetris.hitbox.collidepoint((x,y)):
                    Tetris_game.main_menu()
                if snake.hitbox.collidepoint((x,y)):
                    Snake_game.main_menu()
                if flappy_bird.hitbox.collidepoint((x,y)):
                    Flappy_game.main_menu()
        for i in game_list:
            i.print_game(screen)
            if i.hitbox.collidepoint((x,y)):
                i.print_box(screen)
        pygame.display.update()



if __name__ == "__main__":
    main_menu()
        