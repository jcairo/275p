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
        self.cursor_pos = 0

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
        
        def delete_button(*args):
            # get index of the currently selected email
            selected_msg_index = self.cursor_pos
            # get the uid of the mail 
            msg_uid = self.inbox_messages[selected_msg_index].uid
            # call server to mark as read
            rv = self.parentApp.mail.delete_msg(msg_uid)
            if rv == 'OK':
                del self.email_hdr_lst[selected_msg_index]
                del self.inbox_messages[selected_msg_index]
                # upate the indexes of the read and unread emails.



                # delete the email from the headers list
                #email_hdrs_after_delete = []
                #email_hdrs_after_delete.append(self.email_hdr_lst[0:selected_msg_index])
                #email_hdrs_after_delete.append(self.email_hdr_lst[selected_msg_index + 1:])
                #self.email_hdr_lst = email_hdrs_after_delete
                ## delete the message from the list of inbox messages
                #inbox_msg_after_delete = []
                #inbox_after_delete.append(self.inbox_messages[0:selected_msg_index])
                #inbox_after_delete.append(self.inbox_messages[selected_msg_index + 1:])
                #self.inbox_messages = inbox_msg_after_delete
                # update the screen
                self.msg_headers.update()
            else:
                npyscreen.notify_confirm("Failed to mark as read")

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
                                relx=15, rely = 7,
                                name="Mark Read")
        self.mark_read.whenPressed = mark_read_button
        self.delete = self.add(npyscreen.ButtonPress,
                                relx=28, rely = 7,
                                name="Delete")
        self.delete.whenPressed = delete_button

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

    # all you need to do is add an unread flag to all the emails when
    # they are created in the gmaillib class and that should be enough
    # to have unread messages bolded.
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

                
