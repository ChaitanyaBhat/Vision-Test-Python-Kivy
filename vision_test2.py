import speech_recognition as sr  
from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
Builder.load_file("vision_test2.kv")

from kivy.config import Config  
Config.set('graphics', 'resizable', False) 
Config.set('graphics', 'width', '1200')  
Config.set('graphics', 'height', '700') 

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
            info.text = "[color=#d8021c]All fields are mandatory[/color]"
            self.ids.name.text = ""
            self.ids.age.text = ""
            self.ids.place.text = ""
            self.ids.number.text = ""
        else:
            info.text =""
            self.manager.current="select"

class SelectWindow(Screen):
    pass

class VisualAcuityWindow(Screen):
    pass

class AstigmatismWindow(Screen):
    pass

class GlassCheckerWindow(Screen):
    pass

class SnellenChartWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def empty_text(self):
        self.ids.audio_test.text = ""                                                                                

    def recording(self):
        self.ids.audio_test.text = "[color=#d8021c]Recording...[/color]"                                                                                

    def validate_speech(self):
        # get audio from the microphone                                                                       
        recognize = sr.Recognizer()                                                                                   
        with sr.Microphone() as source:
            print("Speak:")   
            audio = recognize.listen(source)   
        
        print("Processing...")
        word1 = 's r z k d'; word2 = "c k d n r"; word3 = "z s o k n"; word4 ="d k s n v"
        word5 = 'o n h r c'; word6 = "c z r h s"; word7 = "d o v h r"; word8 ="r h s d"

        try:
            print("You said: " + recognize.recognize_google(audio))
            if recognize.recognize_google(audio) == word1:
                print("Line 1: Matching")
                self.ids.audio_test.text = "[color=#d8021c]Line 1: Matching[/color]"                                                                                
            elif recognize.recognize_google(audio) == word2:
                print("Line 2: Matching")
                self.ids.audio_test.text = "[color=#d8021c]Line 2: Matching[/color]"                                                                                
            elif recognize.recognize_google(audio) == word3:
                print("Line 3: Matching")
                self.ids.audio_test.text = "[color=#d8021c]Line 3: Matching[/color]"                                                                                
            elif recognize.recognize_google(audio) == word4:
                print("Line 4: Matching")
                self.ids.audio_test.text = "[color=#d8021c]Line 4: Matching[/color]"                                                                                
            elif recognize.recognize_google(audio) == word5:
                print("Line 5: Matching")
                self.ids.audio_test.text = "[color=#d8021c]Line 5: Matching[/color]"                                                                                
            elif recognize.recognize_google(audio) == word6:
                print("Line 6: Matching")
                self.ids.audio_test.text = "[color=#d8021c]Line 6: Matching[/color]"                                                                                
            elif recognize.recognize_google(audio) == word7:
                print("Line 7: Matching")
                self.ids.audio_test.text = "[color=#d8021c]Line 7: Matching[/color]"  
            elif recognize.recognize_google(audio) == word8:
                print("Line 8: Matching")
                self.ids.audio_test.text = "[color=#d8021c]Line 8: Matching[/color]"                                                                                                                                                    
            else: 
                print("Not matching")
                self.ids.audio_test.text = "[color=#d8021c]Not matching[/color]"                                                                                
        except sr.UnknownValueError:
            print("Could not understand audio\nTry again")
            self.ids.audio_test.text = "[color=#d8021c]Could not understand audio\nTry again[/color]"                                                                                
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            self.ids.audio_test.text = "[color=#d8021c]Could not request results[/color]" 

class LandoltCWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def empty_text(self):
        self.ids.audio_test.text = ""

    def recording(self):
        self.ids.audio_test.text = "[color=#d8021c]Recording...[/color]"
        
    def validate_speech(self):
        # get audio from the microphone                                                                       
        recognize = sr.Recognizer()                                                                                   
        with sr.Microphone() as source:
            print("Speak:")   
            audio = recognize.listen(source)   
        
        print("Processing...")
        word1 = '45 degree right down up right'; word2 = "up left 45 degree left up" 
        word3 = "right 45 degree right down 45 degree left down"; word4 ="45 degree right up left down"
        word5 = 'up right 45 degree left down'; word6 = "right 45 degree right up 45 degree left down"
        word7 = "down 45 degree left down 45 degree right down"; word8 ="45 degree right down 45 degree left up up"

        try:
            print("You said: " + recognize.recognize_google(audio))
            if recognize.recognize_google(audio) == word1:
                print("Line 1: Matching")
                self.ids.audio_test.text = "[color=#d8021c]Line 1: Matching[/color]"                                                                                
            elif recognize.recognize_google(audio) == word2:
                print("Line 2: Matching")
                self.ids.audio_test.text = "[color=#d8021c]Line 2: Matching[/color]"                                                                                
            elif recognize.recognize_google(audio) == word3:
                print("Line 3: Matching")
                self.ids.audio_test.text = "[color=#d8021c]Line 3: Matching[/color]"                                                                                
            elif recognize.recognize_google(audio) == word4:
                print("Line 4: Matching")
                self.ids.audio_test.text = "[color=#d8021c]Line 4: Matching[/color]"                                                                                
            elif recognize.recognize_google(audio) == word5:
                print("Line 5: Matching")
                self.ids.audio_test.text = "[color=#d8021c]Line 5: Matching[/color]"                                                                                
            elif recognize.recognize_google(audio) == word6:
                print("Line 6: Matching")
                self.ids.audio_test.text = "[color=#d8021c]Line 6: Matching[/color]"                                                                                
            elif recognize.recognize_google(audio) == word7:
                print("Line 7: Matching")
                self.ids.audio_test.text = "[color=#d8021c]Line 7: Matching[/color]"                                                                                
            elif recognize.recognize_google(audio) == word8:
                print("Line 8: Matching")
                self.ids.audio_test.text = "[color=#d8021c]Line 8: Matching[/color]"                                                                                
            else: 
                print("Not matching")
                self.ids.audio_test.text = "[color=#d8021c]Not matching[/color]"                                                                                
        except sr.UnknownValueError:
            print("Could not understand audio\nTry again")
            self.ids.audio_test.text = "[color=#d8021c]Could not understand audio\nTry again[/color]"                                                                                
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            self.ids.audio_test.text = "[color=#d8021c]Could not request results[/color]"  

class RandomEWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def empty_text(self):
        self.ids.audio_test.text = ""

    def recording(self):
        self.ids.audio_test.text = "[color=#d8021c]Recording...[/color]"
        
    def validate_speech(self):
        # get audio from the microphone                                                                       
        recognize = sr.Recognizer()                                                                                   
        with sr.Microphone() as source:
            print("Speak:")   
            audio = recognize.listen(source)   
        
        print("Processing...")
        word1 = 'up right up right left'; word2 = "down up left right down"; word3 = "right left up left up" 
        word4 ="up down up left up"; word5 = 'down right down left right'; word6 = "right down left right left"
        word7 = "right left right up down"

        try:
            print("You said: " + recognize.recognize_google(audio))
            if recognize.recognize_google(audio) == word1:
                print("Line 1: Matching")
                self.ids.audio_test.text = "[color=#d8021c]Line 1: Matching[/color]"                                                                                
            elif recognize.recognize_google(audio) == word2:
                print("Line 2: Matching")
                self.ids.audio_test.text = "[color=#d8021c]Line 2: Matching[/color]"                                                                                
            elif recognize.recognize_google(audio) == word3:
                print("Line 3: Matching")
                self.ids.audio_test.text = "[color=#d8021c]Line 3: Matching[/color]"                                                                                
            elif recognize.recognize_google(audio) == word4:
                print("Line 4: Matching")
                self.ids.audio_test.text = "[color=#d8021c]Line 4: Matching[/color]"                                                                                
            elif recognize.recognize_google(audio) == word5:
                print("Line 5: Matching")
                self.ids.audio_test.text = "[color=#d8021c]Line 5: Matching[/color]"                                                                                
            elif recognize.recognize_google(audio) == word6:
                print("Line 6: Matching")
                self.ids.audio_test.text = "[color=#d8021c]Line 6: Matching[/color]"                                                                                
            elif recognize.recognize_google(audio) == word7:
                print("Line 7: Matching")
                self.ids.audio_test.text = "[color=#d8021c]Line 7: Matching[/color]"                                                                                                                                                               
            else: 
                print("Not matching")
                self.ids.audio_test.text = "[color=#d8021c]Not matching[/color]"                                                                                
        except sr.UnknownValueError:
            print("Could not understand audio\nTry again")
            self.ids.audio_test.text = "[color=#d8021c]Could not understand audio\nTry again[/color]"                                                                                
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            self.ids.audio_test.text = "[color=#d8021c]Could not request results[/color]"  

sm=ScreenManager()
sm.add_widget(StartWindow(name = "start"))
sm.add_widget(InfoWindow(name = "info"))
sm.add_widget(SelectWindow(name = "select"))
sm.add_widget(VisualAcuityWindow(name = "acuity"))
sm.add_widget(AstigmatismWindow(name = "astigma"))
sm.add_widget(GlassCheckerWindow(name = "glass"))
sm.add_widget(SnellenChartWindow(name = "snellen"))
sm.add_widget(LandoltCWindow(name = "landolt_c"))
sm.add_widget(RandomEWindow(name = "random_e"))

class VisionApp(App):
    def build(self):
        self.title="e-VISION CLINIC"
        return sm

if __name__=="__main__":
    VisionApp().run()

