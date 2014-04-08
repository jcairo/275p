import npyscreen
from edit_distance import edit_distance, spell_check, read_in_dict 
import pdb
import string
class SpellCheckPopup(npyscreen.ActionPopup):
    """
    Inherits from ActionPopup form. Popups when user presses spellcheck
    and allows user to either correct misspelt words or skip them.
    """
    OK_BUTTON_TEXT = "NEXT"
    CANCEL_BUTTON_TEXT = "REPLACE"

    def create(self):
        #add title and corrections widgets to form
        self.word = None
        self.title = self.add(npyscreen.TitleFixedText,name = "Word:", value = None)
        self.corrections = self.add(npyscreen.SpellChecker, values = [], name = "Corrections")
            
    #this is run before the application enters the edit loop
    def beforeEditing(self):
        #the index for finding which incorrect word to 
        #correct next
        self.index = self.parentApp.next_index
        #stores the email message as list 
        self.m_list = self.parentApp.message_save.split() 
        #stores unix shared british-english dictionary as a list
        self.dict = self.parentApp.english_dict
        #check to see it the dictionary file has been read
        #if not store as a attribute of the main application
        if not(self.dict):
            self.dict = read_in_dict('british-english')
            self.parentApp.english_dict = self.dict
        #if we have not searched the message for errors 
        #search it, otherwise set form inds attribut equal to parentApp index_list 
        if not(self.parentApp.index_list):
            self.inds = self.find_errors_index(self.m_list, self.dict)
            self.parentApp.index_list = self.inds
        else:
            self.inds = self.parentApp.index_list
        #grab the current word that needs to be corrected and 
        # the list of possible corrections
        self.word, self.corrections.values = self.run_spell_check()
        
        self.title.value = self.word.strip(string.punctuation)

    # this gets run when the user selects ok 
    def on_ok(self):
        """
        If the NEXT button is pressed skips to the next
        misspelled word without correcting  
        """
        #increment error index list index
        self.parentApp.next_index += 1
        
        #switches back to compose form if no words are left to check
        self.check_form_switch()
       
    # this gets run when the user selects cancel on the login form.
    def on_cancel(self):
        """
        If REPLACE button is pressed replaces misspelt word with
        the correctly spelled word selected by the user
        """
        self.parentApp.next_index += 1
        
        #first grab email message and user selection
        old_save = self.parentApp.message_save
        selection = self.parentApp.spell_check_selection
        #if user was forced to select "?" then spell_check did not 
        #find a correction therefore no replacement should be done
        #otherwise find if there is punctuation and replace the word
        if selection != "?":
            start, end = self.check_punctuation(self.word)
            new_message = old_save.replace(self.word,(start+selection+end), 1)            
            self.parentApp.message_save = new_message
               
        #switches back to compose form if no words are left to check
        self.check_form_switch()
         
    
    def check_form_switch(self):
        """
        Switches to previous form if there are not more words to spell check
        """
        if (not(self.m_list) or not(self.inds)
            or self.parentApp.next_index >= len(self.inds)
            or self.corrections == ["?"]):
            self.parentApp.next_index = 0
            self.parentApp.index_list = []
            self.parentApp.new_message_save = self.parentApp.message_save
            self.parentApp.switchFormPrevious()
        else:
            return False

    def find_errors_index(self, word_list, d):
        """
        Returns a list of indices corresponding to misspelt words
        in word_list
        """
        error_list = []
       
        for i, item in enumerate(word_list):
            #checks have reached the old message boundary of a reply message
            #if true then breaks, so we do not spell check the message
            #we are replying to 
            if item == ('-'*40):
                break
            tmp = item.strip(string.punctuation)
            if tmp not in d and tmp.lower() not in d:
                error_list.append(i)
        return error_list
    
    def find_corrections(self,word, d):
        """
        Returns a list of possible corrections for a misspelt word
        """
        p_end = '?!%"),:.;}]'
        p_start = '([{"'
        if word:
            tmp = word.strip(p_end+p_start)
            return spell_check(tmp, d)
        else:
            return []
      
    def check_punctuation(self, word):
        """
        Returns the starting and ending punctuation in
        word
        """
        p_end = '?!%"),:.;}]'
        p_start = '([{"'
        p = string.punctuation
        s = ""
        e = ""
        for i in p_start:
            if word.startswith(i):
                s = i
        for i in p_end:
            if word.endswith(i):
                e = i
        
        return s, e
        
    def run_spell_check(self):
        """
        Returns a word that needs to be corrected and a list of possible
        corrections based of the current self.index
        """
        #first checks cases where there are no words to correct in which
        #case we return special values
        if not(self.m_list):
            return "Nothing To Spell Check", ["None"]
        elif not(self.inds):
            return "You get a A+ for no errors!", ["A+"]
        elif self.parentApp.next_index >= len(self.inds):
            return "Spell Check Complete", ["Done"]
        #otherwise we grab the current incorrect word and its corrections  
        else:
            error = self.m_list[self.inds[self.index]]
            correction_list = self.find_corrections(error,self.dict)
            if correction_list:
                return error, correction_list
            #if the correction list is empty, then the spell_check
            # function did not return any corrections meeting 
            # the requirements and we return "?" 
            else:
                return error, ["?"]


