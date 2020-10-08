from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color
from kivy.core.window import Window
#from kivy.graphics import Rectangle
from kivy.properties import ObjectProperty
import time
from threading import Thread
from kivy.clock import Clock
import os.path
import sys
from kivy.lang import Builder
import keyboard


Window.clearcolor = (25/255.0, 55/255.0, 116/255.0, 1)





class CounterGridLayout(FloatLayout):
    


    
        
    
        

      

    times_pressed = 0 
    tickets = 0
    additional_time = ObjectProperty(None)
    additional_time_reason = ObjectProperty(None)
    emergency_time = ObjectProperty(None)
    emergency_time_reason = ObjectProperty(None)
    start_btn = ObjectProperty(None)
    clock = 0
    hours = 0
    productive_time = 0
    timer = ObjectProperty(None)
    productivity = ObjectProperty(None)
    remove_hints = ObjectProperty(None)
    hints_counter = 0
    hint1 = ObjectProperty(None)
    hint2 = ObjectProperty(None)
    hint3 = ObjectProperty(None)
    hint4 = ObjectProperty(None)
    hint5 = ObjectProperty(None)
    hint6 = ObjectProperty(None)
    hint7 = ObjectProperty(None)
    tickets_label = ObjectProperty(None)
    tickets_left = ObjectProperty(None)
    tickets_left_normal = 60
    close_app = ObjectProperty(None)

    

    def NewTicketButton(self, *args):
        self.tickets += 1
        self.tickets_label.text = "Tickets: " + str(self.tickets) 

    
    def key_input(self, *args):
        if keyboard.is_pressed('F9'):
            self.key_listener()
            
            
	        

    def StartTimerBtn(self):
        self.times_pressed += 1
        self.key_listener2 = Clock.schedule_interval(self.key_input, 0.005)
        self.key_listener = Clock.create_trigger(self.NewTicketButton, timeout=0.25, interval=0.25)
        

        
        
        if self.times_pressed == 1:
            file = open ("5CA.txt", "a", encoding="utf- 8")
            file.write(time.ctime() + "\n")
            file.close()

        if self.times_pressed % 2 == 0:
            self.start_btn.text = "Start again!"
            Clock.schedule_once(self.stop_updating_time_label)
            
        else: 
            self.start_btn.text = "Break / Meal / Bathroom"
            self.function_interval = Clock.schedule_interval(self.update_time_label, 1)
    
    def update_time_label(self, *args):
        self.clock += 1
        self.productive_time += 1
        mins = self.clock // 60
        self.hours = mins // 60
        mins_new = mins % 60
        secs = self.clock % 60
        self.timer.text = str("0" + str(self.hours) if self.hours > 0 else "00") + " : " + str(mins_new if mins_new > 9 else "0" + str(mins_new)) + " : " + str(secs if secs > 9 else "0" + str(secs))
        self.productivity.text = "  Productivity: " + str(round(self.tickets / (self.productive_time/3600) if self.productive_time != 0 else 0, 2))
        self.tickets_left.text = "  Tickets left (to minimum): " + str(self.tickets_left_normal - self.tickets)

    def stop_updating_time_label(self, *args):
        self.function_interval.cancel()

    def additional_time_func(self):
        # self.productive_time -= (int(self.additional_time.text)*60)
        # #self.tickets_left.text = "  Tickets left (to minimum): " + str(round(((8*3600 - int(self.additional_time.text)*60)/3600 * 10) - self.tickets))
        # self.tickets_left_normal -= int(self.additional_time.text) // 6
        file = open ("5CA.txt", "a", encoding="utf- 8")
        file.write(self.additional_time.text + " minutes was spent for " + "\"" + self.additional_time_reason.text + "\"" + "\n")
        file.close()
        self.additional_time_reason.text = ""
        self.additional_time.text = ""

    def time_deduction(self):
        #делю нацело на 8, так как за 8 минут я должен отправить один тикет (при норме в 7.5 в час)
        #self.productive_time -= (int(self.emergency_time.text)*60)
        self.tickets_left_normal -= int(self.emergency_time.text) // 8
        file = open ("5CA.txt", "a", encoding="utf- 8")
        file.write("Your working hours were reduced by " + self.emergency_time.text + " minutes " + "due to the " + "\"" + self.emergency_time_reason.text + "\"" + "\n")
        file.close()
        self.emergency_time_reason.text = ""
        self.emergency_time.text = ""

        
        
    def remove_hints_func(self):
        self.hints_counter += 1

        if self.hints_counter % 2 == 0:
            self.remove_hints.text = "Remove hints"
            self.hint1.text = "Press when you have sent,\n    a reply to the player. \n                    <-"
            self.hint2.text = "   Type in the time (in minutes) you have\nspent on meeting, training, game time, etc.\n                                   ->"
            self.hint3.text = "Working time ->"
            self.hint4.text = "<- Your productivity."
            self.hint5.text = "Click to start the app"
            self.hint6.text = "         If you have to work less\n    due to any kind of emergency -\n write the time and the reason here.\n         Then, click " + "\"" + "Spent time" + "\"" + "."
            self.hint7.text = "                  It will close the app\n and record your statistics in file " + "\"" + "5CA.txt" + "\"" + " ->"
        else: 
            self.remove_hints.text = "Return hints"
            self.hint1.text = ""
            self.hint2.text = ""
            self.hint3.text = ""
            self.hint4.text = ""
            self.hint5.text = ""
            self.hint6.text = ""
            self.hint7.text = ""
            

    def close_app_func(self):
        file = open ("5CA.txt", "a", encoding="utf- 8")
        file.write("Your handling emails time: " + str("0" + str(self.productive_time//3600) if self.productive_time//3600 > 0 else "00") \
         + ":" + str((self.productive_time // 60 % 60) if (self.productive_time // 60 % 60) > 9 else "0" + str(self.productive_time // 60 % 60)) \
         + ":" + str(self.productive_time % 60 if self.productive_time % 60 > 9 else "0" + str(self.productive_time % 60)) + "\nYou have done " + str(self.tickets) + " tickets" + "\nYour productivity for today is: "\
         + str(round(self.tickets / (self.productive_time/3600) if self.productive_time != 0 else 0, 2)) + "\n"*4)
        file.close()
        sys.exit()
        
            
        

        
        
     
        
        


 
class CounterApp(App):
    def build(self):
        
        return CounterGridLayout()
    
            



if __name__ == "__main__":
    
    CounterApp().run()
    
    
    

       