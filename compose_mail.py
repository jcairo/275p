import npyscreen
import pdb
import re

class ComposeMail(npyscreen.ActionForm):
    """
    Compose form inherits from npyscreen ActionForm class. Includes a to, subj and 
    message widget for composing emails. Includes three buttons: Send, Spell Check
    and Back. If user was sent to the compose form by pressing reply in the inbox 
    form, then the to and subject widgets values get set. In addition the message 
    the user is replying to is appended onto the messege widgets value seperated
    by a dashed line. If we are coming back from doing a spellcheck then the to
    and subj values remain the same and the corrected message value is used.
    Otherwise the forms feilds are set to empty strings 
    """
    OK_BUTTON_TEXT          = ""
    CANCEL_BUTTON_TEXT      = ""   
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

        def press_spell_check(*args):
            #switch to spell check form 
            #set spell check flag to true so that we know 
            #we have done a spell check when we go back to 
            #compose form
            self.parentApp.SPELLCHECK = True
            self.parentApp.switchForm("SPELL_CHECK_POPUP")

        def press_back(*args):
            #switch back to compose window
            self.parentApp.REPLY = False
            self.parentApp.switchFormPrevious()

        self.to = self.add(npyscreen.TitleText, name="To: ")
       
        self.subject = self.add(npyscreen.TitleText, 
                                   name="Subject:",
                                   use_two_lines=False, 
                                   field_width=54)
        #form buttons
        self.send_button = self.add(npyscreen.ButtonPress,
                                name="Send")
        self.spell_check_button = self.add(npyscreen.ButtonPress,
                                    name="Spell Check", relx = 9, rely = 4)
        self.back_button = self.add(npyscreen.ButtonPress,
                                    name="Back", relx = 22, rely = 4)
        #button press actions
        self.send_button.whenPressed = send_button_press
        self.spell_check_button.whenPressed = press_spell_check
        self.back_button.whenPressed = press_back

        self.message = self.add(npyscreen.EmailComposeWidget, 
                                name="Compose", 
                                height=16,
                                max_height=16, scroll_exit=True,
                                slow_scroll=True, exit_left=True, 
                                exit_right=True)

        
        # set the message body a few lines below
        self.nextrely+=2
        self.nextrelx+=3
        #self.query_confirm = self.add(npyscreen.ButtonPress, 
            #name="Send", relx=70)
        
    #function is called before edit loop
    def beforeEditing(self):
        # check reply flag to see whether we are replying to a message
        # or composing a new one.
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
            #check SPELLCHECK flag to see if we were just
            #doing spell check. If so keep the same from and subj
            #values as we had before pressing spell check button
            if self.parentApp.SPELLCHECK:
                if self.parentApp.message_save:
                    self.message.value = self.parentApp.message_save
                if not(self.to.value) and self.parentApp.email_to:
                    self.to.value = self.parentApp.email_to
                if not(self.subject.value) and self.parentApp.email_subject:
                    self.subject.value = self.parentApp.email_subject
            else:
                # clear all form fields.
                self.to.value = ''
                self.subject.value = ''
                self.message.value = ''


   
        #spell check flag is set to false
        self.parentApp.SPELLCHECK = False

    #function is called after edit loop
    def afterEditing(self):
        #stores value of from and subject into parentApp attributes 
        #for reference 
        if self.to.value:
            self.parentApp.email_to = self.to.value
        if self.subject.value:
            self.parentApp.email_subject = self.subject.value
        self.parentApp.REPLY = False    
       
        
   
