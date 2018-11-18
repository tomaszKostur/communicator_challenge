from asciimatics.screen import Screen
from asciimatics import screen
from asciimatics.scene import Scene
from asciimatics.exceptions import ResizeScreenError, StopApplication, NextScene
from asciimatics import widgets
from asciimatics.event import KeyboardEvent
import sys
from time import sleep


data = {'messages': ['msg1', 'msg2'],
        'input_text': ['']
}

class DialogView(widgets.Frame):
    def __init__(self, screen, data):
        super().__init__(screen,
                         screen.height,
                         screen.width,
                         hover_focus=True,
                         can_scroll=True,
                         reduce_cpu=True,
                         data=data,
                         title="Communicator")

        self.messages = data['messages']

        self.msg_lay = widgets.Layout([100], fill_frame=True)
        self.add_layout(self.msg_lay)

        input_lay = widgets.Layout([100])
        self.add_layout(input_lay)
        input_text = widgets.TextBox(5, name='input_text')
        input_lay.add_widget(input_text)

        menu_lay = widgets.Layout([1, 1, ])
        self.add_layout(menu_lay)
        menu_lay.add_widget(widgets.Button("Send", self._empty), 0)
        menu_lay.add_widget(widgets.Button("Quit", self._quit), 1)

        self.fix()

    @staticmethod
    def _empty(*args, **kwargs):
        pass

    @staticmethod
    def _quit():
        raise StopApplication("User triggered quit")

    def _draw_messages(self):
        for msg in self.messages:
            self._add_msg(msg)

    def _add_msg(self, msg):
        self.msg_lay.add_widget(widgets.Label(msg))
        self.fix()

    def _submit_text(self, event):
        if isinstance(event, KeyboardEvent):
            c = event.key_code
            if c == 10:  # Key "Line Feed" (enter)
                self.save()
                self.messages = self.data['input_text']
                self.data = {'input_text': ['']}
                self._draw_messages()


def asciimatics_tui(screen):
    # container for scenes, played one afrer another
    scenes = []
    # Scene 1

    dialog = DialogView(screen, data)
    effects = [
        dialog
    ]

    scenes.append(Scene(effects, -1, name='main'))
    # This starts the work
    screen.play(scenes, stop_on_resize=True,
                unhandled_input=dialog._submit_text)  # register Keyboard Event


if __name__ == "__main__":
    try:
        Screen.wrapper(asciimatics_tui)
        sys.exit(0)
    except ResizeScreenError:
        pass
