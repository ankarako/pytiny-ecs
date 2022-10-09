from pyapp.ecs import Component

class InputComp(Component):
    def __init__(self) -> None:
        self.scroll_x: float = 0.0
        self.scroll_y: float = 0.0
        self.scroll_dx: float = 0.0
        self.scroll_dy: float = 0.0

        self.listener = None