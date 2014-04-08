#!/usr/bin/python
from . import wgwidget    as widget
from . import npysGlobalOptions as GlobalOptions
import locale
import sys
import curses
import textwrap
import re
from functools import reduce
from wgeditmultiline import MultiLineEdit

class EmailComposeWidget(MultiLineEdit):
    """
    Inherited from  wgeditmultiline.py
    Added the abilty to undo and redo 
    Overridded Functions: when_value_edited
    Added key bindings: ctrl + u : undo, ctrl + y : redo 
    Added attributes: u_states and r_states
    """
    _SAFE_STRING_STRIPS_NL = False
    def __init__(self, screen, autowrap=True, slow_scroll=True, scroll_exit=True, value=None, **keywords):
        #Added additional attributes for track undo commands 
        self.u_states = []
        self.r_states = []
        self.value = value or ''
       
        super(EmailComposeWidget, self).__init__(screen, **keywords)
        
        #additional key bindings for undo and redo 
        self.add_handlers({
                "^U": self.h_undo_state,
                "^Y": self.h_redo_state
        })

    def when_value_edited(self):
        """
        Function gets called if the value of the widget changes
        
        Overrided to allow for saving the current state of the widget
        """
        self.save_state()
        self.parent.parentApp.message_save = self.value
        
    def save_state(self):
        """
        Append the widgets current value into u_states if it is
        different from the last entry in u_states. Will only
        allow 100 states to be saved, therefore 100 undo's
        """
        
        #If u_states is empty append the current value
        if len(self.u_states) == 0:
            self.u_states.append(self.value)
        #Otherwise check that the current value is not already the last 
        #entry in u_states
        elif self.value != self.u_states[-1]:
        #clear r_states whenever more text is added 
            self.r_states = []
            if len(self.u_states) > 100:
                self.u_states.pop(0)
            self.u_states.append(self.value)

    def h_undo_state(self, input):
        """
        Undo the current state by switching to previous state 
        """
        #checks that u_states is not empty then pops its last value into
        #r_states for redo method
        if self.u_states:
            self.r_states.append(self.u_states.pop())
            #again checks that u_states is not empty and sets the 
            #widgets value to last entry u_states
            if self.u_states:
                self.value = self.u_states[-1]
                #self.parent.parentApp.message_save = self.u_states[-1]
            #if u_states is empty then the previous state was blank
            else:
                self.value = ""
                
            #self.update(clear = False)
            self.CHECK_REDO = True
    def h_redo_state(self, input):
        """
        Redo the text the last undo undid if the r_states list has values 
        """
        #check that redo states exist, if true pop the last value 
        # r_states and append it to u_states and set the widgets value
        if self.r_states:
            self.u_states.append(self.r_states.pop())
            self.value = self.u_states[-1]
            #self.parent.parentApp.message_save = self.u_states[-1]
        


