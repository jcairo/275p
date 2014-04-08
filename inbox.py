import npyscreen
import pdb
import re
import mail_listener
import gmaillib
import imaplib2
import curses

# this is the screen used to show email data for any mailbox retrieved
class Inbox(npyscreen.FormBaseNew):
    def create(self):
        """
        THis is run like the __init__ method when
        we create a new class instance
        """
        # set mail check time
        self.keypress_timeout = 10

        # setup form attributes to hold message data
        self.inbox_messages = self.parentApp.mail.inbox()
        self.email_hdr_lst = []
        self.cursor_pos = 0

        # setup the message headers scroll box
        self.msg_headers = self.add(MultiLineActionAuto, columns=3,
             max_height=5)

        # set up main menu button
        def main_menu_button(*args):
            self.parentApp.switchForm("MAIN")

        # set up compse button
        def compose_button(*args):
            self.parentApp.REPLY = False
            self.parentApp.switchForm("COMPOSE_MAIL")

        # set up reply button
        def press_reply_button(*args):
            self.parentApp.REPLY = True
            self.parentApp.switchForm("COMPOSE_MAIL")
        
        
        def delete_button(*args):
            # get index of the currently selected email
            selected_msg_index = self.cursor_pos
            # get the uid of the mail 
            num_msgs = len(self.inbox_messages)
            # ensure the last message is not deleted.
            if num_msgs == 1:
                npyscreen.notify_ok_cancel("Can't delete last message in box")
                return
            # if we are deleting the last message show the body of the second
            # last message
                 
            msg_uid = self.inbox_messages[selected_msg_index].uid
            # call server to delete the msg with the specified id
            rv = self.parentApp.mail.delete_msg(msg_uid)
            if rv == 'OK':
                del self.email_hdr_lst[selected_msg_index]
                del self.inbox_messages[selected_msg_index]
                del self.msg_headers.msg_unread[selected_msg_index]
                # upate the indexes of the read and unread emails.
                self.msg_headers.update()
                # update the message body being displayed
                # if we delete the last message show the one above
                # otherwise show the one below
                if num_msgs == selected_msg_index + 1:
                    self.parentApp.INBOX_MSG_TXT = self.inbox_messages[selected_msg_index - 2].body
                else:
                    self.parentApp.INBOX_MSG_TXT = self.inbox_messages[selected_msg_index].body
                # update the display
                self.msg_body.value = self.parentApp.INBOX_MSG_TXT 
                self.msg_body.update()
            else:
                npyscreen.notify_confirm("Failed to delete")
            
        # set behavious or mark read button
        def mark_read_button(*args):
            # get index of the currently selected email
            selected_msg_index = self.cursor_pos
            # get the uid of the mail 
            msg_uid = self.inbox_messages[selected_msg_index].uid
            # call server to mark as read
            rv = self.parentApp.mail.mark_read(msg_uid)
            if rv == 'OK':
                self.inbox_messages[selected_msg_index].unread = False
                # update the mails image so its no longer highlighted in the mail list
                self.msg_headers.msg_unread[selected_msg_index] = False
                self.msg_headers.update()
            else:
                npyscreen.notify_confirm("Failed to mark as read")
        
        # place buttons on form
        self.reply_button = self.add(npyscreen.ButtonPress,
                                name="Reply")
        self.reply_button.whenPressed = press_reply_button
        self.mark_read = self.add(npyscreen.ButtonPress,
                                relx=12, rely = 7,
                                name="Mark Read")
        self.mark_read.whenPressed = mark_read_button
        self.delete = self.add(npyscreen.ButtonPress,
                                relx=26, rely = 7,
                                name="Delete")
        self.delete.whenPressed = delete_button
        self.menu = self.add(npyscreen.ButtonPress,
                                relx=36, rely = 7,
                                name="Main Menu")
        self.menu.whenPressed = main_menu_button

        self.compose = self.add(npyscreen.ButtonPress,
                                relx=50, rely = 7,
                                name="Compose New")
        self.compose.whenPressed = compose_button

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

    def new_mail(self, *args):
        # this gets called from the threaded mail checker process an event
        # unfortuneatly events can be all sorts of things like deleting a message
        # so before we actually can confirm we received new mail we need to check
        # whether a new piece of mail actually exists.
        new_msg = self.parentApp.mail.inbox(amount=1)[0]
        if new_msg.uid == self.inbox_messages[0].uid:
            # this means we don't actually have a new message
            return
        # append the new mail to the message list
        # get the header and append it to the header list
        npyscreen.notify_confirm("You've got mail")
        new_msg = self.parentApp.mail.inbox(amount=1)[0]
        # create the header and attach it to the form
        fmt_msg_hdr = "{0:<{width}.{width}} {1:<17.17} {2:<}".format(
            new_msg.sender_addr.split(' <')[0],
            new_msg.date, new_msg.subject, width=20)
        self.email_hdr_lst.insert(0, fmt_msg_hdr)
        self.msg_headers.values = self.email_hdr_lst
        self.inbox_messages.insert(0, new_msg)
        self.msg_headers.msg_unread.insert(0, True)
        # update the display
        self.msg_headers.update()
        self.msg_body.update()
   
    def while_waiting(self):
        # This method is overridden from the super class it is called when
        # the user is doing nothing so it is very resource light.
        # It provides a hook for the mail check thread to notify the main application
        # thread of new mail.
        # if we find an email we notify the user.
        if not self.parentApp.queue.empty():
            self.parentApp.queue.get()
            # call the get mail method to process new message
            self.new_mail()
        return

class MultiLineActionAuto(npyscreen.MultiLineAction):
    """
    Add ability to display the message body of the selected header
    and pass selection to the parent form for display in the lower
    portion of the form.
    """
    def when_cursor_moved(self):
        # perform the standard cursor moved routine
        super(MultiLineActionAuto, self).when_cursor_moved()

        # set the cursor position so we know which email we are on
        self.parent.cursor_pos = self.cursor_line
        # get the index of the email header currently selected
        msg_body = self.parent.inbox_messages[self.cursor_line].body

        # attach the relevant attributes for a response to the parent app
        # so they are accessible in the repy form.
        self.parent.parentApp.SENDER = self.parent.inbox_messages[self.cursor_line].sender_addr
        self.parent.parentApp.SUBJECT = self.parent.inbox_messages[self.cursor_line].subject
        self.parent.parentApp.INBOX_MSG_TXT = msg_body
        self.parent.parentApp.INBOX_CURRENTLY_SELECTED = self.cursor_line

        # force the widgets on the form to refresh
        self.parent.set_value(self.cursor_line) 

    def _before_print_lines(self):
        # list containing a True if unread False if read
        for msg in self.parent.inbox_messages:
            if msg.unread == True:
                self.msg_unread.append(True)
            else:
                self.msg_unread.append(False)
        return 

class MultiLineEditAuto(npyscreen.MultiLineEdit):
    """
    Add ability to display body of selected message in text field
    to the standard text display form.
    """
    def when_parent_changes_value(self):
        self.value = self.parent.parentApp.INBOX_MSG_TXT 
        self.display()

                
