import imaplib2
import smtplib
import email
import os
import time
import datetime
import re
import pdb
import mail_listener
import Queue

# gmaillib is an imap library and was found here:
# https://github.com/thedjpetersen/gmaillib
# although we have used much of its basic structure
# we added the ability to store the state of eacah email
# read/unread and store a unique message id on each email.
# we also added the ability for the account class which
# manages the gmail connections to create a threaded object
# which is an event listener on the gmail server.


#THE MESSAGE CLASS

#PROPERTIES OF A MESSAGE:

#1. parsed_email
#2. reciever_addr -- email address of the reciever
#3. sender_addr -- email address of the sender
#4. date -- date that the message was sent
#5. subject -- subject of the email
#6. body -- content of the email
#7. uid -- unique message id
#8. message unread/read
class message:
    def __init__(self, fetched_email, uid=None, unread=None):
        accepted_types = ['text/plain']
        parsed = email.message_from_string(fetched_email)
        self.parsed_email = email.message_from_string(fetched_email)
        self.receiver_addr = parsed['to']
        self.sender_addr = parsed['from']
        self.uid = uid
        # conditionally set this.
        self.unread = unread

        # handle times which are of the same day as today
        self.date = parsed['date']

        """
        self.date_hdr_fmt = email.utils.parsedate(self.date)
        self.date_hdr_fmt = time.mktime(self.date_hdr_fmt)
        # local_time = time.localtime(time.time()) 
        # self.date_hdr_fmt = time.mktime(self.date_hdr_fmt[:-1]) - \
            # self.date_hdr_fmt[-1] - (7 * 60)

        if local_time[0] == self.date_hdr_fmt[0] and\
            local_time[1] == self.date_hdr_fmt[1] and\
            local_time[2] == self.date_hdr_fmt[2]:
                # format the time as a hourly time
                self.date_hdr_fmt = datetime.fromtimestamp(mktime(self.date_hdr_fmt))
        """

        self.subject = parsed['subject']
        self.body = ''
        if parsed.is_multipart():
            for part in parsed.walk():
                if part.get_content_type() in accepted_types:
                    self.body = part.get_payload()
        else:
            if parsed.get_content_type() in accepted_types:
                self.body = parsed.get_payload()

    def __repr__(self):
        return "<Msg from: {0}>".format(self.sender_addr)

    def __str__(self):
        return "To: {0}\nFrom: {1}\nDate: {2}\nSubject: {3}\n\n{4}".format(
            self.receiver_addr, self.sender_addr, self.date, self.subject, self.body)

    def download_attachment(self, dest_dir):
        '''
        Courtsey of http://stackoverflow.com/questions/348630/how-can-i-download-all-emails-with-attachments-from-gmail
        '''
        mail = self.parsed_email
        if mail.get_content_maintype() != 'multipart':
            return "no attachment"

        print "["+ mail["From"]+"] :" + mail["Subject"]

        for part in mail.walk():
            if part.get_content_maintype() == 'multipart':
                continue
 
            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename()
            counter = 1

            if not filename:
                filename = 'part-%03d%s' % (counter, 'bin')
                counter += 1

            att_path = os.path.join(dest_dir, filename)

            if not os.path.isfile(att_path) :
                fp = open(att_path, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
                
#THE ACCOUNT CLASS

#THE PROPERTIED OF THE ACOUNT CLASS

#1. username -- username of the account
#2. password -- password associated with the account

class account:
    def __init__(self, username, password, parent=None, queue=None):
        self.parent = parent
        self.username = username
        self.password = password

        # attach communication queue to account instance
        # this is how we will communicate with the subthread.
        self.queue = queue

        # create smtp instance for sending messages.
        self.sendserver = smtplib.SMTP('smtp.gmail.com:587')
        self.sendserver.starttls()
        self.sendserver.login(username,password)

        self.receiveserver = imaplib2.IMAP4_SSL('imap.gmail.com', 993)
        self.receiveserver.login(username,password)

        self.listen_server = imaplib2.IMAP4_SSL('imap.gmail.com', 993)
        self.listen_server.login(username, password)
        # initiate listening for incoming mail using threaded process
        self.listen_server.select("INBOX") 
        self.idler = mail_listener.Idler(self.listen_server, self.queue, parent=self)
        self.idler.start()
        
    def exit_server(self):
        # shut down all connections and processes.
        self.idler.stop()
        self.idler.join(10)
        self.idler.exit()
        self.sendserver.quit()
        self.listen_server.close()
        self.listen_server.logout()
        self.receiveserver.close()
        self.receiveserver.logout()

    def send(self, toaddr, subject='', msg=''):
        fromaddr = self.username
        headers = ["From: " + fromaddr,
               "Subject: " + subject,
                   "To: " + toaddr,
                   "MIME-Version: 1.0",
                   "Content-Type: text/plain"]
        headers = "\r\n".join(headers)
        self.sendserver.sendmail(fromaddr, toaddr, headers + "\r\n\r\n" + msg)

    def receive(self):
        return

    def filter(self, search_string):
        '''
        This function provides gmail style search.

        @type search_string: string
        @param search_string: GMail style search string

        @return list of email matching the search criteria
        
        '''
        
        self.receiveserver.select("Inbox")
        fetch_str = self.receiveserver.uid('SEARCH', None, 'X-GM-RAW', search_string)[1][0]
        fetch_list = fetch_str.split(' ')
        emails = []
        for email_index in fetch_list:
            emails.append(self.get_email(email_index))
        return emails

    def get_all_messages(self):
        self.receiveserver.select('Inbox')
        fetch_list = self.receiveserver.search(None, '(UNDELETED)')[1][0]
        fetch_list = fetch_list.split(' ')
        inbox_emails = []
        for each_email in fetch_list:
            inbox_emails.append(self.get_email(each_email))
        return inbox_emails

    def unread(self):
        self.receiveserver.select('Inbox')
        fetch_list = self.receiveserver.search(None,'(BODY.PEEK[HEADER])')[1][0]
        fetch_list = fetch_list.split(' ')
        if fetch_list == ['']:
            return []
        unread_emails = []
        for each_email in fetch_list:
            unread_emails.append(self.get_email(each_email))
        return unread_emails

    def get_email(self, email_id):
        self.receiveserver.select('Inbox')
        fetched_email = self.receiveserver.fetch(email_id, "(RFC822)")[1][0][1]
        parsed_email = message(fetched_email)
        return parsed_email
    
    def mark_read(self, uid):
        """
        Takes an email id and marks it as read on the server
        """
        ## send mark read request.
        typ, response = self.receiveserver.uid('STORE', uid, '+FLAGS', '\Seen') 
        return typ

    def delete_msg(self, uid):
        """
        Takes a message id number and deletes it from the server
        """
        #response = self.receiveserver.uid('COPY', uid, '[Gmail]/Trash')
        #if response[0] == 'OK':
        typ, response = self.receiveserver.uid('STORE', uid, '+FLAGS', '\\Deleted')
        # move the message to the trash
        return typ

    def inbox(self, start=0, amount=10):
        # select the message inbox
        self.receiveserver.select('Inbox')
        # create an empty list
        inbox_emails = []
        # get a list of messages
        messages_to_fetch = ','.join(self._get_uids()[start:start+amount])
        fetch_list = self.receiveserver.uid('fetch', messages_to_fetch,
            '(BODY.PEEK[] FLAGS)')
        for each_email in fetch_list[1]:
            if(len(each_email) == 1):
                continue
            # get the uid and pass it to the message class
            uid_id, uid = re.search(r'UID [0-9]*', each_email[0]).group().split()
            # check whether the message has been read
            if each_email[0].find('\\Seen') >= 0:
                unread = False
            else:
                unread = True
            inbox_emails.append(message(each_email[1], uid, unread=unread))
        return inbox_emails

    def get_inbox_count(self):
        return int(self.receiveserver.select('Inbox')[1][0])

    def _get_uids(self):
        self.receiveserver.select('Inbox')
        result, data = self.receiveserver.uid('search', None, 'ALL')
        data = data[0].split(' ')
        data.reverse()
        return data

# test script not used in application.
if __name__ == "__main__":
    mail = account('joncairo', 'Carrma123')
    mail.inbox()
    uids = mail._get_uids()
    for i in range(10):
        result, data = mail.receiveserver.uid('fetch', uids[i], '(FLAGS)')
        print result
        print data
    messages = mail.inbox()
    for message in messages:
        print message.uid, message.sender_addr
