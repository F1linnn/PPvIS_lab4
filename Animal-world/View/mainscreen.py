import os
import Utility.dialog_windows as window
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.screen import Screen
from kivymd.uix.snackbar import Snackbar


class ScreenView(MDScreen):

    controller = ObjectProperty()
    model = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.model.add_observer(self)
        self.screen = Screen()
        self.dialog = None

    def open_dialog(self, mode: str):
        if mode == "input":
            self.dialog = window.InputWindow(model=self.model, controller=self.controller)
        elif mode == "delete":
            self.dialog = window.DeleteWindow(model=self.model, controller=self.controller)
        elif mode == "upload":
            self.dialog = window.UploadWindow(model=self.model, controller=self.controller)
        elif mode == "save":
            self.dialog = window.SaveWindow(model=self.model, controller=self.controller)

        self.dialog.open()
        self.controller.dialog(mode, self.dialog)

    def next_step(self):
        self.controller.next_step()

    def close_dialog(self, dialog_data: list = []):
        if self.dialog.mode == "input":
            self.controller.add_animal(dialog_data)
        elif self.dialog.mode == "delete":
            self.controller.delete_animal(dialog_data)
        elif self.dialog.mode == "upload":
            self.controller.upload_from_file(dialog_data)
        elif self.dialog.mode == "save":
            self.controller.save_in_file(dialog_data)
        self.dialog = None

    def model_is_changed(self, data):
        """ The method is called when the model changes. """
        self.close_dialog(data)

    def build(self):
        for cell_row in self.model.cells:
            for cell in cell_row:
                self.add_widget(cell)
        for label in self.model.labels:
            self.add_widget(label)
        return self


Builder.load_file(os.path.join(os.path.dirname(__file__), "mainscreen.kv"))
