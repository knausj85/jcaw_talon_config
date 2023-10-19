from talon import Context, Module, actions, clip, ui

key = actions.key
insert = actions.insert
user = actions.user
sleep = actions.sleep


module = Module()


@module.action_class
class Actions:
    def open_current_page_in_chrome():
        """Open the current web page in Google Chrome."""

    def browser_address_backup() -> str:
        """Backup action to get the current URL.

        This can be used in place of `broser.address` when implementing
        `browser.address` would cause Talon to start automatically calling
        invasive procedures.

        """
        actions.browser.focus_address()
        actions.edit.select_all()
        with clip.capture() as c:
            actions.edit.copy()
        url = c.text()
        if not isinstance(url, str):
            raise ValueError(
                f"`url` should be a string. Was: {type(url)}, value: {url}"
            )
        return url

    def switch_start_chrome():
        """Switch to Chrome if it's running, otherwise start it."""


ctx = Context()
ctx.matches = r"""
tag: user.browser
"""


@ctx.action_class("edit")
class EditActions:
    def zoom_in():
        actions.key("ctrl-plus")

    def zoom_out():
        actions.key("ctrl-minus")


@ctx.action_class("browser")
class BrowserActions:
    def go(url: str):
        actions.browser.focus_address()
        clip.set_text(url)
        actions.edit.paste()
        # FIXME: Enter isn't carrying through - just stays in the address bar (Windows 10)
        key("enter")


@ctx.action_class("user")
class UserActions:
    def go_back() -> None:
        key("alt-left")

    def go_forward() -> None:
        key("alt-right")

    def open_current_page_in_chrome():
        url = actions.user.browser_address_backup()
        print(f"URL: {url}")
        actions.self.switch_or_start("chrome")

        actions.app.tab_open()
        actions.browser.go(url)
