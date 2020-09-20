from hotbox.managers import *

configManager = ConfigManager()
commandManager = CommandManager()


#Main class for controlling program state
class Main():
    def __init__(self, configManager, commandManager):
        self.state = 0
        self.configManager = configManager
        self.commandManager = commandManager
     
    def loop(self):
        while self.state != 5:
            if self.state == 0:
                self.main_menu()
            elif self.state == 1:
                self.change_resource()
                self.state = 0
            elif self.state == 2:
                self.list_keys()
                self.state = 0
            elif self.state == 3:
                self.delete_key()
                self.state = 0
            elif self.state == 4:
                self.add_key()
                self.state = 0
    
    #Ensure valid menu selection        
    def validate_selection(self,options,value):
        int_value = 0
        try:
            int_value = int(value)
        except ValueError:
            print('Invalid Selection')
        if int_value < 1 or int_value > options:
            print('Invalid Selection')
            int_value = 0
        return int_value
    
    def main_menu(self):
        options = 5
        menu = '''
Main Menu:
1. Set Resource File Path
2. List Hotkeys
3. Delete Hotkey
4. Add Hotkey
5. Exit
'''
        print(menu)
        while self.state == 0:
            self.state = self.validate_selection(options,input('Enter Selection: ')) 

    #Change location of openbox configuration file
    def change_resource(self):
        value = input('Set resource path. Currently using ' + 
               self.configManager.get_resource_path() + ': ')
        if value != '':
            self.configManager.set_resource_path(value)
            print('Resource path set to ' + self.configManager.get_resource_path() + '.')
    
    #List currently used hotkeys
    def list_keys(self):
        if configManager.is_loaded():
            self.configManager.generate_all_actions_string()
        else:
            print('Error: Configutation file could not be loaded')
    
    #delete a hotkey
    def delete_key(self):
        if configManager.is_loaded():
            self.configManager.delete_key()
        else:
            print('Error: Configutation file could not be loaded')

    #Add a new hotkey
    def add_key(self):
        if configManager.is_loaded():
            hotkey_string = input('Enter Hotkey E.G. A-t for Alt+t: ')
            if self.configManager.hotkey_available(hotkey_string):
                self.configManager.add_hotkey(hotkey_string,self.commandManager,False)
            else:
                if input(hotkey_string + ' is already in use! Continue? y/n: ') == 'y':
                    if input('Remove all actions associated with ' + hotkey_string + '? y/n: ') == 'y':
                        self.configManager.add_hotkey(hotkey_string,self.commandManager,True)
                    else:
                        self.configManager.add_hotkey(hotkey_string,self.commandManager,False)
        else:
            print('Error: Configuration file could not be loaded')

def main():
    main_man = Main(configManager,commandManager)
    #run main loop
    main_man.loop()

main()
