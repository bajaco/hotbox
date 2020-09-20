import os.path
import configparser
import xml.dom.minidom
import json

#Configuration class for defining and editing settings resource file
class ConfigManager:
    def __init__(self):
        self.loaded = False

        #Load configuration path from conf.ini
        self.config = configparser.ConfigParser()
        self.config.read('./hotbox/conf.ini')
        self.load_resource()

    def get_resource_path(self):
        return self.config['default']['path']

    def set_resource_path(self, path):
        self.config['default']['path'] = path
 


        with open('./hotbox/conf.ini', 'w') as configfile:
            self.config.write(configfile)
        self.load_resource()
    
    def refresh(self):
        self.keybinds = self.document.getElementsByTagName('keybind')

    def load_resource(self):
        try:
            self.dom = xml.dom.minidom.parse(os.path.expanduser(self.get_resource_path()))
            self.document = self.dom.documentElement
            self.keybinds = self.document.getElementsByTagName('keybind')
            self.loaded = True
            print('Loaded resource file at ' + self.get_resource_path())
        except OSError:
            print('*WARNING* Unable to load resource file at ' + self.get_resource_path() + '!')
            self.loaded = False
    
    def is_loaded(self):
        return self.loaded

    def reconfigure(self):
        try:
            cmd = 'openbox --reconfigure'
            os.system(cmd)
        except OSError:
            print('*Error* Could not reconfigure Openbox')
    
    #gets rid of annoying whitespace added by toprettyxml
    def clean_lines(self, text):
        lines = text.split('\n')
        newtext = '\n'.join([line for line in lines if line.strip() != ''])
        return newtext
    
    #save a backup before creating changes
    def save_backup(self):
        try:
            cmd = 'cp ' + self.get_resource_path() + ' ' + self.get_resource_path() + '.hotbox.backup'
            os.system(cmd)
            print('Backup file saved to ' + self.get_resource_path() + '.hotbox.backup')
        except OSError:
            print('*Warning* Could not create backup file!')

    #write changes to configuration file
    def save_resource(self):
        try:
            with open(os.path.expanduser(self.get_resource_path()), 'w') as f:
                f.write(self.clean_lines(self.dom.toprettyxml(indent='  ')))
                f.close()
        except OSError:
            print('Unable to write file!')

    #Recursively sorts through tagnames, attributes, etc to print what a hotkey does
    def generate_actions_string(self,node):
        actions = []
        if node.nodeName != '#text':
            if node.nodeValue:
                if node.nodeValue.strip() != '':
                    actions.append(node.nodeName + ':' + node.nodeValue)
            else:
                actions.append(node.nodeName + ':')
        else:
            if node.nodeValue:
                if node.nodeValue.strip() != '':
                    actions.append(node.nodeValue)
        if node.nodeType == 1:
            if node.hasAttributes():
                for name, value in node.attributes.items():
                    if name == 'key' or name == 'name':
                        actions.append(value)
                    else:
                        actions.append(name + ':' + value)
        if node.hasChildNodes():
            for child in node.childNodes:
                child_string = self.generate_actions_string(child)
                if child_string.strip() != '':
                    actions.append(child_string)

        return ' '.join(actions)

    #gets all actions_strings
    def generate_all_actions_string(self):
        all_actions_string = []
        self.refresh()
        for keybind in self.keybinds:
            all_actions_string.append(self.generate_actions_string(keybind))
        self.print_options(all_actions_string)

    def delete_key(self):
        all_actions_string = []
        self.refresh()
        for keybind in self.keybinds:
            all_actions_string.append(self.generate_actions_string(keybind))
        self.print_options(all_actions_string)
        delete_index = self.validate_input(all_actions_string)
        hotkey_string = self.keybinds[delete_index].attributes.items()[0][1]
        if input('Delete hotkey for ' + hotkey_string + '? y/n: ') == 'y':
                keybind = self.keybinds[delete_index]
                keyboard = self.document.getElementsByTagName('keyboard')[0]
                orphan = keyboard.removeChild(keybind)
                orphan.unlink()
                self.save_backup()
                self.save_resource()
                self.reconfigure()
    
    #check if a hotkey is in use already
    def hotkey_available(self,hotkey_string):
        self.refresh()
        for keybind in self.keybinds:
            if hotkey_string == keybind.attributes.items()[0][1]:
                return False
        return True
    
    #returns a numbered list of options
    def print_options(self, options):
        for i,v in enumerate(options):
            print(str(i+1) + '. ' + str(v))

    #ensures valid option selection
    def validate_input(self, options):
        size =  len(options)
        valid = False
        while not valid:
            entry = input('Enter number 1-' + str(size) + ': ')
            try:
                entry = int(entry)
                if 0 < entry <= size:
                    valid = True
                else:
                    print('Invalid Entry')
            except ValueError:
                print('Invalid Entry')
        return entry - 1
    
    #create a node on parent with option text subnode and attributes
    def make_node(self,parent,node_name,text=None, **kwargs):
        node = self.dom.createElement(node_name)
        for name, value in kwargs.items():
            node.setAttribute(name, value)
        if text:
            node.appendChild(self.dom.createTextNode(text))
        parent.appendChild(node)
        return node


    #add a hotkey
    def add_hotkey(self,hotkey_string,commandManager,remove):
 
        self.save_backup()

        #get keyboard element
        keyboard = self.document.getElementsByTagName('keyboard')[0]
        
        #remove all hotkey instances if directed by user
        if remove:
            if not self.hotkey_available(hotkey_string):
                child = None
                for keybind in self.keybinds:
                    if keybind.attributes.items()[0][1] == hotkey_string:
                        child = keybind
                        orphan = keyboard.removeChild(child)
                        orphan.unlink()
        
        #create root keybind node
        bind_node = self.make_node(keyboard,'keybind',key=hotkey_string)
        
        self.add_action(bind_node,commandManager)

        #save changes
        self.save_resource()
        #apply changes
        self.reconfigure() 
    
    #add_actions method is separate from add_hotkey so finalactions can recursively add actions
    def add_action(self,parent_node,commandManager):

        #get available commands
        commands = commandManager.get_commands()
        self.print_options(commands)
        command = commands[self.validate_input(commands)]
        print(command + ': ')
        
        #create action node for keybind
        action_node = self.make_node(parent_node,'action',name=command)
        options = commandManager.get_options(command)
        
        #loop through options and create nodes as necessary
        for option in options:
            
            #startupnotify-specific options
            if option == 'startupnotify':
                if 'y' == input('Notify on startup? y/n: '):
                    option_node = self.make_node(action_node,'startupnotify')
                    enabled = input('Enter value for "enabled": (default value: "no"): ')
                    if enabled != '':
                        sub_option_node = self.make_node(option_node,'enabled',text=enabled)
                    wmclass = input('Enter value for "wmclass": (default value: "none"): ')
                    if wmclass != '':
                        sub_option_node = self.make_node(option_node,'wmclass',text=wmclass)
                    name = input('Enter value for "name": (default value: "none"): ')
                    if name != '':
                        sub_option_node = self.make_node(option_node,'name',text=name)
                    icon = input('Enter value for "icon": (default value: "none"): ')
                    if icon != '':
                        sub_option_node = self.make_node(option_node,'icon',text=icon)
                        
            #finalactions-specific code, requires sub-actions
            elif option == 'finalactions':
                enabled = input('Use custom "finalactions"? Defaults to using Focus, Raise, and Unshade. y/n: ')
                if enabled == 'y':
                    option_node = self.make_node(action_node,'finalactions')
                    adding = True
                    while adding:
                        if input('Enter "add" to add an action, "quit" to stop: ') == 'add':
                            self.add_action(option_node,commandManager)
                        else:
                            adding = False               
        
            #remaining options
            else:
                prompt = 'Enter value for "' + option + '": '
                if options.get(option) != '':
                    prompt += '(leave blank for default value: "' + options.get(option) + '"): '
                new_value = input(prompt)
                if new_value != '':
                    option_node = self.make_node(action_node,option,text=new_value)
                    
                    
#class to parse commands.json and return commands and options
class CommandManager:
    def __init__(self):
        with open('hotbox/commands.json') as f:
            self.commands = json.load(f)

    def get_commands(self):
        return [command for command in self.commands]

    def get_options(self,command):
        options = self.commands.get(command)
        return options
