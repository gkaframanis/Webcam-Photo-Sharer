from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard

import time
import webbrowser

from filesharer import FileSharer

Builder.load_file("frontend.kv")


class CameraScreen(Screen):
    """Class to manage the webcam."""

    def start(self):
        """Starts the camera and changes the Button text"""
        self.ids.camera.opacity = 1
        self.ids.camera.play = True
        self.ids.camera_btn.text = "Stop Camera"
        self.ids.camera.texture = self.ids.camera._camera.texture

    def stop(self):
        """Stops the camera and changes the Button text"""
        self.ids.camera.opacity = 0
        self.ids.camera.play = False
        self.ids.camera_btn.text = "Start Camera"
        # Remove the last frame
        self.ids.camera.texture = None

    def capture(self):
        """Creates a filename with the current time and captures and saves a photo image under that filename"""
        current_time = time.strftime("%Y%m%d-%H%M%S")
        self.filepath = f"files/{current_time}.png"
        # self.ids gives us access to the widgets of the class where the code is written - The widgets of CameraScreen
        self.ids.camera.export_to_png(self.filepath)
        # To go to the ImageScreen
        self.manager.current = "image_screen"
        # self.manager.current_screen.ids will gives us access to the widgets of the current screen the user is using. -
        # The widgets of the ImageScreen
        self.manager.current_screen.ids.captured_img.source = self.filepath


class ImageScreen(Screen):

    link_message = "Create a Link First"

    def create_link(self):
        """Accesses the saved photo's filepath, uploads it to the web
        and inserts the link in the Label widget of the ImageScreen.
        """
        # We take the current instance of the CameraScreen class.
        file_path = App.get_running_app().root.ids.camera_screen.filepath
        filesharer = FileSharer(filepath=file_path)
        self.url = filesharer.share()
        self.ids.link.text = self.url

    def copy_link(self):
        """Copy link to the clipboard available for pasting."""
        try:
            Clipboard.copy(self.url)
        except AttributeError:
            self.ids.link.text = self.link_message

    def open_link(self):
        """Open link with default browser."""
        try:
            webbrowser.open(self.url)
        except AttributeError:
            self.ids.link.text = self.link_message


class RootWidget(ScreenManager):
    pass


class MainApp(App):

    def build(self):
        return RootWidget()


MainApp().run()
