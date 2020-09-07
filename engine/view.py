from engine.imports import *

class View(object):
    def __init__(self, refresh_rate: int = 60, width: int = 800, height: int = 600):
        # region [Public Variables]
        # Screen Parameters
        self.refresh_rate: int = refresh_rate
        self.width: int = width
        self.height: int = height
        self.project_name: str = "Mini Game - Snake"

        # endregion

        # region [Init]
        pygame.display.set_caption(self.project_name)
        self.screen: pygame.Surface = pygame.display.set_mode((self.width, self.height))
        # endregion
