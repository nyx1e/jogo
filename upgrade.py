import pygame

class Upgrade:
    def __init__(self, player):
        self.display_surf = pygame.display.get_surface()
        self.player = player
        self.atribute_number = len(player.stats)
        self.atribute_name = list(player.stats.keys())
        self.max_value = list(player.max_stats.values())
        self.font = pygame.font.Font('assets/fonte/Eight-Bit Madness.ttf', 18)
        self.height = self.display_surf.get_size()[1] * 0.7
        self.width = self.display_surf.get_size()[0] // 6
        self.create_items()
        #selecao
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True

    def input(self):
        keys = pygame.key.get_pressed()
        if self.can_move:
            if keys[pygame.K_RIGHT] and self.selection_index < self.atribute_number - 1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT] and self.selection_index >= 1:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.item_list[self.selection_index].trigger(self.player)

    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_move = True

    def create_items(self):
        self.item_list = []
        for item, index in enumerate(range(self.atribute_number)):
            incremento = self.display_surf.get_size()[0]// self.atribute_number
            left = (item * incremento) + (incremento - self.width) // 2
            top = self.display_surf.get_size()[1] * 0.1
            item = Item(left, top, self.width, self.height, index, self.font)
            self.item_list.append(item)

    def display(self):
        self.input()
        self.selection_cooldown()
        for index, item in enumerate(self.item_list):
            name = self.atribute_name[index]
            value = self.player.get_value_index(index)
            max_value = self.max_value[index]
            cost = self.player.get_cost_index(index) #aumenta o custo com base na lista presente na classe player 
            item.display(self.display_surf, self.selection_index, name, value, max_value, cost)

class Item:
    def __init__(self, left, top, width, height, index, font):
        self.rect = pygame.Rect(left, top, width, height)
        self.index = index
        self.font = font

    def display_names(self, surf, name, cost, selected):
        color = 'gold' if selected else '#EEEEEE'
        title = self.font.render(name, False, color)
        title_rect = title.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,20))
        cost = self.font.render(f'cost {int(cost)} exp', False, color)
        cost_rect = cost.get_rect(midbottom = self.rect.midbottom - pygame.math.Vector2(0,20))
        surf.blit(title, title_rect)
        surf.blit(cost, cost_rect)
    
    def display_bar(self, surf,  value, max_value, selected):
        top = self.rect.midtop + pygame.math.Vector2(0,60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0,60)
        color = 'gold' if selected else 'white'
        tamanho_completo = bottom[1] - top[1]
        posicao_relativa = (value/max_value) * tamanho_completo
        value_rect = pygame.Rect(top[0] - 10,bottom[1] - posicao_relativa, 20, 5)
        pygame.draw.line(surf, color, top, bottom, 5)
        pygame.draw.rect(surf, color, value_rect)

    def trigger(self, player):
        upgrade_attr = list(player.stats.keys())[self.index]
        if player.exp >= player.upgrade_cost[upgrade_attr] and player.stats[upgrade_attr] < player.max_stats[upgrade_attr]:
            player.exp -= player.upgrade_cost[upgrade_attr]
            player.stats[upgrade_attr] *= 1.2
            player.upgrade_cost[upgrade_attr] *= 1.4
        if player.stats[upgrade_attr] > player.max_stats[upgrade_attr]:
            player.stats[upgrade_attr] = player.max_stats[upgrade_attr]

    def display(self, surf, selection_num, name, value, max_value, cost):
        if self.index == selection_num:
            pygame.draw.rect(surf, '#222222', self.rect)
            pygame.draw.rect(surf, 'gold', self.rect, 4)
        else:
            pygame.draw.rect(surf, '#222222', self.rect)
            pygame.draw.rect(surf, 'black', self.rect, 4)
        self.display_names(surf,name,cost, self.index == selection_num)
        self.display_bar(surf,  value, max_value, self.index == selection_num)