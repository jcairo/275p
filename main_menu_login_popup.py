import npyscreen
import imaplib
import getpass
from gmaillib import message, account
import smtplib

# this is the login form.
class MainMenuPopup(npyscreen.ActionPopup):
    OK_BUTTON_TEXT = "OK"
    CANCEL_BUTTON_TEXT = "CANCEL"    


    def create(self):
        self.username = self.add(npyscreen.TitleText, name="Gmail address:",
            begin_entry_at = 17)
        self.password = self.add(npyscreen.TitlePassword, name="Password:",
            begin_entry_at = 17)

        # prefilled credentials for testing.
        self.username.value = 'joncairo'
        self.password.value = 'Carrma123'

    # this gets run when the user selects ok in the login form
    def on_ok(self):
        # try to create an instance of the mail class
        # based on the users login credentials.
        try:
            # pass account credentials, a link to the parent app
            # and a queue object attached to the parent application
            # for interprocess communication.
            self.parentApp.mail = account(self.username.value,
                self.password.value, parent=self.parentApp, 
                queue=self.parentApp.queue)

        except Exception as e:
            npyscreen.notify_confirm(e, title="Error",
                form_color='STANDOUT', wrap=True, editw=1)
            return

        # notify the user that the login worked
        npyscreen.notify_confirm("Login successful", title="Success",
            form_color='STANDOUT', wrap=True, editw=1)

        # take them back to the main men 
        self.parentApp.switchForm('MAIN')

    # this gets run when the user selects cancel on the login form.
    def on_cancel(self):
        self.parentApp.switchFormPrevious()

