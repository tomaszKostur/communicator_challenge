from multiprocessing.managers import BaseManager
from threading import Thread
from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.exceptions import ResizeScreenError, StopApplication,\
                                   NextScene
from asciimatics import widgets
from asciimatics.event import KeyboardEvent
import sys
from time import sleep
import argparse


class MessageServer():
    messages = []

    def add_message(self, message_text):
        self.messages.append(message_text)

    def get_messages(self):
        return self.messages

    def messages_len(self):
        return len(self.messages)


class RemoteManager(BaseManager):
    pass


RemoteManager.register('MessageServer', MessageServer)

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

        # Messages server section
        remote = RemoteManager(address=('127.0.0.1', 5000), authkey=b'123')
        remote.connect()
        self.message_server = remote.MessageServer()
        self.messages_len = self.message_server.messages_len()

        # Creating layout section
        self.msg_lay = widgets.Layout([100], fill_frame=True)
        self.add_layout(self.msg_lay)

        input_lay = widgets.Layout([100])
        self.add_layout(input_lay)
        input_text = widgets.TextBox(5, name='input_text')
        input_lay.add_widget(input_text)

        menu_lay = widgets.Layout([1, 1, ])
        self.add_layout(menu_lay)
        menu_lay.add_widget(widgets.Label("Press Enter to send"
                                          " or Tab to focus Quit button"), 0)
        menu_lay.add_widget(widgets.Button("Quit", self._quit), 1)

        self.fix()

        # monitor thread start
        self._monitor_thread()

    @staticmethod
    def _empty(*args, **kwargs):
        pass

    @staticmethod
    def _quit():
        raise StopApplication("User triggered quit")

    def _draw_new_messages(self, slice_idx_low, slice_idx_high):
        self.messages = self.message_server.get_messages()
        for msg in self.messages[slice_idx_low:slice_idx_high]:
            self.msg_lay.add_widget(widgets.Label(msg))
            self.fix()

    # TODO: register KeyboardEvent inside this class
    def _submit_text(self, event):
        if isinstance(event, KeyboardEvent):
            c = event.key_code
            if c == 10:  # Key "Line Feed" (enter)
                # TODO: I dont remember why should I save, or really should I?
                self.save()
                # Send text from input widget to message_server
                self.message_server.add_message(self.data['input_text'][0])
                # clear text input widget
                self.data = {'input_text': ['']}

    def _messages_monitoring_loop(self):
        # TODO: new messages APPEARS ONLY WHEN KEYBOAR EVENT!!
        # I need to creale good logging to debug it!
        while(True):
            m_len_old = self.messages_len
            self.messages_len = self.message_server.messages_len()
            if (m_len_old < self.messages_len):
                self._draw_new_messages(m_len_old, self.messages_len)

    def _monitor_thread(self):
        monitor_t = Thread(target=self._messages_monitoring_loop, daemon=True)
        monitor_t.start()


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


def set_server():
    manager = RemoteManager(address=('127.0.0.1', 5000), authkey=b'123')
    manager.get_server().serve_forever()


def get_args():
    parser = argparse.ArgumentParser(
        description='''Asciimatics version of simpliest communicator''')
    parser.add_argument('--server', action='store_true')
    return parser.parse_args()


if __name__ == "__main__":

    args = get_args()
    if args.server:
        set_server()
    else:
        try:
            Screen.wrapper(asciimatics_tui)
            sys.exit(0)
        except ResizeScreenError:
            pass
