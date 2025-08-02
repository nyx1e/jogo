import pygame, sys
from level import *
from player import Player
from objetos import *

width, heigth = 900,500
FPS = 60
tamanho_bloco = 32

class Game:
    def __init__(self):
        #settup
        pygame.init()
        self.screen = pygame.display.set_mode((width,heigth))
        icone = pygame.image.load('assets/pergaminho.jpg')
        pygame.display.set_icon(icone)
        pygame.display.set_caption('Tales of a Swordsman')
        self.clock = pygame.time.Clock()
        self.font1 = pygame.font.Font('assets/fonte/BreatheFireIii-PKLOB.ttf', 85)
        self.font2 = pygame.font.Font('assets/fonte/Eight-Bit Madness.ttf', 25)
        self.image = pygame.image.load('assets/capa.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (900, 500))
        self.rect = self.image.get_rect(center = (width/2,heigth/2))
        self.level = Level()

        #texto do início
        self.button_start = pygame.Rect(350, 325, 200, 50)
        self.button_controls = pygame.Rect(350, 390, 200, 50)
        self.button_controls_out = pygame.Rect(350, 440, 200, 50)
        self.title = self.font1.render(f'Tales of a Swordsman', False, 'white')
        self.title_rect = self.title.get_rect(center = (width/2, 200))
        self.text1 = self.font2.render(f'START', False, 'white')
        self.text_rect1 = self.text1.get_rect(center = self.button_start.center)
        self.text2 = self.font2.render(f'CONTROLS', False, 'white')
        self.text_rect2 = self.text2.get_rect(center = self.button_controls.center)
        self.text3 = self.font2.render(f'BACK', False, 'white')
        self.text_rect3 = self.text3.get_rect(center = self.button_controls_out.center)

        #texto controles
        self.scroll = pygame.image.load('assets/scroll.png').convert_alpha()
        self.scroll = pygame.transform.scale(self.scroll, (900, 600))
        self.scroll_text = pygame.image.load('assets/controls.png').convert_alpha()
        self.scroll_text = pygame.transform.scale(self.scroll_text, (650, 300))
        self.scroll_rect = self.scroll.get_rect(center = (width/2 - 10,heigth/2))
        self.scroll_text_rect = self.scroll_text.get_rect(center = (width/2 + 10,heigth/2))

        #variaveis de estado de jogo
        self.controls = False
        self.game_start = False
        self.gameover = self.level.gameover

    def run(self): #td q acontece dentro do jogow
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #sair
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c: #pausa e upgrade display
                        self.level.menu_pausa()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_start.collidepoint(event.pos): #nível começa
                        self.game_start = True
                    if self.button_controls.collidepoint(event.pos): #mostra os controles q podem ser usados
                        self.controls = True
                    if self.button_controls_out.collidepoint(event.pos): #sai dos controles
                        self.controls = False

            #draw
            self.screen.blit(self.image, self.rect)
            pygame.draw.rect(self.screen, '#111111', self.button_start)
            pygame.draw.rect(self.screen, 'gold', self.button_start, 4)
            pygame.draw.rect(self.screen, '#111111', self.button_controls)
            pygame.draw.rect(self.screen, 'gold', self.button_controls, 4)
            self.screen.blit(self.title, self.title_rect)
            self.screen.blit(self.text1, self.text_rect1)
            self.screen.blit(self.text2, self.text_rect2)
            if self.controls:
                self.screen.blit(self.scroll, self.scroll_rect)
                self.screen.blit(self.scroll_text, self.scroll_text_rect)
                pygame.draw.rect(self.screen, '#111111', self.button_controls_out)
                pygame.draw.rect(self.screen, 'gold', self.button_controls_out, 4)
                self.screen.blit(self.text3, self.text_rect3)
            if self.game_start:
                self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()