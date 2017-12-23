# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : vorcepa
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 30

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2,
    'e': 1, 'f': 4, 'g': 2, 'h': 4,
    'i': 1, 'j': 8, 'k': 5, 'l': 1,
    'm': 3, 'n': 1, 'o': 1, 'p': 3,
    'q': 10, 'r': 1, 's': 1, 't': 1,
    'u': 1, 'v': 4, 'w': 4, 'x': 8,
    'y': 4, 'z': 10, '*' : 0
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    wordlen = len(word)
    
    word_score = 0
    i = 0
    while i < len(word):
        word_score += SCRABBLE_LETTER_VALUES[word[i]]
        i += 1
    word_score_length = 7*wordlen - 3*(n-wordlen)
    if word_score_length < 1:
        word_score_length = 1
    word_score += word_score_length
    
    return word_score

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
        if i == (num_vowels - 1):
            wild_card = random.choice(list(hand))
            hand[wild_card] -= 1
            hand['*'] = 1
            if hand[wild_card] == 0:
                hand.pop(wild_card)

    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    return hand

def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """    
    i = 0
    hand_store = hand
    while i < len(word):
        try:
            hand[word[i]] -= 1
            if hand[word[i]] == 0:
                hand.pop(word[i])
        except KeyError:
            print("You don't have all the letters to make that word! Try again.")
            return hand_store
        i += 1

    
    return hand

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    word = word.lower()
    word_to_list = list(word)
    word_to_list_store = word_to_list[:]
    wildcard_word = ""
    valid_word = True
    
    #checks for wildcard (*).  If it is present, loops through VOWELS (aeiou),
    #replacing * with the vowel of that iteration.  If a word is found,
    #should result in valid_word = true.  otherwise false.
    if '*' in word_to_list:
        for char in range(len(VOWELS)):
            word_to_list[word_to_list.index('*')] = VOWELS[char]
            wildcard_word = ''.join(word_to_list)
            if wildcard_word in word_list:
                word = wildcard_word
                break
            else:
                word_to_list = word_to_list_store[:]
                wildcard_word = ""
            
    #checks if the submitted word is in the master word list.
    #ends the function if not found, otherwise, continues.
    if word not in word_list:
        print("You've entered an invalid word.  Try again.")
        valid_word = False
        return valid_word
    
    #checks if every letter used in the word submission are in the player's hand
    #if true, continue.  If false, not a valid word
    i = 0
    while i < len(word):
        if word[i] not in hand and len(wildcard_word) == 0:
            print("""You're trying to use letters than are not present in your hand.
Try again.""")
            valid_word = False
            return valid_word
        else:
            valid_word = True
        i += 1
        
    #if the function made it all the way to here, the word is valid.
    #checked for wildcards, if the word was was in the master list,
    #and if the user had the letters in hand to play the submitted word.
    return valid_word

def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    return sum(hand.values())

def play_hand(hand, word_list, can_substitute):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    n = HAND_SIZE
    score = 0
    valid_word = False
    user_input_with_sub = "Enter a word, or '!!' to indicate you are finished, or '1' to substitute a letter: "
    user_input_no_sub = "Enter a word, or '!!' to indicate you are finished: "
    
    while valid_word == False or len(hand) > 0:
        print("The current letters in your hand are:")
        display_hand(hand)
        if can_substitute == True:
            word = input(user_input_with_sub)
        else:
            word = input(user_input_no_sub)
        if word == "!!":
            break #BE SURE THE FUNCTION STILL RETURNS A FINAL SCORE
        elif word == "1" and can_substitute == True:
            letter = input("Enter a letter in your hand you would like to replace (will replace all copies of that letter): ")
            hand = substitute_hand(hand, letter, can_substitute)[0]
            can_substitute = False
        elif word == "1" and can_substitute == False:
            print("You cannot make anymore substitutions!")
        else:
            valid_word = is_valid_word(word, hand, word_list)
            if valid_word == True:
                hand = update_hand(hand, word)
                score += get_word_score(word, n)
                print("That word was worth {} points!".format(get_word_score(word, n)))
                print("Your total score is {}!".format(score))
                if len(hand) == 0:
                    print("Good job! You used all the letters in your hand!")
                    break
    
    print("Your score for this hand is: {}".format(score))        
    return score, can_substitute

def substitute_hand(hand, letter, can_substitute):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    if can_substitute == True:
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        alpha_list = list(alphabet)
        hand_store = hand.copy()
        hand_list = list(hand.keys())
        hand_inverse = []
        for char in range(len(alpha_list)):
            if alpha_list[char] not in hand_list:
                hand_inverse.append(alpha_list[char])
            letter_count = hand[letter]
    
        if letter not in hand:
            print("That letter was not in your hand.  Returning to your original hand...")
            hand = hand_store
        else:
            for char in range(letter_count):
                x = random.choice(hand_inverse)
                hand[x] = hand.get(x, 0) + 1
            hand.pop(letter)
        can_substitute == False
        
    print(hand)
    return (hand, can_substitute) #dictionary, boolean
       
    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    hands_to_play = number_of_hands()
    final_score = 0
    can_substitute = True
    
    for i in range(hands_to_play):
        hand = deal_hand(HAND_SIZE)
        play = play_hand(hand, word_list, can_substitute)
        final_score += play[0]
        can_substitute = play[1]
    
    print("Your final score for the game is: {}".format(final_score))
    
def number_of_hands():
    while True:
        n = input("Enter the number of hands you would like to play (positive integer greater than 0): ")
        try:
            n = int(n)
            if n > 0:
                break
            else:
                print("Playing less than 1 hand doesn't make sense!  Try again.")                
        except ValueError:
            print("Not a valid number.  Try again.")
    
    return n

if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
    
