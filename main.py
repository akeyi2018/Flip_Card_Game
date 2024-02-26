from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
import random
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image 
from kivy.lang import Builder
Builder.load_file('card.kv')

class ImageButton(ButtonBehavior, Image):
    def __init__(self, source, front_source, back_source, text, **kwargs):
        super().__init__(**kwargs)
        self.source = source
        self.back_source = back_source
        self.font_source = front_source
        self.text = text
        
class MemoryGame(BoxLayout):
    def __init__(self, **kwargs):
        super(MemoryGame, self).__init__(**kwargs)
        self.cards = list(range(1,  7)) *  2
        random.shuffle(self.cards)
        self.flipped = []
        self.buttons = []
        self.create_board()

    def create_board(self):
        for i in range(3):  #  3 rows for  4 columns
            inner_layout = BoxLayout(orientation='horizontal', height=300, width=300, size_hint_y=None, spacing=10)
            for j in range(4):  #  4 columns
                index =  4 * i + j
                if index < len(self.cards):  # Ensure we don't go out of range
                    btn = ImageButton(source="./f.png",
                                      front_source= "./f.png",
                                      back_source=f"./{self.cards[index]}.png",text=" ")
                    btn.index = index
                    btn.bind(on_press=self.card_click)
                    self.buttons.append(btn)
                    inner_layout.add_widget(btn)
            self.ids['content'].add_widget(inner_layout) 

    def card_click(self, instance):
        # Check if the card is already flipped
        if instance.text != " ":
            return  # If the card is already flipped, do nothing

        if instance.source == "f.png":
            instance.source = f"./{self.cards[instance.index]}.png"
        else:
            instance.source = f"./{self.cards[instance.index]}.png"
    
        # Flip the card
        instance.text = str(self.cards[instance.index])
        # instance.font_size = '50sp'

        # Check if this is the first card flipped
        if not self.flipped:
            self.flipped.append(instance)
            self.first_card = self.cards[instance.index]
            self.first_card_index = instance.index
        else:
            # This is the second card flipped
            self.second_card = self.cards[instance.index]
            self.second_card_index = instance.index

            # Check if the cards match
            if self.first_card == self.second_card:
                # If the cards match, do nothing (or handle the match as desired)
                pass
            else:
                print(f'1:{self.first_card} 2:{self.second_card}')
                # If the cards do not match, flip them back after a delay
                Clock.schedule_once(lambda dt: self.flip_back(self.first_card_index, self.second_card_index),  1)

            # Reset the flipped list for the next pair
            self.flipped = []

            # # Check if all cards are matched
            # if len([btn for btn in self.buttons if btn.text == " "]) ==  0:
            #     print("Clear")

            # Check if all cards are matched
            if len([btn for btn in self.buttons if btn.text == " "]) ==   0:
                # Open a Popup with the "Clear" message
                close_button = Button(text='Close', size_hint=(None, None), size=(100,   50))
                popup_content = BoxLayout(orientation='vertical', size_hint=(None, None), size=(400,   400))
                popup_content.add_widget(Label(text='Clear'))
                popup_content.add_widget(close_button)
                popup = Popup(title='Clear', content=popup_content, size_hint=(None, None), size=(400,   400))
                
                # Bind the close button to the dismiss method of the Popup
                close_button.bind(on_release=popup.dismiss) 
                popup.open()
    
    def flip_back(self, first_card_index, second_card_index):
        self.buttons[first_card_index].text = " "
        self.buttons[second_card_index].text = " "
        # print(self.buttons[second_card_index].source)
        self.buttons[first_card_index].source = './f.png'
        self.buttons[second_card_index].source = './f.png'

        # print(self.buttons[second_card_index].back_source)

        # if self.source !=  "f.png":
        #     self.source == "f.png"
        # self.buttons[second_card_index].source == "f.png"
         

class MemoryApp(App):
    def build(self):
        return MemoryGame()

if __name__ == "__main__":
    MemoryApp().run()
