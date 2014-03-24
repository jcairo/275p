import email
import imaplib
import npyscreen
import re
import pdb

class Mail():
    """
    The gmail class defines a gmail connection object
    """
    def __init__(self, username, password):
        # try to establish a connection based on the user credentials
        self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
        try:
            self.mail.login(username, password)
        except imaplib.IMAP4.error:
            # raise login failure message in a popup.
            raise KeyError

    def get_mail(self, mailbox_name):
        """
        Returns a dictionary of email data
        based on most recent mail but mail id's are relative to
        the beginning of the inbox so they are not unique.
        """
        # create an empty list to populate with mail
        msg_dict = {}
        #try:
        self.mail.select(mailbox_name, readonly=True) 
        rv, data = self.mail.search(None, 'ALL')
        msg_lst = data[0].split()
        for msg in msg_lst:
            pdb.set_trace()
            # each uid is a bytearray, cast to str for each mail fetch
            rv, msg_data = self.mail.fetch(str(int(msg)), '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])

            # check if the message has a subject
            if 'subject' not in msg.keys():
                msg['subject'] = 'No subject'
            # print the message to the console and append to list
            print(msg['from'] + msg['subject'] + msg['date'])
            msg_dict[msg] = msg['from'] + msg['subject'] + msg['date']
        #except:
            #pass

        # return the list of parsed header strings
        return message_header_list

    def get_mail_uid(self, mailbox_name):
        """
        Returns a list of email header data (from/time/subject)
        based on Unique mail id's
        """
        # create an empty list to populate with mail
        message_header_list = []
        #try:
        self.mail.select(mailbox_name, readonly=True) 
        # get a list of unique mail id numbers.
        rv, data = self.mail.uid('search', None, 'ALL')
        uid_lst = data[0].split()
        # iterate through reversed list since newest come last
        for uid in reversed(uid_lst):
            #pdb.set_trace()
            # each uid is a bytearray, cast to str for each mail fetch
            rv, msg_data = self.mail.uid('fetch', str(int(uid)), '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])

            # check if the message has a subject, if not set a default
            if 'subject' not in msg.keys():
                msg['subject'] = 'No subject'

            # print the message to the console and append to list
            # print(msg['from'] + msg['subject'] + msg['date'])
            message_header_list.append(msg['from'] + msg['subject'] +
                msg['date'])
        #except:
            #pass

        # return the list of parsed header strings
        return message_header_list


        

        def get_mailbox_data(self):
            """
            return data for inbox
            """
            # determine top level mailboxes in the acct.
            rv, self.raw_mailboxes=  self.mail.list()
            if rv == 'OK':
                # get byte array of mailbox names
                # create a list of all mailbox names
                self.mailboxes = []
                for mailbox in self.raw_mailboxes:
                    # convert the byte array to a string
                    mailbox_raw_str = str(mailbox)
                    # get the name should be between the last 2 qoutes.

            pass
        # define functions for email access below.
