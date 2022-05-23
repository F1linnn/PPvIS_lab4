import os

from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.dropdown import DropDown
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.button import Button
from kivymd.uix.menu import MDDropdownMenu


class DialogContent(BoxLayout):
    pass


class InputDialogContent(DialogContent):
    pass


class DeleteDialogContent(DialogContent):
    pass


class UploadDialogContent(DialogContent):
    pass


class SaveDialogContent(DialogContent):
    pass


class DialogWindow(MDDialog):
    def __init__(self, **kwargs):
        super().__init__(
            title=kwargs["title"],
            type="custom",
            content_cls=kwargs["content_cls"],
            buttons=[
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    on_release=self.close
                ),
            ],
        )
        self.mode = kwargs["mode"]
        self.controller = kwargs["controller"]
        self.model = kwargs["model"]

    def close(self, obj):
        self.dismiss()


class InputWindow(DialogWindow):
    def __init__(self, **kwargs):
        super().__init__(
            title="New animal: ",
            content_cls=InputDialogContent(),
            mode="input",
            controller=kwargs["controller"],
            model=kwargs["model"]
        )
        drop_down = DropDown()
        btn = Button(text="Plant", size_hint_y=None, height=20)
        btn.bind(on_release=lambda btn: drop_down.select(btn.text))
        btn1 = Button(text="Bison", size_hint_y=None, height=20)
        btn1.bind(on_release=lambda btn1: drop_down.select(btn1.text))
        btn2 = Button(text="Wolf", size_hint_y=None, height=20)
        btn2.bind(on_release=lambda btn2: drop_down.select(btn2.text))
        btn3 = Button(text="Deer", size_hint_y=None, height=20)
        btn3.bind(on_release=lambda btn3: drop_down.select(btn3.text))
        btn4 = Button(text="Rabbit", size_hint_y=None, height=20)
        btn4.bind(on_release=lambda btn4: drop_down.select(btn4.text))

        drop_down.add_widget(btn)
        drop_down.add_widget(btn1)
        drop_down.add_widget(btn2)
        drop_down.add_widget(btn3)
        drop_down.add_widget(btn4)

        main_but = Button(text="Animal types", size_hint=(.2, .2), pos_hint ={'x': 2, 'y': 2})
        main_but.bind(on_release=drop_down.open)
        drop_down.bind(on_select=lambda instance, x: setattr(self.content_cls.ids['input_type'], 'text', x))
        self.add_widget(main_but)

    def close(self, obj):
        self.dismiss()
        self.controller.close_dialog(
            [
                self.content_cls.ids.input_type.text,
                self.content_cls.ids.input_row_index.text,
                self.content_cls.ids.input_column_index.text
            ]
        )




class SaveWindow(DialogWindow):
    def __init__(self, **kwargs):
        super().__init__(
            title="Saving: ",
            content_cls=SaveDialogContent(),
            mode="save",
            controller=kwargs["controller"],
            model=kwargs["model"]
        )

    def close(self, obj):
        self.dismiss()
        self.controller.close_dialog(self.content_cls.ids.save_path.text)


class UploadWindow(DialogWindow):
    def __init__(self, **kwargs):
        super().__init__(
            title="Upload: ",
            content_cls=UploadDialogContent(),
            mode="upload",
            controller=kwargs["controller"],
            model=kwargs["model"]
        )

    def close(self, obj):
        self.dismiss()
        self.controller.close_dialog(self.content_cls.ids.upload_path.text)


Builder.load_file(os.path.join(os.path.dirname(__file__), "dialog_windows.kv"))
