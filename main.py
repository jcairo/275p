#!/Library/Frameworks/Python.framework/Versions/3.3/bin/python3
import npyscreen
import pdb

from main_menu import MainMenu
from main_menu_login_popup import MainMenuPopup
"""
from auto_transaction import AutoTransaction, AddBuyer, AddSeller
from driver_licence_registration import DriverLicenceRegistration
from violation_record import ViolationRecord
from search_engine import SearchEngine
from add_owner_on_vehicle import AddOwnerOnVehicle
from database import Database
from driver_search import DriverSearch
from violation_search import ViolationSearch
from vehicle_history_search import VehicleHistorySearch    
from add_people import AddPerson        
"""

class MyApplication(npyscreen.NPSAppManaged):
    """
    This is the main application class which manages the application.
    It handles switching forms, the main application loop and other
    bookkeeping
    """
    def onStart(self):
        # empty Database object with db.logged_in = False
        # self.db = Database()   
        self.addFormClass('MAIN', MainMenu, name="MAIN MENU")
        self.addFormClass('MAIN_POPUP',
                     MainMenuPopup, name="Connect to Oracle")
        """
        self.addFormClass('NEWVEHICLEREGISTRATION',
                     NewVehicleRegistration, name='New Vehicle Registration')

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
