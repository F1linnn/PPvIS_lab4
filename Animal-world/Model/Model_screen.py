from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import Snackbar
from Model.Area import Area, create_area_from_database, NUMBER_OF_ROWS, NUMBER_OF_COLUMNS


class ScreenModel:

    _not_filtered = []

    def __init__(self):

        self.dialog = None
        self.area = None
        self._observers = []
        cells = []
        for row_index in range(NUMBER_OF_ROWS):
            cell_row = []
            for column_index in range(NUMBER_OF_COLUMNS):
                cell_row.append(MDRectangleFlatButton(
                    text="   -   \n   -   \n   -   \n   -   ",
                    pos_hint={'center_x': .31 + .125 * column_index, 'center_y': .86 - .155 * row_index},
                    size_hint=(0.125, 0.155),
                    font_size=20,
                    md_bg_color=(0, 1, 1, 0)
                ))
            cells.append(cell_row)
        labels = [MDRectangleFlatButton(
            text="",
            pos_hint={"center_x": .5, "center_y": .2},
            size_hint=(.975, .125),
            font_size=14
        ), MDLabel(
            text="Animal world",
            pos_hint={"center_x": .59, "center_y": 0.975},
            size_hint=(.25, .25),
            font_size=25,
            font_name="Fonts/Action_Man_Shaded_Italic.ttf"
        ), MDLabel(
            text="Moving LOG",
            pos_hint={"center_x": .59, "center_y": .3},
            size_hint=(.25, .25),
            font_size=20
        )]
        self.cells = cells
        self.labels = labels

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, data):
        for x in self._observers:
            x.model_is_changed(data)

    def read_from_file(self, file_name: str) -> None:
        area_ = create_area_from_database(file_name=file_name)
        self.area = area_ if area_ is not None else self.area
        self.area._Area__inhabitant_log = ""
        self.update_area()

    @staticmethod
    def create_empty_file(path):
        try:
            with open(path, 'w'):
                pass
            return True
        except Exception as e:
            return False

    def write_to_file(self, path: str):
        path = "XML/" + path
        self.area.save_in_file(path)
        Snackbar(text="Area was saved").open()

    def add_new_animal(self, data):
        animal_type, row_index, column_index = data
        if animal_type not in ['Bison', 'Deer', 'Rabbit', 'Lion', 'Wolf']:
            Snackbar(text="Invalid animal type").open()
            return
        row_index = int(row_index)
        column_index = int(column_index)
        if row_index < 0 or row_index >= NUMBER_OF_ROWS or column_index < 0 or column_index >= NUMBER_OF_COLUMNS:
            Snackbar(text="Invalid line or column number").open()
            return
        if not self.area.create_animal_gui(animal_type, row_index, column_index):
            Snackbar(text="No place for inhabitant").open()
        self.update_area()

    def update_area(self):
        matrix = self.area.transform_area_into_matrix_form()
        for raw_index in range(NUMBER_OF_ROWS):
            for column_index in range(NUMBER_OF_COLUMNS):
                self.cells[raw_index][column_index].text = ""
                for animal_place in range(4):
                    self.cells[raw_index][column_index].text += matrix[raw_index][column_index][animal_place] + "\n"

    def delete_animal(self, id):
        found_animal = self.area.delete_animal_by_id(id)
        if found_animal:
            self.update_area()
        return found_animal

    def next_step(self):
        inh_log = self.area.next_step(gui=True)
        self.update_area()
        str_max_length = 230
        for i in range(len(inh_log) // str_max_length):
            inh_log = inh_log[:(i + 1) * str_max_length] + '\n' + inh_log[(i + 1) * str_max_length:]
        self.labels[0].text = inh_log
