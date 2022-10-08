from __future__ import annotations
from pyapp.ecs import Component

class TimeComp(Component):
    """
    """
    def __init__(self, start: float=-1) -> TimeComp:
        self.start = start
        self.dt: float = -1
