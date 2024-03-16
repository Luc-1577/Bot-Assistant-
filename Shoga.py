import customtkinter as CTk
import datetime
import webbrowser
import requests
from src.calculator import calculus
import src.wpp as wpp


class Shoga:
    def __init__(self):
        self.root = CTk.CTk()
        self.root.title("Shoga Bot")
        CTk.set_appearance_mode("dark")
        self.root.geometry('600x435')
        self.root.resizable(True, True)
        self.root.minsize(width = 400, height = 435)

        self.chat_display = CTk.CTkTextbox(self.root, wrap=CTk.WORD, state=CTk.NORMAL) 
        self.chat_display.pack(fill=CTk.BOTH, expand=True)
        self.chat_display.bind('<Motion>', self.initial)            

        self.user_input_entry = CTk.CTkEntry(self.root)
        self.user_input_entry.pack(fill=CTk.X, pady=1)
        self.user_input_entry.bind('<Motion>', self.initial)  
        self.user_input_entry.bind("<Return>", self.send_message)  

        self.send_button = CTk.CTkButton(self.root, text="Send", command=self.send_message)
        self.send_button.pack()

    def initial(self, event):
        self.now = datetime.datetime.now()
        self.current_time = self.now.strftime("%H")    
        if '06' <= self.current_time < '12':
            self.greeting = 'Good morning.'
        elif '12' <= self.current_time < '18':
            self.greeting = 'Good afternoon.'
        elif '18' <= self.current_time > '0':
            self.greeting = 'Good evening.'
        elif '00' <= self.current_time < '06':
            self.greeting = 'Oh, you are awake (*_*)\n'

        self.chat_display.insert(CTk.END, f"Shoga - {self.greeting} How can I help you?\n")
        self.chat_display.configure(state=CTk.DISABLED)
    
    def send_message(self, event=None):
        self.user_input = self.user_input_entry.get()
        if '' == self.user_input: pass
        else:
            self.chat_display.configure(state=CTk.NORMAL)  
            self.chat_display.insert(CTk.END, f"You - {self.user_input}\n")

            self.response = get_bot_response(self.user_input)
            self.chat_display.insert(CTk.END, f"Shoga - {self.response}\n")
            self.chat_display.configure(state=CTk.DISABLED)
            self.chat_display.yview_moveto(1.0)
            self.user_input_entry.delete(0, CTk.END)  

            if "exit" in self.user_input.lower():
                self.chat_display.configure(state=CTk.DISABLED)
                self.user_input_entry.configure(state=CTk.DISABLED)
                self.send_button.configure(state=CTk.DISABLED)
                self.after(1200, self.root.destroy)

    def start(self):
        self.root.mainloop()


def get_current_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M:%S %p")
    return f"Shoga - It's {current_time}"

def get_current_date():
    now = datetime.datetime.now()
    current_date = now.strftime("%A(%d), %B(%m) %Y")
    return f"Shoga - It's {current_date}"

def get_site_name(command_str):
    part = command_str.split(" ")
    junt = ""
    for i in part:
        if i == "open":
            continue
        junt = junt + i
    return junt

def open_site(site):
    url = "https://www.{}.com/".format(site)
    try:
        response = requests.head(url)
        if response.status_code == 200:
            webbrowser.open(url)
            return "Ok ^^"
    except:
        pass

def open_gpt():
    url = "https://chat.openai.com/"
    webbrowser.open(url)
    return "Ok"

def pre_calculus(user_input):
    x = ''
    for _ in user_input:
        if _ == "calculate":
            continue
        x += _
    return x

def help():
    command = """"time" Shows time
"Date" Shows what day is today
"Open site_name" Open site
"Calculate numerical_expression" will show the result. Ex: Calculate 6 + 2 * 3
"Exit" End the chat
"add (name) --> (num)" add the person to the contact list
"all" shows everybody in the contact list
"check (name)" check if the person is in the contact lsit
"dele (name)" delet the person
"tot" shows how many people are in the list
"sms (name) --> (message)" sends message to the person
"rename (name) --> (new name)" rename the contact
"update (name) --> (new number)" update the person number
[Note: The commands with "()" can be used with more than one person. Ex: "Add Luc +xx xxxxx-xxxxx; Shoga +xx xxxxx-xxxxx" --> It'll add Luc and Shoga to the lsit"""
    return command

def get_bot_response(user_input):
    if "time" in user_input.lower():
        return get_current_time()

    elif "date" in user_input.lower():
        return get_current_date()
        
    elif ("--help" in user_input.lower()) or ("what can you do?" in user_input.lower()):
        return help()
        
    elif ("open chatgpt" in user_input.lower()) or ("open chat gpt" in user_input.lower()) or ("open gpt" in user_input.lower()):
        return open_gpt()
        
    elif "open" in user_input.lower():
        site = get_site_name(user_input)
        return open_site(site)
        
    elif "calculate" in user_input.lower():
        expression = pre_calculus(user_input)
        return calculus(expression)
            
    elif "exit" in user_input.lower():
        return 'Bye ^^'  

    elif user_input.lower() == 'all':
        st = ''
        for i in range(len(wpp.all_data())):
            st = st + wpp.all_data()[i] + '\n' 
        return st

    elif user_input.lower() == 'tot':
       return wpp.tot()
       
    elif user_input.startswith('check'):
        st = ''
        for i in range(len(wpp.chk(user_input))):
            st = st + wpp.chk(user_input)[i] + '\n' 
        return st
    
    elif user_input.startswith('sms'):
       return wpp.sms(user_input)
       
    elif user_input.startswith('add'):
       if wpp.add(user_input):
        st = ''
        for i in range(len(wpp.add(user_input))):
            st = st + wpp.add(user_input)[i] + '\n'
        return st

       else:
           return 'Done'      
        
    elif user_input.startswith('dele'):
       return wpp.dele(user_input)
       
    elif user_input == '--help':
       return help()
   
    elif user_input.startswith('rename'):
        st = ''
        for i in range(len(wpp.rename(user_input))):
            st = st + wpp.rename(user_input)[i] + '\n' 
        return st
           
    elif user_input.startswith('update'):
        st = ''
        for i in range(len(wpp.update(user_input))):
            st = st + wpp.update(user_input)[i] + '\n' 
        return st
    
    else:
        return "I don't know if I can do that, please type --help to see the commands"

Shoga().start()