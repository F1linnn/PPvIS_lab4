from kivymd.uix.snackbar import Snackbar
from Model.Area import create_area_from_database
from Model.Model_screen import ScreenModel


class ScreenController:
    _observers = []

    def __init__(self, model: ScreenModel):
        self.model = model
        self.model.area = create_area_from_database("start.xml")
        self.model.update_area()
        self._observers = []
        self._dialog = None

    def add_animal(self, data):
        self.model.add_new_animal(data=data)

    def dialog(self, mode, dialog):
        self.open_dialog(mode, dialog)

    def next_step(self):
        self.model.next_step()

    def delete_animal(self, data):
        delete = self.model.delete_animal(id=int(data[0]))
        if delete:
            Snackbar(text=f"Inhabitant with id = {data} was deleted!").open()
        else:
            Snackbar(text=f"Inhabitant with id = {data} not found!").open()

    def upload_from_file(self, file_name):
        self.model.read_from_file(file_name)

    def save_in_file(self, file_name):
        self.model.write_to_file(file_name)

    def open_dialog(self, dialog, mode):
        self._dialog = dialog

    def close_dialog(self, dialog_data: list = []):
        data = dialog_data
        self.model.notify_observers(data)
        self._dialog = None
