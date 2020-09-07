from resources.color_paletes.snake_colors import *
from game_objects.rounded_rectangle import *
from game_objects.text import *


class Tile(object):
    def __init__(self,
                 emoji="",
                 rect: pygame.Rect = pygame.Rect(0, 0, 0, 0),
                 font_size: int = 24,
                 roundness: float = 0.5,
                 color: pygame.Color = pygame.Color(0, 0, 0, 0)):

        # Tile Parameters
        self.is_clicked: bool = False
        self.is_right_clicked: bool = False

        # Rounded Rect Parameters
        self.pos = rect
        self.rect: RoundedRect = RoundedRect(rect, color, roundness)
        self.rect.set_alpha(255)
        self.palette: Palette = Palette()

        # Text Parameters
        self.emoji: TextObject = TextObject((self.pos.x + self.pos.w // 2,
                                             self.pos.y + self.pos.h // 2),
                                            emoji,
                                            font_size, is_emoji=True)

    def handle_events(self, events: List[pygame.event.EventType]):
        self.is_clicked = False
        self.is_right_clicked = False

        # Idle
        if not self.__is_mouse_in_borders(*pygame.mouse.get_pos()):
            self.rect.set_color(self.palette.button_rect_idle)
        else:
            if any(event.type == pygame.MOUSEBUTTONUP and event.button == 1 for event in events):
                self.rect.set_color(self.palette.button_rect_active)
                self.is_clicked = True
            elif any(event.type == pygame.MOUSEBUTTONUP and event.button == 3 for event in events):
                self.rect.set_color(self.palette.button_rect_active)
                self.is_right_clicked = True
            else:
                self.rect.set_color(self.palette.button_rect_hover)

    def render(self, screen: pygame.Surface):
        self.rect.render(screen)
        if self.emoji: self.emoji.render(screen)

    def set_emoji(self, emoji):
        self.emoji.set_str(emoji)

    def set_idle_color(self, color: pygame.Color):
        self.palette.button_rect_idle = color

    def reset(self):
        self.is_clicked = False

    def __is_mouse_in_borders(self, pos_x, pos_y) -> bool:
        return (self.rect.border_right >= pos_x >= self.rect.border_left
                and self.rect.border_down >= pos_y >= self.rect.border_up)

    def __repr__(self):
        return f'Tile({self.emoji} @{self.rect})'

class Button(Tile):
    # RECT BOX | TEXT
    # / --- --- --- \
    # |     TXT     |
    # \ --- --- --- /
    # IDLE | HOVER | CLICK == >= <= /= ===
    def __init__(self,
                 str_: str = "",
                 rect: pygame.Rect = pygame.Rect(0, 0, 0, 0),
                 font_size: int = 24,
                 text_style=0,
                 roundness: float = 0.5,
                 color: pygame.Color = pygame.Color(0, 0, 0, 0),
                 emoji="",
                 emoji_align=0):

        # Button Parameters
        super().__init__(emoji, rect, font_size, roundness, color)
        self.__key_time_max: float = 1.5
        self.__key_time: float = self.__key_time_max

        # Text
        self.text: TextObject = TextObject((self.pos.x + self.pos.w // 2,
                                            self.pos.y + self.pos.h // 2),
                                           str_,
                                           font_size,
                                           text_style)

        self.emoji: Optional[TextObject] = (False
                                            if not emoji
                                            else TextObject((self.pos.x + int(emoji_align * self.pos.w),
                                                             self.pos.y + self.pos.h // 2),
                                                            emoji,
                                                            font_size,
                                                            is_emoji=True))

    def handle_events(self, events: List[pygame.event.EventType]):
        if self.__is_key_time():
            super().handle_events(events)
        else:
            self.rect.set_color(self.palette.button_rect_active)

    def update(self, dt: float):
        self.__update_key_time(dt)

    def __update_key_time(self, dt):
        if self.__key_time < self.__key_time_max:
            self.__key_time += dt

    def render(self, screen: pygame.Surface):
        super().render(screen)
        self.text.render(screen)

    def __is_key_time(self):
        if self.__key_time >= self.__key_time_max:
            if self.is_clicked or self.is_right_clicked:
                self.__key_time = 0
            return True
        return False

    def reset(self):
        super().reset()
        self.__key_time = self.__key_time_max

    def __repr__(self):
        return f'Button({self.text}+{self.emoji} @{self.rect})'
