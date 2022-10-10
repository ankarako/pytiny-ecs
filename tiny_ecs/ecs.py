from __future__ import annotations
from typing import List


class Component:
    """
    A simple base object for components to inherit from.
    """
    def __init__(self) -> Component:
        pass


class Entity:
    """
    Represents an object that be associated
    with ``Component``s
    """
    def __init__(self, id: int=-1) -> Entity:
        self.id = id


class Registry:
    """
    Basically a collection of arrays of components,
    keeping components of the same type in the same 
    array, and mapping them to its corresponding entities
    """
    def __init__(self) -> Registry:
        """
        Instantiate a registry
        """
        self.comps = { }
        self.entts = { }
        self.mapping = { }
        self.id_counter = -1
    
    def create(self) -> int:
        """
        Create an entity
        """
        self.id_counter += 1
        entt = Entity(self.id_counter)
        self.entts[entt.id] = { }
        return entt.id
    
    def register(self, comp: Component, entt: int) -> None:
        """
        Associate a ``Component`` with an ``Entity``

        :param comp: The ``Component`` object to register.
        :param entt: The ``Entity`` object to associate with the component.
        """
        entt
        assert entt >= 0 and entt < len(self.entts)

        if type(comp) not in self.comps:
            self.comps[type(comp)] = []
        
        comp_id = len(self.comps[type(comp)])
        self.comps[type(comp)].append(comp)
        self.entts[entt][type(comp)] = comp_id

        if type(comp) not in self.mapping:
            self.mapping[type(comp)] = []
        self.mapping[type(comp)].append(entt)
            
    def view(self, comp_t: Component) -> List[int]:
        """
        Get a view of the entities that are associated with
        the specified component type.

        :param comp_t: The ``Component`` type to create the view from.
        """
        entt_ids = self.mapping[comp_t]
        return entt_ids
    
    def get(self, comp_t: Component, entt: int) -> Component:
        """
        Get the component of the specified type, that is associated
        with the specified ``Entity`` object.

        :param comp_t: The ``Component`` type to return.
        :param entt: The ``Entity`` object associated with the component.
        :return The specified ``Component`` object.
        """
        if comp_t not in self.mapping:
            return None
        assert entt in self.entts.keys(), f"The specified entity does not exist"
        comp_idx = self.entts[entt][comp_t]
        return self.comps[comp_t][comp_idx]


class ISystem:
    """
    A simple system interface to be implemented by systems.
    This does not restrict the developer to implement systems as
    ``ISystem``s. The developer can use all the registry and
    create other abstractions for systems.
    """
    def __init__(self) -> ISystem:
        """
        Construct a system
        """

    def init(self, reg: Registry) -> None:
        """
        Initialize the system.
        """
        pass
    
    def update(self, reg: Registry) -> None:
        """
        Perform one system update step
        """
        pass

    def shutdown(self, reg: Registry) -> None:
        """
        Shutdown the system.
        """
        pass