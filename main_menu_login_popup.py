import npyscreen


# this is the login form.
class MainMenuPopup(npyscreen.ActionPopup):
    def create(self):
        self.username = self.add(npyscreen.TitleText, name="Oracle user:")
        self.username.value = 'djphan'
        self.password = self.add(npyscreen.TitlePassword, name="Password:")
        self.password.value = ''
        self.host = self.add(npyscreen.TitleText, name="Host:")
        self.host.value = "@gwynne.cs.ualberta.ca:1521/CRS"
    
    # this gets run when the user selects ok in the login form
    def on_ok(self):
        """
        try:
            self.parentApp.db = Database("%s/%s%s" % (self.username.value,
                                                      self.password.value,
                                                      self.host.value))
        except cx_Oracle.DatabaseError:
            self.parentApp.db = Database()
            self.parentApp.switchForm("MAIN_POPUP")
        else:
            self.parentApp.switchFormPrevious()
        """
    # this gets run when the user selects cancel on the login form.
    def on_cancel(self):
        self.parentApp.switchFormPrevious()


