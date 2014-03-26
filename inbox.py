import npyscreen
import pdb

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
        self.grid = self.add(MultiLineActionAuto, columns=3,
             max_height=5)
        
        # get a list of email headers from/date/subject
        # pdb.set_trace()
        inbox_messages = self.parentApp.mail.inbox()
        email_hdr_lst = []
        for message in inbox_messages:
            email_hdr_lst.append(message.sender_addr + message.date + 
                message.subject)

        self.grid.values = email_hdr_lst

        self.results = self.add(npyscreen.MultiLineEdit, name="Compose", 
                                height=16,
                                max_height=16, scroll_exit=True,
                                slow_scroll=True, exit_left=True, 
                                exit_right=True)

        # this is the variable which contains the message value held
        # in the box below the message headers field.
        # self.results.value = inbox_messages[0].body 
        
        # you need an on select/move method which will 
        # get the selected value, determine which email it is
        # and print it's body to the message field.

        def set_message_body(self, message_index):
            self.results.value = message_body 


class MultiLineActionAuto(npyscreen.MultiLineAction):
    """
    This class customizes the widget that displays the email headers
    to allow it to display the message body of the selected header
    """
    def when_cursor_moved(self):
        # do the standard cursor moved routine
        super(MultiLineActionAuto, self).when_cursor_moved()
        # in addition
        # get the index from the list as to which email we are on
        message_index = self.cursor_line
        self.parentApp.Inbox.results.set_message_body(message_index)
        # use this value to display the body of the message that is
        # highlighted
        #print self.cursor_line


