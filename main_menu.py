import sys
import npyscreen

# this is the screen you are forwarded to on startup.
class MainMenu(npyscreen.FormBaseNew):
    def notify_not_logged_in(self):
        npyscreen.notify_confirm("Please log in first.", 
            title="Not Logged In", form_color='STANDOUT',
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
            try:
                if self.parentApp.mail:
                    self.parentApp.switchForm("COMPOSE_MAIL")
            except Exception as e:
                self.notify_not_logged_in()
                return

        def press_inbox_button(*args):
            try:
                if self.parentApp.mail:
                    self.parentApp.switchForm("INBOX")
            except Exception as e:
                self.notify_not_logged_in()
                return

        def press_quit_button(*args):
            try:
                if self.parentApp.mail:
                    self.mail.exit_server()
                    sys.exit(0)
            except Exception as e:
                sys.exit()

        # setup buttons..
        self.login_button = self.add(npyscreen.ButtonPress, 
            name="Gmail Login", color='CRITICAL')
        self.login_button.whenPressed = press_gmail_login

        self.compose_button = self.add(npyscreen.ButtonPress, 
            name="Compose New Mail")
        self.compose_button.whenPressed = press_compose_button

        self.inbox_button = self.add(npyscreen.ButtonPress, 
            name="Inbox")
        self.inbox_button.whenPressed = press_inbox_button

        self.quit = self.add(npyscreen.ButtonPress, 
            name="Quit")
        self.quit.whenPressed = press_quit_button
