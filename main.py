from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.snackbar import Snackbar
import re
import pyperclip
import hero_dictionary
from kivymd.uix.dialog import MDDialog


class FirstWindow(Screen):

    Builder.load_file('firstwindow.kv')

    def replace_text(self):

        try:
            if self.ids.paragraph.text:
                # Define the dictionary of patterns and their replacement strings
                hero_dict = hero_dictionary.hero_dict
                # Define the regular expression pattern with the MULTILINE flag
                pattern = re.compile("|".join(map(re.escape, hero_dict.keys())), re.MULTILINE)
                # Replace all patterns in the input string with their corresponding replacement strings
                output_string = pattern.sub(lambda match: hero_dict[match.group(0)], self.ids.paragraph.text)
                # Set the output string to the MDTextField widget
                self.manager.first.result.text = output_string
                self.show_replaced_snackbar()
            else:
                self.error_dialog("Kindly insert a text to proceed.")
        except ValueError:
            pass

    def reset(self):
        self.ids.paragraph.text = ""
        self.ids.result.text = ""

    def copy(self):
        if self.ids.result.text != '':
            pyperclip.copy(self.ids.result.text)
            self.show_copied_snackbar()
        else:
            self.error_dialog("There is no text to be copied.")

    def show_replaced_snackbar(self):
        snackbar = Snackbar(
            text="The text has been replaced."
        )
        snackbar.open()

    def show_copied_snackbar(self):
        snackbar = Snackbar(
            text="Text was copied!",
            snackbar_x='5'
            )
        snackbar.open()

    def error_dialog(self, message):

            close_button = MDFlatButton(
                text='CLOSE',
                text_color=[0, 0, 0, 1],
                on_release=self.close_dialog,
            )
            self.dialog = MDDialog(
                title='[color=#FF0000]Ooops![/color]',
                text=message,
                buttons=[close_button],
            )
            self.dialog.open()

    # Close Dialog
    def close_dialog(self, obj):
        self.dialog.dismiss()


class WindowManager(ScreenManager):
    pass


class formatterApp(MDApp):

    def build(self):

        return WindowManager()

if __name__ == '__main__':
    formatterApp().run()
