from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
Builder.load_file("vision_test0.kv")

# Builder.load_string("""
# """)

class StartWindow(Screen):
    pass

class InfoWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate(self):
        name=self.ids.name.text 
        age=self.ids.age.text
        place = self.ids.place.text
        num = self.ids.number.text
        info=self.ids.information

        if name=="" or age=="" or place == "" or num == "" :
            info.text = "[color=ff1001]All fields are mandatory[/color]"
            self.ids.name.text = ""
            self.ids.age.text = ""
            self.ids.place.text = ""
            self.ids.number.text = ""
        else:
            info.text =""
            self.manager.transition.direction= "left"
            self.manager.current="select"

class SelectWindow(Screen):
    pass


sm=ScreenManager()
sm.add_widget(StartWindow(name = "start"))
sm.add_widget(InfoWindow(name = "info"))
sm.add_widget(SelectWindow(name = "select"))


class VisionApp(App):
    def build(self):
        self.title="e-VISION CLINIC"
        return sm

if __name__=="__main__":
    VisionApp().run()


