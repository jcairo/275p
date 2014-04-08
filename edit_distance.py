import pdb
"""
Contains edit_distance, spell_check and read_in_file functions
"""
def edit_distance(s1, s2):
    """
    Gives the min number of character edits needed to convert string 1 to string two 
    The three operations with cost are:
    insert: 1
    delete: 1
    replace: 2
    
    Use a dynamic programming approach and calculate cost distance for small i and j 
    (s1[:i] and s2[:j]) first, and keep adding on the cost of additional character
    manipulations on string suffixes for incremental i's and j's. We know that 
    when one string is empty the cost is is easy to compute. For example if i = 0 and j = 1 
    the cost is 1 for one insertion. Or if i = 0 and j = 5 the cost is 5 for 
    5 insertions. With our inital values calculated we can compute the next by taking
    the min of getting there by either a insert, delete or replace. This makes a table
    of values with len(s1)+1 rows and len(s2)+1 columns and return value is in the 
    (len(s1) + 1, len(s2) +1) position
    
    Running Time Analysis: Outer for loop runs len(s1)+1 or n+1 many times and 
    the inner for loop runs len(s2)+1 or m+1 many times. Therefore this algorithm
    has a O(m*n) running time.

    Reccurance relation for edit_distance algorithm referenced from 
    https://www.stanford.edu/class/cs124/lec/med.pdf (Dan Jurafsky,
    Stanford University)

    #four insertions
    >>> edit_distance("", "Jean")
    4
    #four deletions
    >>> edit_distance("Jean", "")
    4
    #one replace
    >>> edit_distance("Sean", "Jean")
    2
    #one replace and one insert
    >>> edit_distance("Longer", "Longest")
    3
    #one replace and twelve inserts
    >>> edit_distance("R", "Understanding")
    14
    >>> edit_distance("Fling", "Glint")
    4
    >>> edit_distance("zzebglmnop", "zeebra")
    10
    """
    
    #memoization table for storing edit_distances 
    #distance[(i,j)] holds the min edit_distance  for converting
    #the slice s1[:i] to s2[:j]
    distance = {}
    
    #function for deciding the cost of replace 
    def replace(i, j):
        #characters are equal, zero cost to replace
        if s1[i] == s2[j]: 
            return 0 
        else: 
            return 2
   
    #run through characters in s1 
    for i in range(0,len(s1)+1):
        #run through characters in s2
        for j in range(0,len(s2)+1): 
            if j == 0:
                distance[(i,j)] = i 
            elif i == 0:
                distance[(i,j)] = j
            else:
                #calculates the distance for each operation using memoized values and takes min 
                distance[(i,j)] = min(
                    #we inserted s2[j] onto the end of s1
                    #so we add 1 to the distance[(i,j-1)] to get the cost at (i,j).
                    distance[(i,j-1)] + 1, #insert
                    #if we delete s1[i] then we add 1 to distance[(i-1,j)]
                    distance[(i-1,j)] + 1, #delete
                    #if we replace s1[i] with s2[j] then we 
                    # add 2 to distance[(i-1,j-1)] to get cost at (i,j). If s1[i] is 
                    #equal to s2[j] we add 0 as we do not have to replace
                    distance[(i-1,j-1)] + replace(i-1,j-1) #replace
                    )

    #the final value stored is the value we return as it represents the 
    # cost of make s1 equal to s2
    return distance[(i,j)]
                
def read_in_dict(dictionary):
    """
    reads in a file line by line into a list, exluding new line characters
    """
    with open(dictionary, "r") as english_dict:
        d =[line[:-1] for line in english_dict]
    return d


def spell_check(word, d):
    """
    Takes a word and dict_file and returns a list of the 
    words with minimum edit distance
    """

    possible_corrections = {}
    c_list = []
    
    #words with non alphabet characters (excluding punctuation) 
    #are not corrected
    if not(word[0].isalpha()):
        c_list.append("?")
        return c_list

    distance = 100
    
    
    #loop through each item in dictionary
    for line in d:
        #ignore single characters besides "I"
        if len(line) == 1 and line != "I":
            continue
        #ignore words that do not have the same first character 
        #with the same case
        if (word[0].upper() == line[0].upper()
            and len(line) <= len(word)+1
            and ((word[0].isupper() and line[0].isupper())
                 or (word[0].islower() and line[0].islower()))):
            
            distance = edit_distance(word,line)

            #if the distance is less than 5 append the correction to c_list         
            if(distance < 5): 
                possible_corrections[line] = distance
                c_list.append(line)
           
    return c_list
                
    
    
    
    
    
