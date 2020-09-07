from game_objects.button import *

from PIL import Image, ImageFilter


class TransparentScreen(object):
    def __init__(self,
                 width: int,
                 height: int,
                 str_: str = "Pause",
                 rect: pygame.Rect = None,
                 color: pygame.Color = None,
                 alpha: int = 200,
                 roundness: float = 0.5):
        # Private Variables
        self.__width = width
        self.__height = height
        self.__image_mode: str = 'RGBA'
        self.__str: str = str_
        self.__roundness: float = roundness
        self.is_closed: bool = False

        # Text and Buttons
        self.texts: Dict[str, TextObject] = dict()
        self.buttons: Dict[str, Button] = dict()

        self.__init_texts()
        self.__init_buttons()

        # Shapes
        self.__screen_blurred: pygame.Surface = pygame.Surface((0, 0))

        self.__rect = rect if rect else pygame.Rect(self.__width // 3, 0, self.__width // 3, self.__height)
        self.__color = color if color else (0, 0, 0)
        self.__alpha = alpha

        self.__screen_pulpit = pygame.Surface(self.__rect.size, pygame.SRCALPHA)
        self.__screen_pulpit.fill((*self.__color, self.__alpha))

        # Public Variables
        self.is_blurred: bool = False

    def handle_events(self, events):
        for button in self.buttons.values():
            button.handle_events(events)
        if self.buttons['EXIT'].is_clicked:
            self.is_closed = True

    def update(self, dt):
        for button in self.buttons.values():
            button.update(dt)

    def render(self, screen: pygame.Surface):
        if not self.is_blurred: self.__blur_screen(screen)
        screen.blit(self.__screen_blurred, (0, 0))
        self.__render_buttons(screen)

    def __blur_screen(self, screen):
        screen_blurred = Image.frombytes(self.__image_mode,
                                         (self.__width, self.__height),
                                         pygame.image.tostring(screen, self.__image_mode)
                                         ).filter(ImageFilter.GaussianBlur(radius=6))

        self.__screen_blurred: pygame.Surface = pygame.image.fromstring(
            screen_blurred.tobytes("raw", self.__image_mode),
            (self.__width, self.__height),
            self.__image_mode)

        self.__screen_blurred.blit(self.__screen_pulpit, self.__rect.topleft)

        for text in self.texts.values():
            text.render(self.__screen_blurred)

        self.is_blurred = True

    def __init_texts(self):
        self.texts["PAUSE"] = TextObject((int(self.__width // 2)
                                          , int(self.__height // 3))
                                         , self.__str
                                         , 48
                                         , color=pygame.Color(207, 207, 196))

    def __init_buttons(self):
        self.buttons["EXIT"] = Button("Continue",
                                      pygame.Rect(int(self.__width // 2) - 100, int(2 * self.__height // 5), 200, 50)
                                      , 24
                                      , roundness=self.__roundness)

    def __render_buttons(self, screen):
        for button in self.buttons.values():
            button.render(screen)

    def reset(self):
        self.is_closed = False
        self.is_blurred = False
        for button in self.buttons.values():
            button.reset()
