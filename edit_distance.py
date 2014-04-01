#import pd

def edit_distance(s1, s2):
    """
    Gives the min "distance" needed to convert string 1 to string two 
    The three operations with cost are:
    insert: 1
    delete: 1
    replace: 2

    >>> edit_distance("Sean", "Jean")
    2
    >>> edit_distance("Longer", "Longest")
    3
    >>> edit_distance("R", "Understanding")
    14
    >>> edit_distance("Fling", "Glint")
    4
    >>> edit_distance("zzebglmnop", "zeebra")
    10
    """
    #memoization
    distance = {}
    
    #function for deciding the cost of replace 
    def replace(i, j):
        #characters are equal, zero cost to replace
        if s1[i] == s2[j]: 
            return 0 
        else: 
            return 2
    
    #run through i positions in s1, i = 0 means no string
    #for example if i == 0 and j == 1  distance[(i,j)] == 1
    # implying that we just have to insert s2[j] into the 
    # empty s1[i]
    for i in range(0,len(s1)+1):
        #run through j positions in s2
        for j in range(0,len(s2)+1): 
            if j == 0:
                distance[(i,j)] = i
            elif i == 0:
                distance[(i,j)] = j
            else:
                #calculates the distance for each operation and takes min  
                distance[(i,j)] = min(
                    distance[(i,j-1)] + 1, #insert
                    distance[(i-1,j)] + 1, #delete
                    distance[(i-1,j-1)] + replace(i-1,j-1) #replace
                    )

              
    return distance[(i,j)]
                

def spell_check(word, dict_file):
    """
    Takes a word and dict_file and returns False if the 
    word is spelled correctly, otherwise it returns a tuple of the top 
    words with minimum edit distance
    
    >>> spell_check(Sean, "british_english.txt")
    True

    """

    possible_corrections = {}
    
    with open(dict_file, "r") as english_dict:
        for line in english_dict:
            if line[:-1] == word:
                return False
            else:
                #if word[0].upper() == line[0].upper()\
                #and  len(line[:-1])/3 <= len(line[:-1]) <= len(word):
                distance = edit_distance(word,line)

                if(distance < 5): 
                    possible_corrections[line[:-1]] = distance
    
    return possible_corrections
                
    
    
    
    
    
