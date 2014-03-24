import npyscreen

# this is the screen used to show email data for any mailbox retrieved
class Inbox(npyscreen.FormBaseNew):
    def create(self):
        """
        THis is run like the __init__ method when
        we create a new class instance
        """
        # when we enter this form we want to make a 
        # request to the mailbox object to return us a list of
        # messages in the specified box. 
        # since we are starting with just the inbox we will
        # hardcode the call as an "Inbox" request but later
        # we can modify this by allowing the user to select
        # which box they want to see


        # setup the grid
        self.grid = self.add(npyscreen.MultiLine, columns=3,
             max_height=5)
        
        # get a list of email headers from/date/subject
        email_hdr_lst = self.parentApp.mail.get_mail_uid("INBOX")
        self.grid.values = email_hdr_lst

        self.results = self.add(npyscreen.MultiLineEdit, name="Compose", 
                                height=16,
                                max_height=16, scroll_exit=True,
                                slow_scroll=True, exit_left=True, 
                                exit_right=True)
        self.results.value = "message" 
