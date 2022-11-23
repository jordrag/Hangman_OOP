import random
from abc import ABCMeta, abstractmethod
from six import with_metaclass
from hangman_package.hangman_db import *

class UserInput(object):

    """ The initial interface to take data from user and start the game:
        username -> the name of the player
        difficulty -> separated in 3 levels depending the word length,
        easy (3-5 symbols),
        medium (6-8),
        hard (9-30)
        category -> starting with 3 categories (cars, animals, cities)
        but could be extended during the time
    """

    @staticmethod
    def entering_game():
        """ A short brief and taking user's data. """

        print("Hello, let's play *** Hangman *** !")
        print()

        username = str(input("Enter username: "))
        difficulty = str(input("Choose difficulty level (easy, medium, hard): "))
        category = str(input("Choose category of words (animals, cars, cities): "))
        return (username, difficulty, category)



    @staticmethod
    def asking_letter(player):
        """ Represents current game points and asks for a letter. """

        print()
        print(f"Game points: {player.game_points}")
        letter = input("Ask a letter from the word: ")

        is_command = False

        if letter == player.commands_symbol:
            letter = int(input("Choose command (1. Hint, "
                                "2. Quit game/Change category/Change diff, "
                                "3. Guess whole word, 4. Show/hide guessed letters, "
                                "5. Exchange HIL points to 1 additional try --> "))
            is_command = True

        return (is_command, letter)

    @staticmethod
    def changing_state():
        """ Option to quit the game or which parameter to be changed. """

        change_trigger = False
        while True:
            try:
                change = input("Do you wanna quit (y/n) ?")
                if change == "y":
                    change_trigger = True
                    return (change_trigger, None)
                elif change == "n":
                    comm = int(input("1. Continue 2. Change level, 3. Change category: "))
                    return (change_trigger, comm)
            except Exception:
                print("Invalid input or empty category for this level, pls make another choice !")

    @staticmethod
    def change_logic(diff, categ, comm):
        """ Choose how to change parameters. """

        difficulty = diff
        category = categ

        if comm == 1:
            pass
        elif comm == 2:
            difficulty = str(input("Choose difficulty level (easy, medium, hard): "))
        elif comm == 3:
            category = str(input("Choose category of words (animals, cars, cities): "))

        return difficulty, category

# ***********************************************************************************************

class DatabaseInput(object):
    """ This class takes all data from database:
        - existing HIL points of user
        - list of words matching player's conditions
        Packs and sends them to the main module.
    """

    username_list = Database.usernames_list
    @staticmethod
    def defining_game_list(difficulty, category):
        """ Setting a list of words matching the player conditions.
            exclude_list -> responsible to not repeat any word in the game
        """

        temp_list = []
        exclude_list = Database.ex_word_read()
        min_length = Database.levels[difficulty][0]
        max_length = Database.levels[difficulty][1]

        for word in Database.categories[category]:
            if min_length <= len(word) <= max_length and word not in exclude_list:
                temp_list.append(word)
        return temp_list

    @staticmethod
    def extracting_hil_points(username):
        """ Taking user's profile info from database,
        if it doesn't exist make new user with hil_points = 0. """

        if username not in Database.usernames_list:
            Database.usernames_list[username] = 0

        return Database.usernames_list[username]

    @staticmethod
    def setting_start_data(game_list):
        """ Complete set of starting data for current game according defined
      conditions. """

        exclude_list = Database.ex_word_read()
        empty_list = []
        rnd_number = random.randrange(0, len(game_list))
        the_word = game_list.pop(rnd_number)
        exclude_list.append(the_word)
        Database.exclude_word_save(exclude_list)
        for lett in the_word:
            empty_list.append("_")
        return {"the_word": the_word, "user_word": empty_list, "words_list": game_list}


# **************************************************************************************************
