import npyscreen

# this is the screen you are forwarded to on startup.
class MainMenu(npyscreen.FormBaseNew):
    def notify_not_logged_in(self):
        npyscreen.notify_confirm("Please log in first!", 
            title="No Database Connection", form_color='STANDOUT',
            wrap=True, wide=False, editw=1)
        self.parentApp.switchForm("MAIN")

    def create(self):
        """
        THis is run like the __init__ method when
        we create a new class instance
        """
        # set up button press methods
        def press_gmail_login(*args):
            self.parentApp.switchForm("MAIN_POPUP")
        
        def press_compose_button(*args):
            self.parentApp.switchForm("COMPOSE_MAIL")

        def press_inbox_button(*args):
            self.parentApp.switchForm("INBOX")

        # setup buttons..
        self.login_button = self.add(npyscreen.ButtonPress, 
            name="Gmail Login")
        self.login_button.whenPressed = press_gmail_login

        self.compose_button = self.add(npyscreen.ButtonPress, 
            name="Compose New Mail")
        self.compose_button.whenPressed = press_compose_button

        self.inbox_button = self.add(npyscreen.ButtonPress, 
            name="Inbox")
        self.inbox_button.whenPressed = press_inbox_button
        """
        def buttonpress1(*args):
            if self.parentApp.db.logged_in: self.parentApp.switchForm("NEWVEHICLEREGISTRATION")
            else: self.notify_not_logged_in()
        def buttonpress2(*args):
            if self.parentApp.db.logged_in:
                if not self.parentApp.auto_transaction_initialized:
                    self.parentApp.addForm('AUTOTRANSACTION', AutoTransaction, name='Auto Transaction')
                    self.parentApp.auto_transaction_initialized = True
                self.parentApp.switchForm("AUTOTRANSACTION")
            else: self.notify_not_logged_in()
        def buttonpress3(*args):
            if self.parentApp.db.logged_in: self.parentApp.switchForm("DRIVERLICENCEREGISTRATION")
            else: self.notify_not_logged_in()
        def buttonpress4(*args):
            if self.parentApp.db.logged_in: self.parentApp.switchForm("VIOLATIONRECORD")
            else: self.notify_not_logged_in()
        def buttonpress5(*args):
            if self.parentApp.db.logged_in: self.parentApp.switchForm("SEARCHENGINE")
            else: self.notify_not_logged_in()
        def buttonpress6(*args):
            self.parentApp.setNextForm(None)
            self.editing = False

        self.button0 = self.add(npyscreen.ButtonPress, name="Oracle Login")
        self.button0.whenPressed = buttonpress0
        self.nextrely += 1 
        self.button1 = self.add(npyscreen.ButtonPress, name="New Vehicle Registration")
        self.button1.whenPressed = buttonpress1
        self.button2 = self.add(npyscreen.ButtonPress, name="Auto Transaction")
        self.button2.whenPressed = buttonpress2
        self.button3 = self.add(npyscreen.ButtonPress, name="Driver Licence Registration")
        self.button3.whenPressed = buttonpress3
        self.button4 = self.add(npyscreen.ButtonPress, name="Violation Record")
        self.button4.whenPressed = buttonpress4
        self.button5 = self.add(npyscreen.ButtonPress, name="Search Engine")
        self.button5.whenPressed = buttonpress5
        self.nextrely += 1
        self.button6 = self.add(npyscreen.ButtonPress, name="Quit",)
        self.button6.whenPressed = buttonpress6
        """

