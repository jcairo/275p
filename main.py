#!/Library/Frameworks/Python.framework/Versions/4.3/bin/python3
import npyscreen
import pdb
import imaplib
import getpass


from main_menu import MainMenu
from main_menu_login_popup import MainMenuPopup
from compose_mail import ComposeMail
from inbox import Inbox

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

        # holds the index of the currently highlighted msg in the
        # inbox form
        self.INBOX_MSG_TXT = 0

# app script.
if __name__ == "__main__":
    # create an application instance
    # and call its run method.
    app = MyApplication()
    app.run()
    print('done')
