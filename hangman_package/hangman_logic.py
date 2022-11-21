from abc import ABCMeta, abstractmethod
from six import with_metaclass
from hangman_package.hangman_input import *

class AbcHangman(with_metaclass(ABCMeta)):

    @abstractmethod
    def defining_game_list(self):
        pass

    @abstractmethod
    def extracting_hil_points(self):
        pass

    @abstractmethod
    def setting_start_data(self):
        pass
    @abstractmethod
    def check_letters(self):
        pass
    @abstractmethod
    def saving_data(self):
        pass

    # @abstractmethod
    # def gaming(self):
    #     pass

class HangmanOne(AbcHangman):
    """
      The main logic of the game responsible for the gameplay:

      In the AbcHangman class main used variables are:
      self.exclude_list -> responsible to not repeat any word in the game
      self.usernames -> all usernames listed in the database
      self.username -> the current player name
      self.difficulty -> the chosen level to play
      self.category -> the chosen category to play
      self.game_list -> setting a list of words matching the player conditions
      self.hil_points -> player's hil_points taken from the database
      self.starting_data -> complete set of starting data for current game according defined
      conditions
      self.the_word -> the concrete word this game
      self.user_word -> first and empty word marked with dashes equivalent to the_word
      self.trigger -> a trigger for switching off the game
      self.guessed_letters -> list of asked letters during the game
      self.fail_count -> fail counter for each word
      self.game_points -> game points for each word, it begins with maximum number (the word length)
      self.visualisation -> variable where could be change printing interface

    """

    def __init__(self, name, diff, cat):
        self.username = name
        self.difficulty = diff
        self.category = cat
        self.hil_points = DatabaseInput.extracting_hil_points(name)
        self.starting_data = DatabaseInput.setting_start_data(self.game_list)
        self.the_word = self.starting_data["the_word"]
        self.user_word = self.starting_data["user_word"]
        self.trigger = False
        self.asked_letters = []
        self.fail_count = 0
        self.game_points = len(self.the_word)
        self.visualisation = ScreenPrint

    @staticmethod
    def analysing_letter(letter):
        """ Check is it a command and take it. """

        is_command = False

        if letter == "@":
            command = UserInput.input_command()
            is_command = True
            return (is_command, command)

        else:
            return (is_command, None)

    # @staticmethod
    def check_letters(self, letter, guessed_right):
        """ The core of gamelogic, checks for accurate letter and manages win and lost result. """

        self.asked_letters.append(letter)
        for i in range(len(self.the_word)):
            if self.the_word[i] == letter or self.the_word[i] == letter.lower() \
                    or self.the_word[i] == letter.upper():
                self.user_word[i] = self.the_word[i]
                guessed_right += 1

        if guessed_right != 0:
            self.visualisation(self.user_word).printing_in_game()
            if "_" not in self.user_word:
                self.trigger = True
                self.hil_points += 1
                self.visualisation(self.username).printing_win_result(self.hil_points,
                                                                      self.game_points)
        else:
            self.fail_count += 1
            self.game_points -= 1
            if self.game_points < 0:
                self.game_points = 0
            self.visualisation(self.fail_count).printing_hangman()
            if self.fail_count == len(self.the_word):
                self.visualisation(self.username).printing_lost_result(self.hil_points,
                                                                       self.the_word,
                                                                       self.game_points)
                self.trigger = True

        return (self.trigger, self.hil_points)




# **************************************************************************************************