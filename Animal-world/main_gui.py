# main file for GUI version

from kivymd.app import MDApp
from Model.Model_screen import ScreenModel
from Controller.Control_screen import ScreenController
from View.mainscreen import ScreenView
from kivy.core.window import Window
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatButton
from Model.Area import NUMBER_OF_COLUMNS, NUMBER_OF_ROWS


class Pass_MVC(MDApp):
    def __init__(self):
        super().__init__()
        self.model = ScreenModel()
        self.controller = ScreenController(self.model)
        self.view = ScreenView(model=self.model, controller=self.controller)

    def build(self):
        Window.size = (1000, 800)
        self.title = "Animal world"
        return self.view.build()


Pass_MVC().run()
