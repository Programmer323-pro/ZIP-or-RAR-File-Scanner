from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
import os
from pyunpack import Archive

class ZipViewer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.file_chooser = FileChooserIconView(filters=["*.zip", "*.rar"])
        self.add_widget(self.file_chooser)

        self.select_button = Button(text="Open Archive", size_hint_y=None, height=50)
        self.select_button.bind(on_release=self.open_archive)
        self.add_widget(self.select_button)

        self.output_label = Label(text="Selected archive content will appear here...", size_hint_y=None, height=30)
        self.add_widget(self.output_label)

        self.content_scroll = ScrollView(size_hint=(1, 1))
        self.content_box = BoxLayout(orientation='vertical', size_hint_y=None)
        self.content_box.bind(minimum_height=self.content_box.setter('height'))
        self.content_scroll.add_widget(self.content_box)
        self.add_widget(self.content_scroll)

        self.extract_button = Button(text="Extract Archive", size_hint_y=None, height=50)
        self.extract_button.bind(on_release=self.extract_archive)
        self.add_widget(self.extract_button)

        self.archive_path = None

    def open_archive(self, instance):
        selection = self.file_chooser.selection
        if not selection:
            return
        self.archive_path = selection[0]
        try:
            temp_dir = "__temp_extract__"
            os.makedirs(temp_dir, exist_ok=True)
            Archive(self.archive_path).extractall(temp_dir)

            self.content_box.clear_widgets()
            for root, _, files in os.walk(temp_dir):
                for f in files:
                    path = os.path.relpath(os.path.join(root, f), temp_dir)
                    self.content_box.add_widget(Label(text=path, size_hint_y=None, height=30))

            self.output_label.text = f"Archive: {os.path.basename(self.archive_path)}"
            import shutil
            shutil.rmtree(temp_dir)
        except Exception as e:
            self.output_label.text = f"Error: {e}"

    def extract_archive(self, instance):
        if not self.archive_path:
            self.output_label.text = "No archive selected."
            return
        try:
            out_path = os.path.join(os.path.expanduser("~"), "ExtractedArchive")
            os.makedirs(out_path, exist_ok=True)
            Archive(self.archive_path).extractall(out_path)
            self.output_label.text = f"Extracted to {out_path}"
        except Exception as e:
            self.output_label.text = f"Extraction failed: {e}"

class ZipApp(App):
    def build(self):
        self.icon = 'icons/app.png'
        return ZipViewer()

if __name__ == "__main__":
    ZipApp().run()
