from tkinter import messagebox as msg
from enum import Enum

class PopupType(Enum):
    ERROR = 1
    WARNING = 2

class MessageBox:
    def __init__(self, message, type = PopupType.ERROR) -> None:
        self.title = "ERROR" if type == PopupType.ERROR else "WARNING"
        self.icon = "error" if type == PopupType.ERROR else "warning"
        self.message = message

    def display(self):
        return msg.askyesnocancel(self.title, self.message, icon=self.icon)

