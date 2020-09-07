from engine.imports import *
from game_objects.button import *
from resources.color_paletes.snake_colors import *
from game_states.state import *
from random import randint, sample


class SaperState(State):
    def __init__(self, state_stack: Deque[State]):
        super().__init__(is_pausable=True)

        # Private Variables
        self.state_stack: Deque[State] = state_stack
        self.is_finished: bool = False

        # Time
        self._time: float = 0
        self._seconds: int = 0
        self._minutes: int = 0

        # Game Objects
        self.font = Font()
        self.palette: Palette = Palette()

        self.texts: Dict[str, TextObject] = dict()
        self.buttons: Dict[str, Button] = dict()

        self.tile_size: int = 28
        self.tiles: Deque[Deque[Tile]] = deque()
        self.tile_type: Dict[str, str] = {'f': u'🚩', '*': u'💣', '?': u'❓', ' ': u' ', 'e': u'💥',
                                          '1': u'1', '2': u'2', '3': u'3', '4': u'4',
                                          '5': u'5', '6': u'6', '7': u'7', '8': u'8'}

        # Map
        self.backdrop: RoundedRect = RoundedRect(pygame.Rect(0, 0, 0, 0), color=self.palette.neutral, roundness=0.1)

        self.bomb_map: Tuple[Tuple[str]] = tuple()
        self.symbol_map: List[List[str]] = []
        self.visible_map: List[List[bool]] = []

        self.map_offset = 12
        self.map_size: pygame.Vector2 = pygame.Vector2(0, 0)

        self.bomb_count: int = 0
        self.flag_count: int = 0

        self.__init_buttons()
        self.__init_texts()
        self.reset_map()

    def __init_texts(self):
        # Time
        self.texts["TIME_NUM"] = TextObject(
            (700, 100), "", 32, color=self.palette.neutral)
        self.texts["TIME_STR"] = TextObject(
            (700, 50), u"🕰 Time", 48, color=self.palette.neutral, is_emoji=True)

        # Bomb
        self.texts["BOMB_NUM"] = TextObject(
            (700, 200), "", 32, color=self.palette.neutral)
        self.texts["BOMB_STR"] = TextObject(
            (700, 150), u"💣 Count", 48, color=self.palette.neutral, is_emoji=True)

        # Map
        self.texts["MAP_SIZE_NUM"] = TextObject(
            (700, 300), f"", 32, color=self.palette.neutral)
        self.texts["MAP_SIZE_STR"] = TextObject(
            (700, 250), u"🗺 Size", 48, color=self.palette.neutral, is_emoji=True)

        self.texts["WIN_STR"] = TextObject(
            (700, 350), f"", 32, color=self.palette.neutral)

    def __init_buttons(self):
        self.buttons['RESET'] = Button(
            "Reset", pygame.Rect(600, 450, 200, 50), 24, roundness=0.2, emoji=u'🔄', emoji_align=1 / 8)
        self.buttons['EXIT'] = Button(
            "Get Back", pygame.Rect(600, 500, 200, 50), 24, roundness=0.2, emoji=u'↩', emoji_align=1 / 8)

    def __init_map(self):
        # Init Variables
        self.map_size = pygame.Vector2(randint(4, 20), randint(4, 20))
        self.flag_count = 0

        self.bomb_count = randint((max_ := max(self.map_size.x, self.map_size.y)),
                                  max(self.map_size.x * self.map_size.y // 4, max_))

        (size_x, size_y) = map(int, self.map_size)
        size = size_x * size_y
        map_x = int(self.tile_size * size_x + self.map_offset + self.tile_size)
        map_y = int(self.tile_size * size_y + self.map_offset + self.tile_size)

        cur_offset = pygame.Vector2(300 - map_x // 2, 300 - map_y // 2)

        # Init Game Objects
        self.backdrop.set_rect(pygame.Rect(int(cur_offset.x), int(cur_offset.y), map_x, map_y))
        self.tiles: List[List[Tile]] = [
            [Tile('',
                  pygame.Rect(self.tile_size * x + int(cur_offset.x) + self.map_offset + self.tile_size // 4,
                              self.tile_size * y + int(cur_offset.y) + self.map_offset + self.tile_size // 4,
                              self.tile_size, self.tile_size),
                  font_size=24,
                  roundness=0.4)
             for y in range(size_y)]
            for x in range(size_x)]

        # Init Maps
        data: List[str] = sample('*' * self.bomb_count + ' ' * (size - self.bomb_count), size)
        data: List[List[str]] = [data[i:i + size_y] for i in range(0, len(data), size_y)]

        neigh = tuple(((-1, -1), (-1, 0), (-1, 1),
                       (0, -1), (0, 1),
                       (1, -1), (1, 0), (1, 1)))

        self.bomb_map: List[List[chr]] = [
            [(str(sum_)
              if (sum_ := sum(
                self.__is_safe((x := i + m), (y := j + n))
                and data[x][y] == '*'
                for m, n in neigh)) != 0
              else ' ') if data[i][j] != '*' else '*'
             for j in range(size_y)]
            for i in range(size_x)]

        self.visible_map: List[List[bool]] = [[False for _ in range(size_y)] for _ in range(size_x)]
        self.symbol_map: List[List[str]] = [[' ' for _ in range(size_y)] for _ in range(size_x)]

    def __is_safe(self, x, y):
        return self.map_size.x > x >= 0 and self.map_size.y > y >= 0

    def handle_events(self, events: List[pygame.event.EventType]):
        for button in self.buttons.values():
            button.handle_events(events)

        for x in range(int(self.map_size.x)):
            for y in range(int(self.map_size.y)):
                self.tiles[x][y].handle_events(events)

        if not self.is_finished: self.__handle_tiles()
        self.__handle_buttons()

    def __handle_buttons(self):
        if self.buttons['EXIT'].is_clicked and self.is_key_time():
            self.end_state()
        if self.buttons['RESET'].is_clicked and self.is_key_time():
            self.reset_map()

    def __handle_tiles(self):
        for x in range(int(self.map_size.x)):
            for y in range(int(self.map_size.y)):
                if self.tiles[x][y].is_clicked and self.is_key_time():
                    self.__uncover_tile(x, y)
                elif not self.visible_map[x][y] and self.tiles[x][y].is_right_clicked and self.is_key_time():
                    self.__switch_tile(x, y)

    def __is_digit(self, x, y):
        return self.bomb_map[x][y] not in ' *'

    def __is_bomb(self, x, y):
        return self.bomb_map[x][y] == '*'

    def __is_flag(self, x, y):
        return self.symbol_map[x][y] == 'f'

    def __is_unknown(self, x, y):
        return self.symbol_map[x][y] == '?'

    def __is_empty(self, x, y):
        return self.symbol_map[x][y] == ' '

    def __find_neigh_flags(self, i, j):
        return sum(self.__is_safe((x := i + m), (y := j + n)) and self.symbol_map[x][y] == 'f'
                   for m, n in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)])

    def __uncover_map(self):
        def set_tile(str_: str, color: pygame.Color):
            self.tiles[x][y].set_emoji(self.tile_type[str_])
            self.tiles[x][y].set_idle_color(color)

        for x in range(int(self.map_size.x)):
            for y in range(int(self.map_size.y)):
                if self.__is_bomb(x, y):
                    if self.__is_flag(x, y):
                        set_tile('*', self.palette.deep_green)
                    else:
                        set_tile('e', self.palette.red)
                else:
                    if self.__is_flag(x, y):
                        set_tile('f', self.palette.deep_red)
                    else:
                        set_tile(self.bomb_map[x][y], self.palette.blue)
                self.visible_map[x][y] = True

    def __uncover_tile(self, x, y):
        if not self.__is_flag(x, y):
            if self.__is_bomb(x, y):

                self.__uncover_map()
                self.tiles[x][y].set_emoji(self.tile_type['e'])
                self.tiles[x][y].set_idle_color(self.palette.deep_red)
                self.is_finished = True

            elif str(self.__find_neigh_flags(x, y)) == self.bomb_map[x][y]:
                self.__uncover_search(x, y, is_flag_click=True)

            elif self.__is_digit(x, y):
                self.visible_map[x][y] = True
                self.tiles[x][y].set_emoji(self.tile_type[self.bomb_map[x][y]])
                self.tiles[x][y].set_idle_color(self.palette.blue)
            else:
                self.__uncover_search(x, y)

    def __uncover_search(self, x, y, is_flag_click=False):
        def set_tile(i, j, color: pygame.Color):
            self.visible_map[i][j] = True
            self.tiles[i][j].set_emoji(self.tile_type[self.bomb_map[i][j]])
            self.tiles[i][j].set_idle_color(color)

        bomb_triggered: bool = False
        stack: Deque[Tuple[int, int]] = deque([(x, y)])
        while stack:
            (x, y) = stack.popleft()
            set_tile(x, y, self.palette.blue)
            for m, n in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                if (self.__is_safe((m := x + m), (n := y + n))
                        and not self.visible_map[m][n]
                        and self.symbol_map[m][n] != 'f'
                        and (self.bomb_map[m][n] != '*' or is_flag_click)):
                    if is_flag_click and self.bomb_map[m][n] == '*':
                        self.__uncover_map()
                        self.tiles[m][n].set_emoji(self.tile_type['e'])
                        self.tiles[m][n].set_idle_color(self.palette.deep_red)
                        bomb_triggered: bool = True
                        break

                    if self.bomb_map[m][n] == ' ':
                        stack.append((m, n))
                    set_tile(m, n, self.palette.blue)
            if bomb_triggered: break

    def __switch_tile(self, x, y):
        if self.__is_empty(x, y):
            self.symbol_map[x][y] = 'f'
            self.flag_count += 1
        elif self.__is_flag(x, y):
            self.symbol_map[x][y] = '?'
            self.flag_count -= 1
        else:
            self.symbol_map[x][y] = ' '

        self.tiles[x][y].set_emoji(self.tile_type[self.symbol_map[x][y]])

    def __finish_map(self):
        self.is_finished = True
        self.__uncover_map()

    def update(self, dt: float):
        self.__update_text(dt)

        self.update_key_time(dt)
        self.__update_buttons(dt)

        if self.is_finished: self.__update_win_text()
        else:
            self.__check_win()

    def __update_timer(self, dt: float):
        if not self.is_finished:
            self._time += dt
            self._seconds = int(self._time) % 60
            self._minutes = int(self._time // 60) % 60
            self.texts["TIME_NUM"].set_str(f'{f"{self._minutes}m " if self._minutes > 0 else ""}{self._seconds}s')

    def __update_bomb_counter(self):
        self.texts["BOMB_NUM"].set_str(f'{self.bomb_count - self.flag_count}')

    def __update_map_size(self):
        self.texts["MAP_SIZE_NUM"].set_str(f'{int(self.map_size.x)} x {int(self.map_size.y)}')

    def __update_buttons(self, dt: float):
        for button in self.buttons.values():
            button.update(dt)

    def __update_tile(self, x, y):
        self.tiles[x][y].set_emoji(self.tile_type[self.symbol_map[x][y]])

    def __update_text(self, dt):
        self.__update_timer(dt)
        self.__update_bomb_counter()
        self.__update_map_size()

    def __update_win_text(self):
        self.texts["WIN_STR"].set_str("It's Done!" if self.is_finished else '')

    def __check_win(self):
        self.is_finished = self.map_size.x*self.map_size.y - sum(sum(row) for row in self.visible_map) == self.bomb_count
        if self.is_finished:
            self.__uncover_map()

    def render(self, screen: pygame.SurfaceType):
        screen.fill(self.palette.background)
        self.__render_text(screen)
        self.__render_map(screen)
        self.__render_buttons(screen)

    def __render_buttons(self, screen):
        for button in self.buttons.values():
            button.render(screen)

        for row in self.tiles:
            for tile in row:
                tile.render(screen)

    def __render_text(self, screen):
        for text in self.texts.values():
            text.render(screen)

    def __render_map(self, screen):
        self.backdrop.render(screen)

    def reset_map(self):
        self.__init_map()
        self.is_finished: bool = False
        self.__update_win_text()

        self._time = 0
