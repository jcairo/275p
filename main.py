#!/Library/Frameworks/Python.framework/Versions/4.3/bin/python3
import npyscreen
import pdb
import imaplib
import getpass


from main_menu import MainMenu
from main_menu_login_popup import MainMenuPopup
from compose_mail import ComposeMail
from inbox import Inbox
from spell_check_popup import SpellCheckPopup
from edit_distance import read_in_dict

class MyApplication(npyscreen.NPSAppManaged):
    """
    This is the main application class which manages the application.
    It handles switching forms, the main application loop and other
    bookkeeping
    """
    def onStart(self):
        # npyscreen.setTheme(npyscreen.Themes.ColorfulTheme)

        self.addFormClass('MAIN', MainMenu, name="MAIN MENU")
        self.addFormClass('MAIN_POPUP',
                     MainMenuPopup, name="Gmail login")
        self.addFormClass('COMPOSE_MAIL', ComposeMail, name="Compose")
        self.addFormClass('INBOX', Inbox, name="Mail")
        self.addFormClass('SPELL_CHECK_POPUP', SpellCheckPopup, name="Spell Check")
       
        # holds the index of the currently highlighted msg in the
        # inbox form
        self.INBOX_MSG_TXT = 0
       
        
        self.english_dict = []
        #stores the list of indices corresponding to misspelt words
        #in email message
        self.index_list = None
        #index of index_list we are currently on
        self.next_index = 0
        #holds the user set values of email to, subject and message feilds
        #for reference
        self.message_save = "" 
        self.email_to = None
        self.email_subject = None

# app script.
if __name__ == "__main__":
    # create an application instance
    # and call its run method.
    app = MyApplication()
    app.run()
    print('done')


