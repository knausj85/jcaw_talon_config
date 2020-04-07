from typing import Callable, List
import logging
import time

from talon import Module, Context, actions, settings, ctrl, cron, speech_system, noise
from talon.track.geom import Point2d
from talon_plugins import eye_zoom_mouse

from user.utils import sound, Modifiers
from user.misc.mouse import Click


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


def zoom_mouse_active():
    """Is the zoom mouse an active mouse mode?"""
    try:
        return eye_zoom_mouse.zoom_mouse.enabled
    except AttributeError:
        return False


def is_zooming():
    """Is the zoom mouse currently zooming?"""
    return eye_zoom_mouse.zoom_mouse.state == eye_zoom_mouse.STATE_OVERLAY


module = Module()
module.setting(
    "click_sounds",
    type=bool,
    default=True,
    desc="play sounds when zoom clicks are buffered (or cancelled)",
)


# TODO: Pull this out once talon exposes mouse mode scopes by default
@module.scope
def scope(*_):
    zoom_mouse = zoom_mouse_active()
    return {
        "zoom_mouse_active": zoom_mouse,
        "zoom_mouse_zooming": zoom_mouse and is_zooming(),
    }


speech_system.register("pre:phrase", scope.update)
# Noises won't trigger pre:phrase - bind them so we definitely catch the zoom.
noise.register("post:pop", scope.update)
noise.register("pre:hiss", scope.update)


@module.action_class
class Actions:
    def end_zoom() -> Point2d:
        """Terminate the zoom.

        Mouse will be moved to the user's gaze position.

        :returns: the final position

        """
        # TODO: Will this be reactive enough, or should we make this accessible
        #   anywhere in the zoom mouse?
        _, origin = eye_zoom_mouse.zoom_mouse.get_pos()
        if origin:
            eye_zoom_mouse.zoom_mouse.cancel()
            actions.mouse_move(origin.x, origin.y)
        return origin

    def queue_zoom_action(function: Callable):
        """Create a command that queues a specific click type on the next zoom.

        For example, we can queue a right click - next time the user pops out of
        the zoom, a right click will be performed instead of a left click.

        """

        def do_action(position):
            """Perform the queued action at `position`."""
            nonlocal function
            LOGGER.debug(f"Performing queued zoom function `{function}` at {position}")
            actions.mouse_move(position.x, position.y)
            function()

        LOGGER.debug(f"Queuing zoom function `{function}`")
        eye_zoom_mouse.zoom_mouse.queue_action(do_action)
        if settings["self.click_sounds"]:
            sound.play_ding()

    def clear_zoom_queue():
        """Clear all queued zoom mouse actions."""
        # Possible race here. Not important or likely to happen; tolerate it.
        if not eye_zoom_mouse.zoom_mouse.queued_actions.empty():
            eye_zoom_mouse.zoom_mouse.cancel_actions()
            if settings["self.click_sounds"]:
                sound.play_cancel()


context = Context()
context.matches = r"""
user.zoom_mouse_active: True
"""


@context.action_class("user")
class MouseActions:
    def drop(modifiers: List[str] = []):
        # Some drag actions require that the mouse wait in the drop position
        # for a little while before dropping. Movement is instant with the zoom
        # mouse, so insert an artificial wait.
        time.sleep(0.3)
        # TODO: Port to newapi actions once I know the interface
        ctrl.mouse_click(button=0, up=True)
        Modifiers(modifiers).__exit__(None, None, None)

    def default_click(click_info: Click):
        modifiers = click_info.modifiers
        actions.self.queue_zoom_action(lambda: click_info.function(modifiers))

        # If we're dragging, it means we intend to drop, so we can queue both
        # at once.
        #
        # HACK: Intercepting the function here is pretty hacky.
        #
        # TODO: Remove `str` cast once action path comparison works
        if str(click_info.function) == str(actions.user.drag):

            def queue_drop():
                nonlocal modifiers
                actions.user.queue_zoom_action(lambda: actions.user.drop(modifiers))

            # Add drop on a delay so the ding rings twice.
            cron.after("150ms", queue_drop)


# HACK: Unbind the default zoom_mouse pop, manually bind it ourselves so we can
#   override the pop binding with other contexts.
#
#   Unbind before every pop to reset the unbind when the zoom mouse is
#   restarted.
noise.register(
    "pre:pop", lambda *_: noise.unregister("pop", eye_zoom_mouse.zoom_mouse.on_pop)
)


@context.action_class("user")
class NoiseActions:
    def on_pop():
        # Manually invoke zoom mouse's own handler
        eye_zoom_mouse.zoom_mouse.on_pop(True)

    def on_hiss(start: bool):
        try:
            # This is currently a private module. Use if available.
            from user.utils import scroll
        except ImportError:
            print("Scroll module not found. It must be manually added.")
        if start:
            scroll.start()
        else:
            scroll.stop()
