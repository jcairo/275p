from .wgmultiline import MultiLineAction
import copy
from . import wgwidget       as widget
from . import wgtextbox      as textbox
import textwrap
import curses
from . import wgtitlefield   as titlefield
from . import fmPopup        as Popup
import weakref

class SpellChecker(MultiLineAction):
    """
    Inherits from npyscreen MultiLineAction class. This widget
    lets the user select a item from a list. If enter
    is pressed on a item the actionHighlighted function
    is called which saves the value of the item
    selected into a parentApp attribute. This widget
    is used in the spell_check_popup form.
    """
    OK_BUTTON_TEXT          = "REPLACE"
    CANCEL_BUTTON_TEXT      = "SKIP"    

    def __init__(self, *args, **keywords):
      
        self.allow_multi_action = False  
        super(SpellChecker, self).__init__(*args, **keywords)  

    #function is called when a user presses on the 
    # the items in the menu
    def actionHighlighted(self, act_on_this, key_press):
        self.value = act_on_this
        #store the selection to be used later and exit the user
        #from editing the widget
        self.parent.parentApp.spell_check_selection = act_on_this
        self.editing = False
        self.how_exited = True
    
    def h_act_on_highlighted(self, ch):
        return self.actionHighlighted(self.values[self.cursor_line], ch)

    def set_up_handlers(self):
        super(SpellChecker, self).set_up_handlers()
        self.handlers.update ( {
                    curses.ascii.NL:    self.h_act_on_highlighted,
                    ord('x'):           self.h_act_on_highlighted,
                    curses.ascii.SP:    self.h_act_on_highlighted,
                    } )

