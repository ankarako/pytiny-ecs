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
    
    def create(self) -> Entity:
        """
        Create an entity
        """
        self.id_counter += 1
        entt = Entity(self.id_counter)
        self.entts[entt.id] = { }
        return self.entts[-1]
    
    def register(self, comp: Component, entt: Entity) -> None:
        """
        Associate a ``Component`` with an ``Entity``

        :param comp: The ``Component`` object to register.
        :param entt: The ``Entity`` object to associate with the component.
        """
        assert entt.id >= 0 and entt.id < len(self.entt_map)

        if type(comp) not in self.comps:
            self.comps[type(comp)] = []
        
        comp_id = len(self.comps[type(comp)])
        self.comps[type(comp)].append(comp)
        self.entts[entt.id][type(comp)] = comp_id

        if type(comp) not in self.mapping:
            self.mapping[type(comp)] = []
        self.mapping[type(comp)].append(entt.id)
            
    def view(self, comp_t: Component) -> List[Entity]:
        """
        Get a view of the entities that are associated with
        the specified component type.

        :param comp_t: The ``Component`` type to create the view from.
        """
        entt_ids = self.mapping[comp_t]
        return entt_ids
    
    def get(self, comp_t: Component, entt: Entity) -> Component:
        """
        Get the component of the specified type, that is associated
        with the specified ``Entity`` object.

        :param comp_t: The ``Component`` type to return.
        :param entt: The ``Entity`` object associated with the component.
        :return The specified ``Component`` object.
        """
        assert comp_t in self.mapping, f"The specified component type is not registered"
        assert entt.id in self.entts, f"The specified entity does not exist"
        comp_idx = self.entts[entt.id][comp_t]
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