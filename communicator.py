from multiprocessing.managers import BaseManager
import argparse
from time import sleep
import sys
from threading import Thread, Event
import signal
import logging


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()


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


class BasicTui():
    exit_program = False

    def __init__(self):
        signal.signal(signal.SIGINT, self._exit)
        self.stop_event = Event()

        remote = RemoteManager(address=('127.0.0.1', 50000), authkey=b'123')
        remote.connect()
        self.message_server = remote.MessageServer()
        self.messages_len = self.message_server.messages_len()

    def _exit(self, signum, frame):
        print('_exit function')
        self.stop_event.set()

    def _new_messages(self):
        messages_len = self.message_server.messages_len()
        if messages_len != self.messages_len:
            new_messages = self.message_server.get_messages()[
                                self.messages_len:messages_len]
            self.messages_len = messages_len
            return new_messages
        else:
            return []

    def _stdout_loop(self, stop_event):
        while(not stop_event.is_set()):
            sys.stdout.writelines(self._new_messages())
            # TODO: remove sleep oriented programming
            sleep(0.1)
        print('out of _stdout_loop')

    def stdout_thread(self):
        stdout_t = Thread(target=self._stdout_loop, args=(self.stop_event,))
        stdout_t.start()

    def _stdin_loop(self, stop_event):
        ''' I couldn't find standard solution for gracefully stop this loop
            in thread. So this should be run in "daemon" thread.'''
        while(True):
            msg = sys.stdin.readline()
            self.messages_len += 1
            self.message_server.add_message(msg)

    def stdin_thread(self):
        stdin_t = Thread(target=self._stdin_loop, args=(self.stop_event,),
                         daemon=True)
        stdin_t.start()

    def communicator_loop(self):
        self.stdout_thread()
        self.stdin_thread()
        while(not self.stop_event.is_set()):
            # TODO: remove sleep oriented programming
            sleep(0.1)

        print('out of communicator_loop')


def set_server():
    manager = RemoteManager(address=('127.0.0.1', 50000), authkey=b'123')
    manager.get_server().serve_forever()


def get_args():
    parser = argparse.ArgumentParser(description='My awesome communicator')
    parser.add_argument('--server', action='store_true')
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    if args.server:
        set_server()
    else:
        tui = BasicTui()
        tui.communicator_loop()
