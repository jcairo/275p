import npyscreen
import pdb

class ComposeMail(npyscreen.ActionFormCarl):
    def create(self):
        self.from_ = self.add(npyscreen.TitleText, name="From: ")
        self.to_ = self.add(npyscreen.TitleText, name="To: ")

        # NOTE: When an entry is selected, the value of 
        #self.chooser.value will
        # be a list containing the index of the 
        # entry in the above list - in
        # this example, [0] or [1]. If nothing is selected, 
        # self.chooser.value
        # will be [].

        self.subject = self.add(npyscreen.TitleText, 
                                   name="Subject:",
                                   use_two_lines=False, 
                                   field_width=54)
        
        # set the message body a few lines below
        self.nextrely+=2
        self.nextrelx+=3
        #self.query_confirm = self.add(npyscreen.ButtonPress, 
            #name="Send", relx=70)

        self.results = self.add(npyscreen.MultiLineEdit, name="Compose", 
                                height=16,
                                max_height=16, scroll_exit=True,
                                slow_scroll=True, exit_left=True, 
                                exit_right=True)
        
    def on_ok(self):
        self.parentApp.switchFormPrevious()
