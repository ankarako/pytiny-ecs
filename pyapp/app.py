from __future__ import annotations
from typing import Sequence

import os
import time
import imgui
import glfw
import OpenGL.GL as gl
from imgui.integrations.glfw import GlfwRenderer

import pyapp.ecs as ecs
from pyapp.event import EventEmitter
from pyapp.comps.app_tag import AppTag
from pyapp.comps.time_comp import TimeComp


def impl_glfw_init(win_name: str, w: int, h: int):
    """
    Initialize an OpenGL context.

    :param win_name: The name of the window to be created.
    :param w: The window width (in pixels).
    :param h: The window height (in pixels).
    """
    if not glfw.init():
        raise RuntimeError("Failed to initialize OpenGL context.")
    
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 0)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    # create the window
    window = glfw.create_window(w, h, win_name, None, None)
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        raise RuntimeError("Failed to initialize a window.")
    return window



class Application:
    """
    A simple application implementation, base on the ECS 
    system of pyapp.
    """
    def __init__(
        self, 
        name: str, 
        win_w: int, 
        win_h: int,
        systems: Sequence[ecs.ISystem]
    ) -> Application:
        """
        Construct the ``Application`` object

        :param name: The name of the application.
        :param win_w: The window width (in pixels).
        :param win_h: The window height (in pixels).
        :param systems: A list of the systems in the application.
        """
        self.name = name
        self.win_w = win_w
        self.win_h = win_h
        self.systems = systems

        # backend object 
        self.render_backend = None
        self.window = None

        # flags
        self.request_shutdown = False
        self.registry = None
    
    def init(self) -> None:
        """
        Initialize the application
        """
        # Create a registry
        self.registry = ecs.Registry()
        
        app_entt = self.registry.create()
        self.registry.register(AppTag(), app_entt)
        
        evnt_emitter = EventEmitter()
        self.registry.register(evnt_emitter, app_entt)

        # initialize graphics context
        if self.window is None:
            self.window = impl_glfw_init(self.name, self.win_w, self.win_h)
        
        # set glfw calbacks

        # create GUI context
        imgui.create_context()
        # configure fonts
        fonts = imgui.get_io().fonts
        # text_font = os.path.join(app_state.res_root, app_state.default_font_path)
        # icon_font = os.path.join(app_state.res_root, app_state.default_awfont_path)
        # app_state.text_font_instance = fonts.add_font_from_file_ttf(text_font, app_state.font_size)
        # app_state.aw_font_instance = fonts.add_font_from_file_ttf(icon_font, app_state.font_size)

        # create backend ogl renderer
        self.render_backend = GlfwRenderer(self.window)
        self.render_backend.refresh_font_texture()


        # initialize all the systems
        for system in self.systems:
            system.init(self.registry)
    
    def update(self) -> None:
        """
        """
        app_entt = self.registry.view(AppTag)
        time_comp: TimeComp = self.registry.get(TimeComp, app_entt)
        time_comp.start = time.perf_counter()

        # run frame code
        if glfw.window_should_close(self.window):
            self.request_shutdown = True
        
        glfw.poll_events()
        self.render_backend.process_inputs()

        imgui.new_frame()
        for system in self.systems:
            system.update(self.registry)

        gl.glClearColor(0.0, 0.0, 0.0, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.end_frame()
        imgui.render()
        self.render_backend.render(imgui.get_draw_data())

        glfw.swap_buffers(self.window)

        time_comp.dt = time.perf_counter() - time_comp.start

    def shutdown(self) -> None:
        """
        """
        for system in self.systems:
            system.shutdown()
        
        self.render_backend.shutdown()
        glfw.terminate()

