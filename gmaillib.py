import imaplib
import smtplib
import email
import os
import time
import datetime
import re
import pdb
#THE MESSAGE CLASS

#PROPERTIES OF A MESSAGE:

#1. parsed_email
#2. reciever_addr -- email address of the reciever
#3. sender_addr -- email address of the sender
#4. date -- date that the message was sent
#5. subject -- subject of the email
#6. body -- content of the email

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


#clarification reqd on the following two items:
#3. sendserver
#4. receiveserver

class account:
    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.sendserver = smtplib.SMTP('smtp.gmail.com:587')
        self.sendserver.starttls()
        self.sendserver.login(username,password)

        self.receiveserver = imaplib.IMAP4_SSL('imap.gmail.com', 993)
        self.receiveserver.login(username,password)

    def exit_server(self):
        self.sendserver.quit()
        self.receiveserver.close()
        self.receiveserver.logout()

    def send(self, toaddr, subject='', msg=''):
        fromaddr = self.username

        headers = ["From: " + fromaddr,
               "Subject: " + subject,
                   "To: " + toaddr,
                   "MIME-Version: 1.0",
                   "Content-Type: text/html"]
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
        
        # NOTE: Gmail's advanced search is limited by the mail box selection
        # irrespective of what we include in the search string.
        # e.g. label:anywhere will return Inbox results only.

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
        #fetch_list = self.receiveserver.search(None,'UnSeen')[1][0]
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
        #This nasty syntax fetches the email as a string
        fetched_email = self.receiveserver.fetch(email_id, "(RFC822)")[1][0][1]
        parsed_email = message(fetched_email)
        return parsed_email
    
    def create_mailbox(self,mailbox):
        self.receiveserver.create(mailbox)

    def append(self,mailbox, flags, date_time, message):
        self.receiveserver.append(mailbox, flags, date_time, message)

    def inbox(self, start=0, amount=10):
        self.receiveserver.select('Inbox')
        inbox_emails = []
        messages_to_fetch = ','.join(self._get_uids()[start:start+amount])
        fetch_list = self.receiveserver.uid('fetch', messages_to_fetch,
            '(BODY.PEEK[] FLAGS)')
        for each_email in fetch_list[1]:
            if(len(each_email) == 1):
                continue
            # get the uid and pass it to the message class
            uid_id, uid = re.search(r'UID [1-9]*', each_email[0]).group().split()
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
