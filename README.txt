Todo's

1. handle deletes better, currently just shows next message.
    won't work if they delete last message in the list of messages.

2. 

3. 

Sean APPLICATION FORMS

compose_form:

Form inherits from the npyscreen ActionForm class. This form has a to, subject and message
feilds for composing emails. If we are replying to a message the
to and subject feilds get set with who we are replying to and reply subject. In
addtion the message we are replying to is appended to the message value with 
a dashed line separating it from the rest of the message.

spell_check_poup form:

Inherits from the npyscreen ActionPopup class. This form popups when user presses
the Spell Check button in the compose window.
Displays current misspelled word and list of corrections the user can choose 
from. The user can choose to either replace or skip the current word. This
form uses functions from edit_distance.py for doing spell_check.

sean ADDITIONAL APPLICATION WIDGETS
 
npyscreen/wgemailcomposewidget.py widget:

This widget inherits from the npyscreen MultiLineEdit class. This widget
lets us type and delete characters in a multiline Field. Extends superclass 
to allow undo and redo ability using key bindings ctrl + u (undo) and
ctrl + r (redo). The string typed into the widget is stored
in its value attribute. This widget is used in the compose form.

npyscreen/wgspellchecker.py widget:

This widget inherits from the npyscreen MultiLineAction class. Lets us select from 
list of items and saves the selection in a parentApp attribute. The list
of items is stored in the values attribute. This widget is used in the
spell_check_popup form.

sean MICCELANEOUS FILES

edit_distance.py file:

  Contains three functions:
    edit_distance(s1, s2): returns the min number of character 
    manipulations needed to turn s1 into s2. Uses three character
    manipulations with cost (insert: 1, replace: 2, delete: 1). 
    Recurrence relation used for edit_distance algorithm
    referenced from https://www.stanford.edu/class/cs124/lec/med.pdf
    (Dan Jurafsky, Stanford University)
	 
    read_in_dict(dictionary): reads in a list of words from 
    text file.
	 
    spell_check(word, d): returns a list of corrections from d for word. 
    Corrections must have a edit_distance(word, correction) < 5 and 
    start with the character and case.


british-english:

A txt file with ~99000 english words retrieved from UNIX usr/share/dict.
Used to check if a word is correctly spelled and generate a list 
of possible corrections for misspelled words.  

