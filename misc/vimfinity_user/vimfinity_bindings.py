from talon import actions, cron, Context, app

user = actions.user
edit = actions.edit


browser_context = Context()
browser_context.matches = r"""
tag: user.browser
"""

windows_context = Context()
windows_context.matches = r"""
os: windows
"""

draft_context = Context()
draft_context.matches = r"""
tag: user.draft_window_showing
"""

browser_context = Context()
browser_context.matches = r"""
tag: user.browser
"""

ide_context = Context()
ide_context.matches = r"""
tag: user.jetbrains
tag: user.emacs
"""


def press_backslash():
    """Press the backslash key. Useful when using a US keyboard in UK layout."""
    actions.key("\\")


def press_pipe():
    """Press the pipe key. Useful when using a US keyboard in UK layout."""
    # FIXMME: Nothing inserted when I call this
    actions.key("|")


def press_menu():
    """Press the menu key."""
    # actions.mouse_click(button=1)
    actions.key("menu")


def google_that():
    user.google_search(user.get_that_dwim())


def bind():
    try:
        user.vimfinity_bind_keys(
            {
                # Emacs Muscle Memory
                "enter": edit.save,
                ",": edit.cut,
                ".": edit.copy,
                "s": edit.find,
                "/": user.search,
                # Everything Else
                ":": user.toggle_gaze_track_dot,
                "g": user.mouse_grid_start,
                # TODO: "space": user.toggle_mark,
                "j": user.jump_click,
                # Compensate for using a US keyboard in UK layout
                "z": press_backslash,
                "Z": press_pipe,
                # Compensate for keyboards without a meny key
                "tab": press_menu,
                "+": edit.zoom_in,
                "-": edit.zoom_out,
                "o": "Open",
                "d": user.draft_current_textbox,
                "D": "Draft Window",
                "D s": user.draft_show,
                "D d": user.draft_current_textbox,
                "o": "Switch Program",
                "o f": user.open_firefox,
                "o c": user.open_chrome,
                "o d": user.open_discord,
                "o s": user.open_slack,
                "o r": user.open_rider,
                "o b": user.open_blender,
                "o w": user.open_whatsapp,
                "o e": user.open_emacs,
                "o t": user.focus_talon_log,
                "o T": user.focus_talon_repl,
                "o space": actions.app.window_hide,
                "m": "Mic",
                # For quicker access
                # This used to be backspace, but that caused too many false positives.
                "delete": user.toggle_mic_off,
                "m m": user.noisy_sleep,
                "m w": user.wake,
                "m space": user.toggle_mic_off,
                "e": "Emacs",
                "e e": user.open_current_file_in_emacs,
                "e p": user.open_current_project_in_emacs,
                "e g": user.send_to_magit_in_emacs,
                "=": "Utils",
                "= i": user.copy_current_app_info,
                "= p": user.command_history_show,
                "= h": user.command_history_hide,
                "= d": user.delete_speech_recordings,
                "= n": user.quarantine_speech_recording,
                "= t": user.emacs_search_talon_user,
                "= T": user.emacs_find_file_talon_user,
                # TODO: Swap these around?
                "?": google_that,
                "q": user.chatgpt_explain_thing,
                "Q": user.chatgpt_switch_start,
                # Override this with the program name in more local contexts
                "k": "Program-Specific",
            }
        )

        user.vimfinity_bind_keys(
            {
                "o m": user.open_task_manager,
                "o p": user.open_windows_terminal,
                # "o p": user.open_command_prompt,
                # "o P": user.open_powershell,
                "o x": user.open_windows_explorer,
                "o u": user.open_unreal_engine,
                "o g": user.open_epic_games,
                "= k": user.windows_cast_screen,
            },
            windows_context,
        )

        user.vimfinity_bind_keys(
            {
                "o ,": user.open_current_page_in_chrome,
                "o .": user.open_current_page_in_firefox,
                "p": "Page-Specific",
            },
            browser_context,
        )

        user.vimfinity_bind_keys(
            {
                # Hide all the base draft window commands
                "d": None,
                "D": None,
                "h": user.draft_hide,
                "f": user.draft_finish,
                "s": user.draft_finish_and_submit,
                "c": user.draft_cancel,
                "h": user.draft_hide,
            },
            draft_context,
        )

        user.vimfinity_bind_keys(
            {
                "k": user.rango_toggle_keyboard_clicking,
                "h": user.rango_disable,
                "r": user.rango_enable,
                # "t": actions.app.tab_open,
                # "w": actions.app.tab_close,
            },
            browser_context,
        )

        # TODO: Build, run, debug commands
        # user.vimfinity_bind_keys(
        #     {
        #         "b b": user.build_project,
        #         "b r": user.run_project,
        #         "b d": user.debug_project,
        #     },
        #     ide_context,
        # )

        print("Key sequences registered successfully.")
    except KeyError:
        # The action is not declared yet. Just re-run it on a delay.
        print("Failed to register key sequences. Retrying in 1s.")
        cron.after("1s", bind)


# HACK: Actions won't be registered on startup, so wait until they are.
cron.after("50ms", bind)
