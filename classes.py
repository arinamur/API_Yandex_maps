import pygame


class Skelet:
    def __init__(self, text, x, y):
        self.text = text
        self.font = pygame.font.Font(None, 25)
        self.get_render(x, y)

    def check_click(self, coords):
        return self.rect.x <= coords[0] <= self.rect.x + self.rect.w and \
               self.rect.y <= coords[1] <= self.rect.y + self.rect.h

    def get_render(self, x, y):
        self.text_r = self.font.render(self.text, True, pygame.Color('black'))
        self.rect = pygame.rect.Rect(
            *[x, y, self.text_r.get_width() + 6, self.text_r.get_height() + 4])


class Button(pygame.sprite.Sprite, Skelet):
    def __init__(self, text, x, y, *groups):
        super().__init__(*groups)
        Skelet.__init__(self, text, x, y)

    def render(self, screen):
        pygame.draw.rect(screen, pygame.Color('gray'), self.rect)
        screen.blit(self.text_r, (self.rect.x + 3, self.rect.y + 2))


class InputAddress(pygame.sprite.Sprite, Skelet):
    def __init__(self, text, x, y, *groups):
        super().__init__(*groups)
        Skelet.__init__(self, text, x, y)
        self.x, self.y = x, y
        self.colors = [(255, 255, 255), (80, 120, 255)]
        self.active = False

    def render(self, screen):
        self.get_render(self.x, self.y)
        pygame.draw.rect(screen, self.colors[self.active], self.rect)
        screen.blit(self.text_r, (self.rect.x + 3, self.rect.y + 2))
