from engine.imports import *

class Palette(object):
    def __init__(self):
        # Default
        self.background: pygame.Color = pygame.Color(41, 41, 37, 255)
        self.neutral: pygame.Color = pygame.Color(207, 207, 196, 255)
        self.blue: pygame.Color = pygame.Color(25, 126, 205, 255)

        self.red: pygame.Color = pygame.Color(205, 126, 25, 255)
        self.deep_red: pygame.Color = pygame.Color(205,25,25,255)

        self.green: pygame.Color = pygame.Color(25, 205, 126, 255)
        self.deep_green: pygame.Color = pygame.Color(25, 205, 25, 255)

        # Rect
        self.button_rect_idle: pygame.Color = pygame.Color(255, 102, 102, 255)
        self.button_rect_hover: pygame.Color = pygame.Color(204, 255, 153, 255)
        self.button_rect_active: pygame.Color = pygame.Color(51, 204, 51, 255)

        # Text
        self.button_text_idle: pygame.Color = pygame.Color(153, 51, 0, 255)
        self.button_text_hover: pygame.Color = pygame.Color(153, 102, 51, 255)
        self.button_text_active: pygame.Color = pygame.Color(51, 51, 0, 255)

