from __future__ import annotations
from typing import Callable, Dict
from pyapp.ecs import Registry

class Event:
    def __init__(self, reg: Registry) -> Event:
        self.reg = reg


class EventEmitter:
    """
    A very simple object for handling callbacks
    """
    def __init__(self) -> EventEmitter:
        """
        Initialize the ``EventEmitter``.
        """
        self.evnt_clbks: Dict[Event, Callable[[Event], None]] = { }
    
    def on(self, evnt_t: Event, clbk: Callable[[Event], None]) -> None:
        """
        Register a callback for a specific event type
        """
        if evnt_t not in self.evnt_clbks.keys():
            self.evnt_clbks[evnt_t] = []
        self.evnt_clbks[evnt_t].append(clbk)
    
    def publish(self, event: Event) -> None:
        """
        Publish an event. All the registered callback for 
        the specified ``Event`` type will be run in a blocking manner.

        :param event: The ``Event`` object to publish.
        """
        if type(event) not in self.evnt_clbks.keys():
            raise ValueError(f"Event type `{type(event)}` is not registered with the EventEmitter.")
        for registered in self.evnt_clbks[type(event)]:
            registered(event)