import npyscreen
import imaplib
import getpass
from gmail import Mail

# this is the login form.
class MainMenuPopup(npyscreen.ActionPopup):
    def create(self):
        self.username = self.add(npyscreen.TitleText, name="Gmail address:")
        self.password = self.add(npyscreen.TitlePassword, name="Password:")

    # this gets run when the user selects ok in the login form
    def on_ok(self):
        # create an instance of the mail class
        # and attach it to the parentApp
        self.parentApp.mail = Mail(self.username.value,
                                    self.password.value)

    # this gets run when the user selects cancel on the login form.
    def on_cancel(self):
        self.parentApp.switchFormPrevious()
