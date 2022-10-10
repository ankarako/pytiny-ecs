# pytiny-ecs
 A very small python library for implementing basic Entity-Component-System (ECS) structures.
 The main structure of the library is the ``Registry``, with which you can create entities, and attach
 components onto them.

 The library additionally provides an interface for systems ``ISystem``, and some basic components, such as an ``EventEmitter`` and a base class for ``Event``s. Furthermore, it provides a simple structure that implements an applications entry-point, and uses [imgui](https://github.com/ocornut/imgui) for creating GUIs.
