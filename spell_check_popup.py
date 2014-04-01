import npyscreen

class SpellCheckPopup(npyscreen.ActionPopup):
    def create(self):
        self.word = self.add(npyscreen.TitleFixedText, name="Word", value = "sean")
        self.corrections = self.add(npyscreen.SpellChecker, name="")
        self.corrections = self.parentApp.getForm("COMPOSE_MAIL")
        #self.corrections.values = ["sean","is","cool"]

    # this gets run when the user selects ok in the login form
    def on_ok(self):
        # create an instance of the mail class
        # and attach it to the parentApp
        #self.parentApp.mail = Mail(self.username.value,
        #                           self.password.value)
        pass
    # this gets run when the user selects cancel on the login form.
    def on_cancel(self):
        self.parentApp.switchFormPrevious()
