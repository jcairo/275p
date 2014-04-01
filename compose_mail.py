import npyscreen
import pdb
import re

class ComposeMail(npyscreen.ActionForm):
    def create(self):
        def send_button_press():
            try:
                # parse the address out of the "To" field
                parsed_to = re.search(r'<.*>', self.to.value)
                # check whether we get a properly formatted address
                if parsed_to.group() == None:
                    to = self.to.value.strip('<>')
                else:
                    to = parsed_to.group().strip('<>')
                subj = self.subject.value
                body = self.message.value
                self.parentApp.mail.send(to, subj, body)  
            except Exception as e:
                npyscreen.notify_confirm(str(e),
                                    title="Mail error",
                                    form_color='STANDOUT',
                                    wrap=True, wide=False, editw=1)
                return    
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
        # to reply to a message prefill the details To and subject.
        try:
            self.to.value = self.parentApp.SENDER
            self.subject.value = "RE: " + self.parentApp.SUBJECT 
            self.message.value = ('\n' * 8) + \
                                    ('-' * 40) + \
                                    ('\n' * 2) + \
                                    self.parentApp.INBOX_MSG_TXT 
        except Exception as e:
            pass

        # set the message body a few lines below
        self.nextrely+=2
        self.nextrelx+=3
        #self.query_confirm = self.add(npyscreen.ButtonPress, 
            #name="Send", relx=70)

       
        
    
    def on_ok(self):
        self.parentApp.switchFormPrevious()
