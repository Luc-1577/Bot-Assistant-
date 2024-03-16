import sqlite3
import time
import webbrowser as web
import pyautogui as pg
      
        
def zap(nums, mes):
   for i, num in enumerate(nums):
      url = 'https://web.whatsapp.com/send?phone=' + str(num) + '&text=' + str(mes[i])
      web.open(url)  
      time.sleep(30)
      pg.click(x=1200, y=536)
      time.sleep(0.5)    
      pg.press('Enter')
      time.sleep(3)  
      pg.hotkey('ctrl', 'w')
   
   
class db:
   def __init__(self):
      self.conn = sqlite3.connect('src/contacts.db')
      self.cursor = self.conn.cursor()
  
         
   def table(self):
      self.cursor.execute('''
                     CREATE TABLE IF NOT EXISTS contacts(
                        name VARCHAR(50) PRIMARY KEY,
                        number VARCHAR(50)
                     )''')
 
      
   def add(self, name, num):
      self.cursor.execute('''INSERT INTO contacts(number, name) VALUES(?, ?)''', (num, name))
      self.conn.commit()


   def show_all(self):
      self.cursor.execute('''SELECT * FROM contacts''')
      informations = self.cursor.fetchall()
      
      list = []
      all = []
      
      for information in informations:
         colums = [name[0] for name in self.cursor.description]
         linha_dict = dict(zip(colums, information))
         list.append(linha_dict)

      for i in range(len(list)):
         value1 = list[i].get('name')
         value2 = list[i].get('number')
         all.append({value1 : value2})
         
      if all:
         return all 

      else:
         return None
   
      
   def select(self, name):
      self.cursor.execute('''SELECT * FROM contacts WHERE name = ?''', (name,))
      information = self.cursor.fetchall()
      
      list = []
      per = []
      
      for info in information:
         colums = [name[0] for name in self.cursor.description]
         linha_dict = dict(zip(colums, info))
         list.append(linha_dict)
         
         for i in range(len(list)):
            value1 = list[i].get('name')
            value2 = list[i].get('number')
            per.append({value1 : value2})

            return per
 
   
   def delete(self, name):
      self.cursor.execute('''DELETE FROM contacts WHERE name = ?''', (name,))
      self.conn.commit()
  
   def dels(self):
      self.cursor.execute('''drop table contacts''')
      self.conn.commit()
  
   def rename(self, new_name, name):
     self.cursor.execute('''UPDATE contacts SET name = ? WHERE name = ?''', (new_name, name,))
     self.conn.commit()
    
     
   def update(self, new_num, name):
      self.cursor.execute('''UPDATE contacts SET number = ? WHERE name = ?''', (new_num, name,))
      self.conn.commit()
  
   
def add(R1):
   R1 = R1.replace('add', '')
   R1 = R1.title().split(';')

   for i in range(len(R1)):
      R1[i] = R1[i].strip()

   cmd = db()
   cmd.table()

   new = R1.copy()
   exis = []
   
   cn = 0
   
   for i in range(len(R1)):     
      for phnum in R1[i]:
         if not phnum.isalpha():
            R1[i] = R1[i].replace(phnum, '')
     
      if cmd.select(R1[i]):
         exis.append(f'{R1[i]} already exists ({chk(R1[i])[0]})')

      else:
         for x in new[i]:
            if x == '>':
               break
            else:   
               for y in new[i]:
                  if y == '>':
                     break
                  elif y == x:
                     cn += 1
                  
               new[i] = new[i].replace(x, '', cn)
               cn = 0

         new[i] = new[i].replace('>', '')
         new[i] = new[i].strip()

      cmd.add(R1[i], new[i])

   return exis if exis else None
   
   
def all_data():
   cmd = db()
   cmd.table()
   people = cmd.show_all()
   
   all = []
   
   if people != None:
      for i in range(len(people)):
         for person, number in people[i].items():
            all.append(person + ' --> ' + number)
      return all
   
   else:
      return 'The contact list is empty'
       
         
def chk(R1):
   R1 = R1.replace('check', '')
   R1 = R1.title().split(';')

   for i in range(len(R1)):
      R1[i] = R1[i].strip()
      
   cmd = db()
   cmd.table()
   
   exis = []
   noexis = []
   
   for i in range(len(R1)):
      person = cmd.select(R1[i])
   
      if person:
         for name, num in person[0].items():
            exis.append(name + ' --> ' + num)
   
      else:
         noexis.append(f'{R1[i]} doesn\'t exists')
   
   if not exis:
      return noexis
   elif not noexis:
      return exis
   else:
      al = exis + noexis
      return al
         

def dele(R1):
   R1 = R1.replace('dele', '')
   R1 = R1.title().split(';')
   

   for i in range(len(R1)):
      R1[i] = R1[i].strip()
      
   cmd = db()
   cmd.table()
   
   for i in range(len(R1)):
      if cmd.select(R1[i]):
         cmd.delete(R1[i])  
      
   return 'Ok \n'
         
              
def tot():
   tot = 0
   
   cmd = db()
   cmd.table()
   people = cmd.show_all()
   
   for i in range(len(people)):
      for _ in people[i]:
         tot = tot + 1
   return 'total: '+ str(tot)


def sms(R1):
   R1 = R1.replace('sms', '')
   R1 = R1.title().split(';')

   for i in range(len(R1)):
      R1[i] = R1[i].strip()
      
   cmd = db()
   cmd.table()

   messages = R1.copy()
   contact = []
   noexis = []
   
   xF = ''
   cn = 0


   symbols = ' +-()'

   for i in range(len(R1)):
      for x in R1[i]:
         if x == '-':
            break
         else:
            xF = xF + x
      R1[i] = xF.strip()   
      xF = ''

      person = cmd.select(R1[i])
      
      if person:
         for name, num in person[0].items():
            if any(char in symbols for char in num):
               for char in symbols:
                  num = num.replace(char, '')
            
            for y in messages[i]:
               if y == '>':
                  break
               else:
                  for z in messages[i]:
                     if z == '>':
                        break
                     elif z == y:
                        cn += 1
                     
               messages[i] = messages[i].replace(y, '', cn)
               cn = 0

         messages[i] = messages[i].replace('>', '')
         messages[i] = messages[i].title().strip()
         
         contact.append(num)
   
      else:
         noexis.append(f'{R1[i]} doesn\'t exists')

   print(end='\n\n')
   zap(contact, messages)
       
      
def rename(R1):
   R1 = R1.replace('rename', '')
   R1 = R1.title().split(';')
   
   for i in range(len(R1)):
      R1[i] = R1[i].strip()
   
   cmd = db()
   cmd.table()
   
   exis = []
   noexis = []
   new_name = R1.copy() 

   xF = ''
   cn = 0

   for i in range(len(R1)):
      for x in R1[i]:
         if x == '-':
            break
         else:
            xF = xF + x
      R1[i] = xF.strip()   
      xF = ''
                     
      if cmd.select(R1[i]) == None:
         noexis.append(f'{R1[i]} doesn\'t exists')

      else:
         for y in new_name[i]:
            if y == '>':
               break
            else:
               for z in new_name[i]:
                  if z == '>':
                     break
                  elif z == y:
                     cn += 1
                     
               new_name[i] = new_name[i].replace(y, '', cn)
               cn = 0

         new_name[i] = new_name[i].replace('>', '')
         new_name[i] = new_name[i].title().strip()
               
         cmd.rename(new_name[i], R1[i])
         exis.append(f'{R1[i]} is {new_name} now')   
      
   if not exis:
      return noexis
   elif not noexis:
      return exis
   else:
      al = exis + noexis
      return al
 
   
def update(R1):
   R1 = R1.replace('update', '')
   R1 = R1.title().split(';')

   for i in range(len(R1)):
      R1[i] = R1[i].strip()
   
   cmd = db()
   cmd.table

   exis = []
   noexis = []
   new_num = R1.copy() 
   
   cn = 0


   for i in range(len(R1)):
      for phnum in R1[i]:
         if not phnum.isalpha():
            R1[i] = R1[i].replace(phnum, '')
     
      if cmd.select(R1[i]) == None:
         noexis.append(f'{R1[i]} doesn\'t exists')
      
      else:
         for x in new_num[i]:
            if x == '>':
               break
            else:   
               for y in new_num[i]:
                  if y == '>':
                     break
                  elif y == x:
                     cn += 1
                  
               new_num[i] = new_num[i].replace(x, '', cn)
               cn = 0

         new_num[i] = new_num[i].replace('>', '')
         new_num[i] = new_num[i].strip()
                
         cmd.update(new_num[i], R1[i])
         exis.append(f'{R1[i]}\'s number updated')
      
   if not exis:
      return noexis
   elif not noexis:
      return exis
   else:
      al = exis + noexis
      return al

      
def help():
   print(
      '"add (name) --> (num)" add the person to the contact list',
      '"all" shows everybody in the contact list',
      '"check (name)" check if the person is in the contact lsit',
      '"dele (name)" delet the person',
      '"tot" shows how many people are in the list',
      '"sms (name) --> (message)" sends message to the person',
      '"rename (name) --> (new name)" rename the contact',
      '"update (name) --> (new number)" update the person number',
      '[Note: The commands with "()" can be used with more than one person. Ex: "Add Luc +xx xxxxx-xxxxx; Shoga +xx xxxxx-xxxxx" --> It\'ll add Luc and Shoga to the lsit]',
      
      sep='\n\n', end='\n\n'
   )
   
   
   
if __name__ == '__main__':
   print('Type --help to see the commands', end='\n\n')
   
   while True:
      R1 = input('> ')
      R1 = R1.lower()

      if R1.strip() == 'all':
         print(all_data())    

      elif R1.strip() == 'tot':
         print(tot())
         
      elif R1.startswith('check'):
         print(chk(R1))
      
      elif R1.startswith('sms'):
         print(sms(R1))
         
      elif R1.startswith('add'):
         print(add(R1))
         
      elif R1.startswith('dele'):
         print(dele(R1))
         
      elif R1 == '--help':
         help()

      elif R1.startswith('rename'):
         print(rename(R1))
         
      elif R1.startswith('update'):
         print(update(R1))
         
      elif 'del' == R1:
         db().dels()
         
      else:
         print('Type --help to see the commands', end='\n\n')