import imaplib
import npyscreen
import re


class Mail():
    """
    The gmail class defines a gmail object
    """
    def __init__(self, username, password):
        try:
            self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
            self.mail.login(username, password)
        except imaplib.IMAP4.error:
            # wrap failure message in a popup.
            print("login failure")

        def get_mailboxes(self):
            # if we get a connection figure out what
            # mailboxes we have in the acct.
            rv, self.mailboxes = self.mail.list()
            if rv == 'OK':
                for mailbox in self.mailboxes:
                    # convert the byte array to a string
                    str_mailbox = str(mailbox)

                    # get the name should be between the last 2 qoutes.

        # define functions for email access below.
