import npyscreen
import pdb
import re

class ComposeMail(npyscreen.ActionForm):
    def create(self):
        def send_button_press():
            # regex courtesy of http://www.webmonkey.com
            #/2008/08/four_regular_expressions_to_check_email_addresses/
            # parse the address out of the "To" field
            parsed_to = re.search('.+\@.+\..+', self.to.value)
            try:
                to = parsed_to.group().strip(' <>')
            except Exception as e:
                npyscreen.notify_confirm(str(e), title="Mail error",
                                    form_color='STANDOUT',
                                    wrap=True, wide=False, editw=1)
                return    

            subj = self.subject.value
            body = self.message.value
            
            #replace '\n' with '\r\n' to match content-type: text/plain
            #for sending and recieving emails
            body = re.sub('\n','\r\n',body)
                  
            self.parentApp.mail.send(to, subj, body)  

            npyscreen.notify_confirm("Mail sent",
                                    title="Send Confirmation",
                                    form_color='STANDOUT',
                                    wrap=True, wide=False, editw=1)
            self.parentApp.switchForm("INBOX") 


        self.to = self.add(npyscreen.TitleText, name="To: ")
       
        self.subject = self.add(npyscreen.TitleText, 
                                   name="Subject:",
                                   use_two_lines=False, 
                                   field_width=54)
        self.send_button = self.add(npyscreen.ButtonPress,
                                name="Send")
        self.send_button.whenPressed = send_button_press
        self.message = self.add(npyscreen.EmailComposeWidget, 
                                name="Compose", 
                                height=16,
                                max_height=16, scroll_exit=True,
                                slow_scroll=True, exit_left=True, 
                                exit_right=True)

        
        # if we have been forwarded here from the inbox page
        # to reply to a message prefill the details form with
        # from/to/message.
                

        # set the message body a few lines below
        self.nextrely+=2
        self.nextrelx+=3
        #self.query_confirm = self.add(npyscreen.ButtonPress, 
            #name="Send", relx=70)

    def beforeEditing(self):
        if self.parentApp.REPLY:
            try:
                self.to.value = self.parentApp.SENDER
                self.subject.value = "RE: " + self.parentApp.SUBJECT 

                self.message.value = ('\n' * 2) + \
                                        ('-' * 40) + \
                                        ('\n' * 2) + \
                                        ('From: ' + self.parentApp.SENDER) + \
                                        ('\n') + \
                                        self.parentApp.INBOX_MSG_TXT 
            except Exception as e:
                pass
        else:
            # clear all form fields.
            self.to.value = ''
            self.subject.value = ''
            self.message.value = ''


        # check reply flad to see whether we are replying to a message
        # or composing a new one.
        #Set message.value if we have a value stored in parentApp attribute
        if self.parentApp.message_save:
            self.message.value = self.parentApp.message_save
            self.message.save_state()
        #set to and subject values if they exist
        if not(self.to.value) and self.parentApp.email_to:
            self.to.value = self.parentApp.email_to
        if not(self.subject.value) and self.parentApp.email_subject:
            self.subject.value = self.parentApp.email_subject

    def afterEditing(self):
        #stores value of from and subject into parentApp attributes 
        #for reference 
        if self.to.value:
            self.parentApp.email_to = self.to.value
        if self.subject.value:
            self.parentApp.email_subject = self.subject.value
        self.parentApp.REPLY = False    
        
    def on_ok(self):
        self.parentApp.REPLY = False
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchForm("SPELL_CHECK_POPUP")
