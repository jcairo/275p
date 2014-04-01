#!/Library/Frameworks/Python.framework/Versions/3.3/bin/python3
import npyscreen
import pdb
import imaplib
import getpass


from main_menu import MainMenu
from main_menu_login_popup import MainMenuPopup
from compose_mail import ComposeMail
from spell_check_popup import SpellCheckPopup

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
        self.addFormClass('SPELL_CHECK_POPUP', SpellCheckPopup, name="Spell Check")

        # create the gmail connection object.











        """
        self.addFormClass('NEWVEHICLEREGISTRATION',
                     NewVehicleRegistration, name='New
                     Vehicle Registration')

        self.auto_transaction_initialized = False
        self.addFormClass('ADDBUYER', AddBuyer, name='Add Buyer')
        self.addFormClass('ADDSELLER', AddSeller, name='Add Seller')



        self.addFormClass('DRIVERLICENCEREGISTRATION',
                     DriverLicenceRegistration, name='Driver Licence Registration')
        self.addFormClass('VIOLATIONRECORD',
                     ViolationRecord, name='Violation Record')
        self.addFormClass('SEARCHENGINE',
                     SearchEngine, name='Search Engine')
        self.addFormClass('DRIVER_SEARCH',
                     DriverSearch, name='Driver Search')
        self.addForm('ADDOWNERONVEHICLE',
                     AddOwnerOnVehicle, name='Add owner')
        self.addFormClass('VIOLATION_SEARCH',
                     ViolationSearch, name='Violation Search')
        self.addFormClass('VEHICLE_HISTORY_SEARCH',
                     VehicleHistorySearch, name='Vehicle History Search')
        """

# app script.
if __name__ == "__main__":
    # create an application instance
    # and call its run method.
    app = MyApplication()
    app.run()
    print('done')
