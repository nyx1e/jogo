import pygame, sys
from level import *
from player import Player
from objetos import Tile

width,heigth = 900,500
FPS = 60
tamanho_bloco = 32

class Game:
    def __init__(self):
        #settup
        pygame.init()
        self.screen = pygame.display.set_mode((width,heigth))
        pygame.display.set_caption('Desventuras em Série')
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self): #td q acontece dentro do jogow
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #sair
                    pygame.quit()
                    sys.exit()

            #draw
            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()