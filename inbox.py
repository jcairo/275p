import npyscreen
import pdb
import re

# this is the screen used to show email data for any mailbox retrieved
class Inbox(npyscreen.FormBaseNew):
    def create(self):
        """
        THis is run like the __init__ method when
        we create a new class instance
        """
        # setup form attributes to hold message data
        self.inbox_messages = self.parentApp.mail.inbox()
        self.email_hdr_lst = []
        

        # setup the message headers scroll box
        self.msg_headers = self.add(MultiLineActionAuto, columns=3,
             max_height=5)
        # set up reply button
        def press_reply_button(*args):
            # get the currently highlighted email
            # attach the relevant data to the parent app
            # to forward over to the compose form.
            # determine the reply address
            self.parentApp.switchForm("COMPOSE_MAIL")

        self.reply_button = self.add(npyscreen.ButtonPress,
                                name="Reply")
        self.reply_button.whenPressed = press_reply_button

        # setup message body display
        self.msg_body = self.add(MultiLineEditAuto, name="Compose", 
                                height=16,
                                max_height=16, scroll_exit=True,
                                slow_scroll=True, exit_left=True, 
                                exit_right=True)

        # get a list of email headers from/date/subject

        # assemble header information for all messages in the
        # inbox_messages list
        self.inbox_messages.reverse()
        for message in self.inbox_messages:
            fmt_msg_hdr = "{0:<{width}.{width}} {1:<17.17} {2:<}".format(
                message.sender_addr.split(' <')[0],
                message.date, message.subject, width=20)
            self.email_hdr_lst.append(fmt_msg_hdr)

        # pass the list of headers to the widget to display
        self.msg_headers.values = self.email_hdr_lst

        # this is the variable which contains the message value held
        # in the box below the message headers field.
        self.msg_body.value = self.inbox_messages[0].body 
        

class MultiLineActionAuto(npyscreen.MultiLineAction):
    """
    Add ability to display the message body of the selected header
    and pass selection to the parent form for display in the lower
    portion of the form.
    """
    def when_cursor_moved(self):
        # perform the standard cursor moved routine
        super(MultiLineActionAuto, self).when_cursor_moved()

        # get the index of the email header currently selected
        msg_body = self.parent.inbox_messages[self.cursor_line].body
        self.parent.parentApp.SENDER = self.parent.inbox_messages[self.cursor_line].sender_addr
        self.parent.parentApp.SUBJECT = self.parent.inbox_messages[self.cursor_line].subject
        self.parent.parentApp.INBOX_MSG_TXT = msg_body
        self.parent.parentApp.INBOX_CURRENTLY_SELECTED = self.cursor_line
        self.parent.set_value(self.cursor_line) 

class MultiLineEditAuto(npyscreen.MultiLineEdit):
    """
    Add ability to display body of selected message in text field
    to the standard text display form.
    """
    def when_parent_changes_value(self):
        self.value = self.parent.parentApp.INBOX_MSG_TXT 
        self.display()
