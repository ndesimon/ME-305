''' @file           morseCode.py
    @brief          Provides Morse Code patterns
    @details        Contains a wordBank and codeBank along with functions to
                    be called in the simonSays class
    @author         Nick De Simone
    @date           4/9/21
    @copyright      License Info Here
'''

import random

# List of all possible characters to be used in the Simon Says game
wordBank = [' ', 
"'", 
'(', 
')', 
',', 
'-', 
'.', 
'/', 
'0', 
'1', 
'2', 
'3', 
'4', 
'5', 
'6', 
'7', 
'8', 
'9', 
':', 
';', 
'?', 
'A', 
'B', 
'C', 
'D', 
'E', 
'F', 
'G', 
'H', 
'I', 
'J', 
'K', 
'L', 
'M', 
'N', 
'O', 
'P', 
'Q', 
'R', 
'S', 
'T', 
'U', 
'V', 
'W', 
'X', 
'Y',
'Z', 
'_']

# Dictionary of all keyboard characters and their Morse equivalents
codeBank = {' ': '_', 
"'": '.----.', 
'(': '-.--.-', 
')': '-.--.-', 
',': '--..--', 
'-': '-....-', 
'.': '.-.-.-', 
'/': '-..-.', 
'0': '-----', 
'1': '.----', 
'2': '..---', 
'3': '...--', 
'4': '....-', 
'5': '.....', 
'6': '-....', 
'7': '--...', 
'8': '---..', 
'9': '----.', 
':': '---...', 
';': '-.-.-.', 
'?': '..--..', 
'A': '.-', 
'B': '-...', 
'C': '-.-.', 
'D': '-..', 
'E': '.', 
'F': '..-.', 
'G': '--.', 
'H': '....', 
'I': '..', 
'J': '.---', 
'K': '-.-', 
'L': '.-..', 
'M': '--', 
'N': '-.', 
'O': '---', 
'P': '.--.', 
'Q': '--.-', 
'R': '.-.', 
'S': '...', 
'T': '-', 
'U': '..-', 
'V': '...-', 
'W': '.--', 
'X': '-..-', 
'Y': '-.--', 
'Z': '--..', 
'_': '..--.-'}

#phras = [] #create empty list phrase to be filled with random phrase
#while len(level) >= len(phras):
#    x = 0
#    for x in range(len(level)):
#        phras = level[x]
#        phras = random.choice(wordBank)
#        print(phras)
#        x += 1
#    if len(phras) >= len(level):
#        print(phras)

#Working selection and conversion of a random phrase to Morse
#level = 1
#phrase = [0]
#if level == 1:
#    phrase = []
#    phrase[0]=random.choice(wordBank)
#    print(phrase)
#    level += 1
#elif level == 2:
#   phrase = [0]
#    phrase[0]=random.choice(wordBank)
#    phrase.append(random.choice(wordBank))
#    print(phrase)
#morse = []
#for n in phrase:
#    morse.append(codeBank[n])
#    print(morse)

def createPhrase (level):
    '''
    @brief  Randomly generates a phrase from the word bank based on user's 
            progress in the game
    @param level Value corresponding to user's progress in the game
    @return Phrase of alphabetic characters in the form of a list
    '''

    phrase = [0]
    if level == 1:
#        phrase = []
        phrase[0]=random.choice(wordBank)
        return phrase
    elif level == 2:
#        phrase=[0]
        phrase[0]=random.choice(wordBank)
        phrase.append(random.choice(wordBank))
        return phrase
    elif level == 3:
        
        phrase[0]=random.choice(wordBank)
        phrase.append(random.choice(wordBank))
        phrase.append(random.choice(wordBank))
        return phrase

def convertPhraseToMorse(n):
    '''
    @brief Converts characters to Morse code
    @details  Converts the randomly generated phrase/character into a 
                list containing its/their Morse code equivalent
    @param n Value corresponding to the elements contained in the 
                random phrase
    @return List of Morse code characters
    '''    
    return (codeBank[n])

    

    
    
