from engine.imports import *
from game_objects.button import *
from resources.color_paletes.snake_colors import *
from game_states.state import *


class SnakeGameState(State):
    class Chunk(object):
        def __init__(self, pos: Tuple[int, int]):
            self.pos = pygame.Vector2(pos)
            self.next_pos = None

    def __init__(self, state_stack: Deque[State]):
        super().__init__(is_pausable=True)

        # Private Variables
        self._state_stack: Deque[State] = state_stack
        self._palette: Palette = Palette()
        self._buttons: Dict[str, Button] = dict()
        self._texts: Dict[str, TextObject] = dict()

        # Game Variables
        self.score: int = 0
        self.length: int = 1
        self.move_direction: pygame.Vector2 = pygame.Vector2(0, 0)
        self.time_between_moves_max: float = 2
        self.time_between_moves: float = self.time_between_moves_max

        self.point_pos: Optional[pygame.Vector2] = None

        self.body_chunks_tiles = None
        self.speed: int = 1

        self._init_buttons()
        self._init_texts()


    def _init_texts(self):
        self._texts["SCORE_STR"] = TextObject((700, 50), u"🍀 Score", 48,
                                              color=self._palette.neutral,
                                              style=freetype.STYLE_STRONG,
                                              is_emoji=True)
        self._texts["SCORE_NUM"] = TextObject((700, 100), "", 48, color=self._palette.neutral)

    def _init_buttons(self):
        self._buttons['EXIT'] = Button("Get Back", pygame.Rect(600, 500, 200, 50), 24, roundness=0.2)

    def handle_points(self):
        pass

    def update_movement(self):
        pass

    def handle_input(self, events: List[pygame.event.EventType]):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                self.move_direction = pygame.Vector2(0, 1)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.move_direction = pygame.Vector2(0, -1)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                self.move_direction = pygame.Vector2(-1, 0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                self.move_direction = pygame.Vector2(0, 1)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                self.speed = 5

            if event.type == pygame.KEYUP and event.key == pygame.KEYDOWN:
                self.speed = 1

    def update_score(self):
        pass

    def handle_events(self, events):
        for button in self._buttons.values():
            button.handle_events(events)
        self._handle_buttons()

    def update(self, dt: float):
        self.update_key_time(dt)
        self._update_buttons(dt)

    def _update_buttons(self, dt: float):
        for button in self._buttons.values():
            button.update(dt)

    def _update_text(self):
        pass

    def render(self, screen: pygame.SurfaceType):
        screen.fill(self._palette.background)
        self._render_buttons(screen)
        self._render_text(screen)

    def _render_buttons(self, screen):
        for button in self._buttons.values():
            button.render(screen)

    def _render_text(self, screen):
        for text in self._texts.values():
            text.render(screen)

    def _handle_buttons(self):
        if self._buttons['EXIT'].is_clicked and self.is_key_time():
            self.end_state()

    def _handle_score(self):
        pass
