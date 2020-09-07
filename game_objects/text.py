from engine.font import *


class TextObject(object):
    def __init__(self,
                 pos: Tuple[int, int],
                 str_: str,
                 size: int,
                 style: int = 0,
                 color: pygame.Color = pygame.Color(0, 0, 0, 0),
                 is_centered: bool = True,
                 is_emoji: bool = False):
        font = Font()
        self.__font = font.emoji if is_emoji else font.font

        self.__str = str_
        self.__size = size
        self.__style = style
        self.__color: pygame.Color = pygame.Color(*color)
        self.__color.a = 255

        self.pos: pygame.Vector2 = pygame.Vector2(pos)

        self.__offset: pygame.Vector2 = pygame.Vector2(0, 0)
        self.__is_centered = is_centered
        self.shape: Optional[pygame.Surface] = None

        self.__update_shape()

    def __update_shape(self):
        offset: pygame.Rect
        self.shape, offset = self.__font.render(text=self.__str,
                                                fgcolor=self.__color,
                                                style=self.__style,
                                                rotation=0,
                                                size=self.__size)

        self.__offset = self.pos - pygame.Vector2(offset.size)//2 * self.__is_centered

    def render(self, screen: pygame.Surface):
        screen.blit(self.shape, self.__offset)

    def set_str(self, str_: str):
        if str_ != self.__str:
            self.__str = str_
            self.__update_shape()

    def set_size(self, size: int):
        if size != self.__size:
            self.__size = size
            self.__update_shape()

    def set_style(self, style):
        if style != self.__style:
            self.__style = style
            self.__update_shape()

    def set_color(self, color: pygame.Color):
        if color != self.__color:
            self.__color = color

    def __repr__(self):
        return f'TextObject({self.__str} @{self.pos})'
