import speech_recognition as sr
from fuzzywuzzy import fuzz

from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_file("vision_test.kv")
Builder.load_file("visual_acuity.kv")
Builder.load_file("astigmatism.kv")
Builder.load_file("glass_checker.kv")
Builder.load_file("vision_report.kv")

from kivy.config import Config 
# resizing the screen: 
Config.set('graphics', 'resizable', False) 
Config.set('graphics', 'width', '1200')  
Config.set('graphics', 'height', '700') 

class StartWindow(Screen):
    pass

class InfoWindow(Screen):
    user_info = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate(self):
        # getting the entered user information from screen:
        f_name=self.ids.f_name.text 
        l_name=self.ids.l_name.text 
        age=self.ids.age.text
        place = self.ids.place.text
        num = self.ids.number.text
        info=self.ids.information

        # validating the user information:
        if f_name=="" or l_name == "" or age=="" or place == "" or num == "" :
            info.text = "[color=#8B0000][b]All fields are mandatory[/b][/color]"
            self.ids.f_name.text = ""
            self.ids.l_name.text = ""
            self.ids.age.text = ""
            self.ids.place.text = ""
            self.ids.number.text = ""
        elif any(character.isnumeric() for character in f_name) or any(not character.isalnum() for character in f_name):
            info.text = "[color=#8B0000][b]Invalid First Name[/b][/color]"
            self.ids.f_name.text = ""
        elif any(character.isnumeric() for character in l_name) or any(not character.isalnum() for character in l_name):
            info.text = "[color=#8B0000][b]Invalid Last Name[/b][/color]"
            self.ids.l_name.text = ""
        elif (len(age) > 2):
            info.text = "[color=#8B0000][b]Invalid Age[/b][/color]"
            self.ids.age.text = ""
        elif any(character.isnumeric() for character in place) or any(not character.isalnum() for character in place) : 
            info.text = "[color=#8B0000][b]Invalid Place[/b][/color]"
            self.ids.place.text = ""
        elif (len(num) < 10) or (len(num) > 11):
            info.text = "[color=#8B0000][b]Invalid Contact Number[/b][/color]"
            self.ids.number.text = ""
        else:
            info.text =""
            self.manager.current="select"

        # sending the user information to report screen:
        self.user_info = {'First Name': f_name, 'Last Name': l_name, 'Age': age, 'Place': place, 'Contact Number': num} 
        self.manager.get_screen("acuity_report").user_info = dict(self.user_info)
        self.manager.get_screen("astigma_report").user_info = dict(self.user_info)
        self.manager.get_screen("glass_report").user_info = dict(self.user_info)


class SelectWindow(Screen):
    pass

class VisualAcuityWindow(Screen):
    pass

class SnellenChartWindow(Screen):
    result1 = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def empty_text(self):
        self.ids.audio_test.text = ""                                                                                

    def recording(self):
        self.ids.audio_test.text = "[color=#8B0000]Recording...[/color]"                                                                                

    def validate_speech(self):
        # get audio from the microphone                                                                       
        recognize = sr.Recognizer()                                                                                   
        with sr.Microphone() as source:
            print("Speak:")   
            audio = recognize.listen(source)   
        
        print("Processing...")
        # self.ids.audio_test.text = "[color=#8B0000]Processig...[/color]"                                                                                

        input_word = recognize.recognize_google(audio)
        input_word = input_word.replace(' ', '')
        input_word = input_word.upper()

        line_num = self.ids.line_num.text

        try:
            if line_num == '1':
                percentage_matching = fuzz.ratio(input_word, 'HTVOV')
                vision = percentage_matching - 60
            elif line_num == '2':
                percentage_matching = fuzz.ratio(input_word, 'OVTHO')
                vision = percentage_matching - 50
            elif line_num == '3':
                percentage_matching = fuzz.ratio(input_word, 'THOVH')
                vision = percentage_matching - 40
            elif line_num == '4':
                percentage_matching = fuzz.ratio(input_word, 'VOVHT')
                vision = percentage_matching - 30
            elif line_num == '5':
                percentage_matching = fuzz.ratio(input_word, 'OTHTV')
                vision = percentage_matching - 20
            elif line_num == '6':
                percentage_matching = fuzz.ratio(input_word, 'HVTOH')
                vision = percentage_matching - 10
            elif line_num == '7':
                percentage_matching = fuzz.ratio(input_word, 'TOHVO')
                vision = percentage_matching
            else:
                percentage_matching = 0
                vision = percentage_matching

            percentage_string = str(vision)
            self.ids.audio_test.text = 'You said: ' + input_word +'\nYou have '+ percentage_string+' % vision'
            
        except sr.UnknownValueError:
            self.ids.audio_test.text = "[color=#d8021c]Try again \nCould not understand audio[/color]"                                                                                
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            self.ids.audio_test.text = "[color=#d8021c]No connection \nCould not request results[/color]"  
             
        text = self.ids.audio_test.text
        text_list = text.split()
        number_list = [int(char) for char in text_list if char.isnumeric()]
        if number_list == []:
            self.result1 = 0
        else:
            self.result1 = vision

    def next_screen(self):
        print(self.result1)
        self.ids.audio_test.text = ''
        self.manager.get_screen("acuity_result").result1 = int(self.result1)
        self.manager.current = 'random_e'

class RandomEWindow(Screen):
    result2 = 0
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
            
    def empty_text(self):
        self.ids.audio_test.text = ""                                                                                

    def recording(self):
        self.ids.audio_test.text = "[color=#8B0000]Recording...[/color]"                                                                                

    def validate_speech(self):
        recognize = sr.Recognizer()                                                                                   
        with sr.Microphone() as source:
            print("Speak:")   
            audio = recognize.listen(source)   
        
        print("Processing...")

        input_word = recognize.recognize_google(audio)
        input_word = input_word.lower()
        
        word1 = "right left right up down"; word2 = "right down left right left"; word3 = 'down right down left right'
        word4 ="up down up left up"; word5 = "right left up left up"; word6 = "down up left right down"
        word7 = 'up right up right left'

        line_num = self.ids.line_num.text

        try:
            if line_num == '1':
                percentage_matching = fuzz.ratio(input_word, word1)
                vision = percentage_matching - 60
            elif line_num == '2':
                percentage_matching = fuzz.ratio(input_word, word2)
                vision = percentage_matching - 50
            elif line_num == '3':
                percentage_matching = fuzz.ratio(input_word, word3)
                vision = percentage_matching - 40
            elif line_num == '4':
                percentage_matching = fuzz.ratio(input_word, word4)
                vision = percentage_matching - 30
            elif line_num == '5':
                percentage_matching = fuzz.ratio(input_word, word5)
                vision = percentage_matching - 20
            elif line_num == '6':
                percentage_matching = fuzz.ratio(input_word, word6)
                vision = percentage_matching - 10
            elif line_num == '7':
                percentage_matching = fuzz.ratio(input_word, word7)
                vision = percentage_matching
            else:
                percentage_matching = 0
                vision = percentage_matching

            percentage_string = str(vision)
            self.ids.audio_test.text = 'You said: ' + input_word +'\nYou have '+ percentage_string+' % vision'
            
        except sr.UnknownValueError:
            self.ids.audio_test.text = "[color=#d8021c]Try again \nCould not understand audio[/color]"                                                                                
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            self.ids.audio_test.text = "[color=#d8021c]No connection \nCould not request results[/color]"  
    
        text = self.ids.audio_test.text
        text_list = text.split()
        number_list = [int(char) for char in text_list if char.isnumeric()]
        if number_list == []:
            self.result2 = 0
        else:
            self.result2 = vision

    def next_screen(self):
        print(self.result2)
        self.ids.audio_test.text =''
        self.manager.get_screen("acuity_result").result2 = int(self.result2)
        self.manager.current = 'landolt_c'


class LandoltCWindow(Screen):
    result3 = 0
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
            
    def empty_text(self):
        self.ids.audio_test.text = ""                                                                                

    def recording(self):
        self.ids.audio_test.text = "[color=#8B0000]Recording...[/color]"                                                                                

    def validate_speech(self):
        recognize = sr.Recognizer()                                                                                   
        with sr.Microphone() as source:
            print("Speak:")   
            audio = recognize.listen(source)   
        
        print("Processing...")

        input_word = recognize.recognize_google(audio)
        input_word = input_word.lower()

        word1 = "left down up"; word2 = "right up left down"; word3 = "up left right down"
        word4 = "up left down right down up"; word5 = "down left up left up right"
        word6 = "right down left left up right"; word7 = "left right down down up left"

        line_num = self.ids.line_num.text

        try:
            if line_num == '1':
                percentage_matching = fuzz.ratio(input_word, word1)
                vision = percentage_matching - 60
            elif line_num == '2':
                percentage_matching = fuzz.ratio(input_word, word2)
                vision = percentage_matching - 50
            elif line_num == '3':
                percentage_matching = fuzz.ratio(input_word, word3)
                vision = percentage_matching - 40
            elif line_num == '4':
                percentage_matching = fuzz.ratio(input_word, word4)
                vision = percentage_matching - 30
            elif line_num == '5':
                percentage_matching = fuzz.ratio(input_word, word5)
                vision = percentage_matching - 20
            elif line_num == '6':
                percentage_matching = fuzz.ratio(input_word, word6)
                vision = percentage_matching - 10
            elif line_num == '7':
                percentage_matching = fuzz.ratio(input_word, word7)
                vision = percentage_matching
            else:
                percentage_matching = 0
                vision = percentage_matching

            percentage_string = str(vision)
            self.ids.audio_test.text = 'You said: ' + input_word +'\nYou have '+ percentage_string+' % vision'
            
        except sr.UnknownValueError:
            self.ids.audio_test.text = "[color=#d8021c]Try again \nCould not understand audio[/color]"                                                                                
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            self.ids.audio_test.text = "[color=#d8021c]No connection \nCould not request results[/color]"  
        
        text = self.ids.audio_test.text
        text_list = text.split()
        number_list = [int(char) for char in text_list if char.isnumeric()]
        if number_list == []:
            self.result3 = 0
        else:
            self.result3 = vision

    def next_screen(self):
        print(self.result3)
        self.ids.audio_test.text = ''
        self.manager.get_screen('acuity_result').result3 = int(self.result3)
        self.manager.current = 'acuity_result'



class AstigmatismWindow(Screen):
    pass

class Astigma1Window(Screen):
    result1 = 0
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def empty_input(self):
        if self.ids.audio_test.text == '':
            self.ids.audio_test.text = 'Proper Input Required. Try Again.'
        else:
            self.manager.current= '2astigma'

    def empty_text(self):
        self.ids.audio_test.text = ""                                                                                

    def recording(self):
        self.ids.audio_test.text = "[color=#8B0000]Recording...[/color]"                                                                                

    def validate_speech(self):
        recognize = sr.Recognizer()                                                                                   
        with sr.Microphone() as source:
            print("Speak:")   
            audio = recognize.listen(source)   
        
        print("Processing...")

        input_word = recognize.recognize_google(audio)
        input_word = input_word.lower()

        word1 = 'yes'; word2 = "no"

        try:
            if input_word == word1:
                self.ids.audio_test.text = "yes"                                                                               
            elif input_word == word2:
                self.ids.audio_test.text = "no"                                                                                                                                                                                                                                 
            else: 
                self.ids.audio_test.text = "[color=#d8021c]Not recorded properly\nTry again.[/color]"                                                                                
        except sr.UnknownValueError:
            self.ids.audio_test.text = "[color=#d8021c]Could not understand audio\nTry again[/color]"                                                                                
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            self.ids.audio_test.text = "[color=#d8021c]Could not request results\nPlease check your connection.[/color]" 

        
        audio_string = self.ids.audio_test.text
        if audio_string == 'yes':
            self.result1 = 1
        elif audio_string == 'no':
            self.result1 = 2
        else:
            self.result1 = 0

        self.manager.get_screen('astigma_result').result1 = int(self.result1)


class Astigma2Window(Screen):
    result2 = 0
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def empty_input(self):
        if self.ids.audio_test.text == '':
            self.ids.audio_test.text = 'Proper Input Required. Try Again.'
        else:
            self.manager.current= '3astigma'

    def empty_text(self):
        self.ids.audio_test.text = ""                                                                                

    def recording(self):
        self.ids.audio_test.text = "[color=#8B0000]Recording...[/color]"                                                                                

    def validate_speech(self):
        recognize = sr.Recognizer()                                                                                   
        with sr.Microphone() as source:
            print("Speak:")   
            audio = recognize.listen(source)   
        
        print("Processing...")

        input_word = recognize.recognize_google(audio)
        input_word = input_word.lower()
        
        word1 = 'yes'; word2 = "no"

        try:
            if input_word == word1:
                self.ids.audio_test.text = "yes"                                                                               
            elif input_word == word2:
                self.ids.audio_test.text = "no"                                                                                                                                                                                                                                 
            else: 
                self.ids.audio_test.text = "[color=#d8021c]Not recorded properly\nTry again.[/color]"                                                                                
        except sr.UnknownValueError:
            self.ids.audio_test.text = "[color=#d8021c]Could not understand audio\nTry again[/color]"                                                                                
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            self.ids.audio_test.text = "[color=#d8021c]Could not request results\nPlease check your connection.[/color]" 

        audio_string = self.ids.audio_test.text
        if audio_string == 'yes':
            self.result2 = 1
        elif audio_string == 'no':
            self.result2 = 2
        else:
            self.result2 = 0

        self.manager.get_screen('astigma_result').result2 = int(self.result2)


class Astigma3Window(Screen):
    result3 = 0
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
            
    def empty_input(self):
        if self.ids.audio_test.text == '':
            self.ids.audio_test.text = 'Proper Input Required. Try Again.'
        else:
            self.manager.current= 'astigma_result'

    def empty_text(self):
        self.ids.audio_test.text = ""                                                                                

    def recording(self):
        self.ids.audio_test.text = "[color=#8B0000]Recording...[/color]"                                                                                

    def validate_speech(self):
        recognize = sr.Recognizer()                                                                                   
        with sr.Microphone() as source:
            print("Speak:")   
            audio = recognize.listen(source)   
        
        print("Processing...")

        input_word = recognize.recognize_google(audio)
        input_word = input_word.lower()
        
        word1 = 'yes'; word2 = "no"

        try:
            if input_word == word1:
                self.ids.audio_test.text = "yes"                                                                               
            elif input_word == word2:
                self.ids.audio_test.text = "no"                                                                                                                                                                                                                                 
            else: 
                self.ids.audio_test.text = "[color=#d8021c]Not recorded properly\nTry again.[/color]"                                                                                
        except sr.UnknownValueError:
            self.ids.audio_test.text = "[color=#d8021c]Could not understand audio\nTry again[/color]"                                                                                
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            self.ids.audio_test.text = "[color=#d8021c]Could not request results\nPlease check your connection.[/color]" 
   
        audio_string = self.ids.audio_test.text
        if audio_string == 'yes':
            self.result3 = 1
        elif audio_string == 'no':
            self.result3 = 2
        else:
            self.result3 = 0

        self.manager.get_screen('astigma_result').result3 = int(self.result3)


class GlassCheckerWindow(Screen):
    pass

class ImagesWindow(Screen):
    result1 = 0
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def empty_text(self):
        self.ids.audio_test.text = ""                                                                                

    def recording(self):
        self.ids.audio_test.text = "[color=#8B0000]Recording...[/color]"                                                                                

    def validate_speech(self):
        recognize = sr.Recognizer()                                                                                   
        with sr.Microphone() as source:
            print("Speak:")   
            audio = recognize.listen(source)   
        
        print("Processing...")

        input_word = recognize.recognize_google(audio)
        input_word = input_word.lower()
        
        images = "apple rocket pen bird tree"

        try:
            percentage_matching = fuzz.ratio(input_word, images)
            percentage_string = str(percentage_matching)
            self.ids.audio_test.text = 'You said: ' + input_word +'\nYou have '+ percentage_string+' % vision'
            
        except sr.UnknownValueError:
            self.ids.audio_test.text = "[color=#d8021c]Try again \nCould not understand audio[/color]"                                                                                
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            self.ids.audio_test.text = "[color=#d8021c]No connection \nCould not request results[/color]"  
    
        text = self.ids.audio_test.text
        text_list = text.split()
        number_list = [int(char) for char in text_list if char.isnumeric()]
        if number_list == []:
            self.result1 = 0
        else:
            self.result1 = percentage_matching

    def next_screen(self):
        print(self.result1)
        self.ids.audio_test.text =''
        self.manager.get_screen('glass_result').result1 = int(self.result1)
        self.manager.current = 'gc_letters'


class AlphabetsWindow(Screen):
    result2 = 0
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
                
    def empty_text(self):
        self.ids.audio_test.text = ""                                                                                

    def recording(self):
        self.ids.audio_test.text = "[color=#8B0000]Recording...[/color]"                                                                                

    def validate_speech(self):
        recognize = sr.Recognizer()                                                                                   
        with sr.Microphone() as source:
            print("Speak:")   
            audio = recognize.listen(source)   
        
        print("Processing...")

        input_word = recognize.recognize_google(audio)
        input_word = input_word.replace(' ', '')
        input_word = input_word.upper()

        letters = "GAKUP"

        try:
            percentage_matching = fuzz.ratio(input_word, letters)
            percentage_string = str(percentage_matching)
            self.ids.audio_test.text = 'You said: ' + input_word +'\nYou have '+ percentage_string+' % vision'
            
        except sr.UnknownValueError:
            self.ids.audio_test.text = "[color=#d8021c]Try again \nCould not understand audio[/color]"                                                                                
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            self.ids.audio_test.text = "[color=#d8021c]No connection \nCould not request results[/color]"  
   
        text = self.ids.audio_test.text
        text_list = text.split()
        number_list = [int(char) for char in text_list if char.isnumeric()]
        if number_list == []:
            self.result2 = 0
        else:
            self.result2 = percentage_matching

    def next_screen(self):
        print(self.result2)
        self.ids.audio_test.text = ''
        self.manager.get_screen('glass_result').result2 = int(self.result2)
        self.manager.current = 'gc_numbers'

    
class NumbersWindow(Screen):
    result3 = 0
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
            
    def empty_text(self):
        self.ids.audio_test.text = ""                                                                                

    def recording(self):
        self.ids.audio_test.text = "[color=#8B0000]Recording...[/color]"                                                                                

    def validate_speech(self):
        recognize = sr.Recognizer()                                                                                   
        with sr.Microphone() as source:
            print("Speak:")   
            audio = recognize.listen(source)   
        
        print("Processing...")

        input_word = recognize.recognize_google(audio)
        input_word = input_word.replace(' ', '')

        numbers = "93758"

        try:
            percentage_matching = fuzz.ratio(input_word,numbers)
            percentage_string = str(percentage_matching)
            self.ids.audio_test.text = 'You said: ' + input_word +'\nYou have '+ percentage_string+' % vision'
            
        except sr.UnknownValueError:
            self.ids.audio_test.text = "[color=#d8021c]Try again \nCould not understand audio[/color]"                                                                                
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            self.ids.audio_test.text = "[color=#d8021c]No connection \nCould not request results[/color]"  
        
        text = self.ids.audio_test.text
        text_list = text.split()
        number_list = [int(char) for char in text_list if char.isnumeric()]
        if number_list == []:
            self.result3 = 0
        else:
            self.result3 = percentage_matching

    def next_screen(self):
        print(self.result3)
        self.ids.audio_test.text = ''
        self.manager.get_screen('glass_result').result3 = int(self.result3)
        self.manager.current = 'glass_result'


class AcuityResultWindow(Screen):
    test_result1 = ''
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def empty_input(self):
        if self.ids.vision_result.text == '':
            self.ids.vision_result.text = 'Proper Input Required. Try Again.'
        else:
            self.manager.current= 'acuity_report'
    
    def final_result(self):
        snellen_result = self.result1
        random_result = self.result2
        landolt_result = self.result3
        
        if snellen_result == 0 and random_result != 0 and landolt_result != 0:
            average_result = (random_result + landolt_result)//2
        elif random_result == 0 and snellen_result != 0 and landolt_result != 0:
            average_result = (snellen_result + landolt_result)//2
        elif landolt_result == 0 and snellen_result != 0 and random_result != 0:
            average_result = (snellen_result + random_result)//2
        elif snellen_result == 0 and random_result == 0  and landolt_result != 0:
            average_result = landolt_result
        elif random_result == 0 and landolt_result == 0 and snellen_result != 0:
            average_result = snellen_result
        elif landolt_result == 0 and snellen_result ==0 and random_result != 0:
            average_result = random_result
        else:
            average_result = (snellen_result + random_result + landolt_result)//3

        if average_result >= 90:
            self.ids.vision_result.text = 'Normal vision'
        elif average_result >= 70:
            self.ids.vision_result.text = 'Near Normal Vision'
        elif average_result >= 50:
            self.ids.vision_result.text = 'Moderate Low Vision'
        elif average_result >= 30:
            self.ids.vision_result.text = 'Severe Low Vision'   
        elif average_result >= 10:
            self.ids.vision_result.text = 'Near Blindness'
        else:
            self.ids.vision_result.text = 'Try again \n You missed something'

        self.test_result1 = self.ids.vision_result.text
        self.manager.get_screen("acuity_report").test_result1 = str(self.test_result1)


class AstigmaResultWindow(Screen):
    test_result2 = ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def empty_input(self):
        if self.ids.vision_result.text == '':
            self.ids.vision_result.text = 'Proper Input Required. Try Again.'
        else:
            self.manager.current= 'astigma_report'
    
    def final_result(self):
        astigma1_result = self.result1
        astigma2_result = self.result2
        astigma3_result = self.result3

        average_result = (astigma1_result + astigma2_result + astigma3_result)/3

        if average_result == 1.0 :
            self.ids.vision_result.text = 'Normal vision'
        elif average_result == 1.3333333333333333 :
            self.ids.vision_result.text = '40% Astigmatism'
        elif average_result == 1.6666666666666667 :
            self.ids.vision_result.text = '70% Astigmatism'
        elif average_result == 2.0:
            self.ids.vision_result.text = '100% Astigmatism'
        else:
            self.ids.vision_result.text = 'Try again \n You missed something'

        self.test_result2 = self.ids.vision_result.text
        self.manager.get_screen("astigma_report").test_result2 = str(self.test_result2)


class GlassCheckerResultWindow(Screen):
    test_result3 = ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def empty_input(self):
        if self.ids.vision_result.text == '':
            self.ids.vision_result.text = 'Proper Input Required. Try Again.'
        else:
            self.manager.current= 'glass_report'
    
    def final_result(self):
        images_result = self.result1
        letters_result = self.result2
        numbers_result = self.result3

        if images_result == 0 and letters_result != 0 and numbers_result != 0:
            average_result = (letters_result + numbers_result)//2
        elif letters_result == 0 and images_result != 0 and numbers_result != 0:
            average_result = (images_result + numbers_result)//2
        elif numbers_result == 0 and images_result != 0 and letters_result != 0:
            average_result = (images_result + letters_result)//2
        elif images_result == 0 and letters_result == 0 and numbers_result != 0:
            average_result = numbers_result
        elif letters_result == 0 and numbers_result == 0 and images_result != 0:
            average_result = images_result
        elif numbers_result == 0 and images_result ==0 and letters_result != 0:
            average_result = letters_result
        else:
            average_result = (images_result + letters_result + numbers_result)//3

        if average_result >= 90:
            self.ids.vision_result.text = 'Normal vision'
        elif average_result >= 70:
            self.ids.vision_result.text = 'Near Normal Vision'
        elif average_result >= 50:
            self.ids.vision_result.text = 'Moderate Low Vision'
        elif average_result >= 30:
            self.ids.vision_result.text = 'Severe Low Vision'   
        elif average_result >= 10:
            self.ids.vision_result.text = 'Near Blindness'
        else:
            self.ids.vision_result.text = 'Try again \n You missed something'

        self.test_result3 = self.ids.vision_result.text
        self.manager.get_screen("glass_report").test_result3 = str(self.test_result3)

class AcuityReportWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def final_report(self):
        patient_info = self.user_info

        result = self.test_result1

        if result == 'Normal vision':
            suggestion = 'Your eyes are perfectly all right'
        elif result == 'Near Normal Vision':
            suggestion = 'Your eyes need occasional rest'
        elif result == 'Moderate Low Vision':
            suggestion = 'You need to wear glasses'
        elif result == 'Severe Low Vision':
            suggestion = 'Consult an eye specialist'
        elif result == 'Near Blindness':
            suggestion = 'Immediately consult an eye specialist'
        else:
            suggestion = 'Follow the instructions properly'

        self.ids.r_name.text = patient_info['First Name'] + ' ' + patient_info['Last Name']
        self.ids.r_age.text = patient_info['Age']
        self.ids.r_place.text = patient_info['Place']
        self.ids.r_number.text = patient_info['Contact Number']
        self.ids.r_test.text = 'Visual Acuity Test'
        self.ids.r_result.text = result
        self.ids.r_suggestion.text = suggestion

class AstigmaReportWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def final_report(self):
        patient_info = self.user_info

        result = self.test_result2

        if result == 'Normal vision':
            suggestion = 'Your eyes are perfectly all right'
        elif result == '40% Astigmatism':
            suggestion = 'You need to have further examinations'
        elif result == '70% Astigmatism':
            suggestion = 'Consult an eye specialist'
        elif result == '100% Astigmatism': 
            suggestion = 'Immediately consult an eye specialist'
        else:
            suggestion = 'Follow the instructions properly'
        

        self.ids.r_name.text = patient_info['First Name'] + ' ' + patient_info['Last Name']
        self.ids.r_age.text = patient_info['Age']
        self.ids.r_place.text = patient_info['Place']
        self.ids.r_number.text = patient_info['Contact Number']
        self.ids.r_test.text = 'Astigmatism Test'
        self.ids.r_result.text = result
        self.ids.r_suggestion.text = suggestion

class GlassReportWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def final_report(self):
        patient_info = self.user_info

        result = self.test_result3

        if result == 'Normal vision':
            suggestion = 'Continue with the same glasses'
        elif result == 'Near Normal Vision':
            suggestion = 'It is better to change your glasses'
        elif result == 'Moderate Low Vision':
            suggestion = 'You need to change your glasses'
        elif result == 'Severe Low Vision':
            suggestion = 'Consult an eye specialist'
        elif result == 'Near Blindness':
            suggestion = 'Immediately consult an eye specialist'
        else:
            suggestion = 'Follow the instructions properly'      

        self.ids.r_name.text = patient_info['First Name'] + ' ' + patient_info['Last Name']
        self.ids.r_age.text = patient_info['Age']
        self.ids.r_place.text = patient_info['Place']
        self.ids.r_number.text = patient_info['Contact Number']
        self.ids.r_test.text = 'Glass Checker Test'
        self.ids.r_result.text = result
        self.ids.r_suggestion.text = suggestion


sm=ScreenManager()
sm.add_widget(StartWindow(name = "start"))
sm.add_widget(InfoWindow(name = "info"))
sm.add_widget(SelectWindow(name = "select"))

sm.add_widget(VisualAcuityWindow(name = "acuity"))
sm.add_widget(SnellenChartWindow(name = "snellen"))
sm.add_widget(RandomEWindow(name = "random_e"))
sm.add_widget(LandoltCWindow(name = "landolt_c"))

sm.add_widget(AstigmatismWindow(name = "astigma"))
sm.add_widget(Astigma1Window(name = "1astigma"))
sm.add_widget(Astigma2Window(name = "2astigma"))
sm.add_widget(Astigma3Window(name = "3astigma"))

sm.add_widget(GlassCheckerWindow(name = "glass"))
sm.add_widget(ImagesWindow(name = "gc_images"))
sm.add_widget(AlphabetsWindow(name = "gc_letters"))
sm.add_widget(NumbersWindow(name = "gc_numbers"))

sm.add_widget(AcuityResultWindow(name = 'acuity_result'))
sm.add_widget(AstigmaResultWindow(name = 'astigma_result'))
sm.add_widget(GlassCheckerResultWindow(name = 'glass_result'))

sm.add_widget(AcuityReportWindow(name = 'acuity_report'))
sm.add_widget(AstigmaReportWindow(name = 'astigma_report'))
sm.add_widget(GlassReportWindow(name = 'glass_report'))


class VisionApp(App):
    def build(self):
        self.title="e-VISION CLINIC"
        return sm

if __name__=="__main__":
    VisionApp().run()