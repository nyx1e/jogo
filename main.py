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
        self.font = pygame.font.Font('assets/fonte/Eight-Bit Madness.ttf', 18)
        self.game_start = False
        self.level = Level()

    def run(self): #td q acontece dentro do jogow
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #sair
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: #nível começa
                        self.game_start = True
                    if event.key == pygame.K_c:
                        self.level.menu_pausa()


            #draw
            self.screen.fill('black')
            title = self.font.render(f'Press SPACE to start', False, 'white')
            title_rect = title.get_rect(center = (width/2, 400))
            self.screen.blit(title, title_rect)
            if self.game_start:
                self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()