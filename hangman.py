from abc import ABCMeta, abstractmethod
from six import with_metaclass
from hangman_package.hangman_display import *
from hangman_package.hangman_input import *
from hangman_package.hangman_logic import *


def run():
    """ For starting the game """

    input_data = UserInput.entering_game()
    username = input_data[0]
    level = input_data[1]
    category = input_data[2]
    player = HangmanApp(username, level, category)
    player.gaming()

class HangmanApp(object):
    """ The game manager. """

    def __init__(self, name, diff, cat):
        self.usernames = DatabaseInput.username_list
        self.username = name
        self.difficulty = diff
        self.category = cat
        self.game_list = DatabaseInput.defining_game_list(diff, cat)
        self.hil_points = DatabaseInput.extracting_hil_points(name)
        self.starting_data = DatabaseInput.setting_start_data(self.game_list)
        self.the_word = self.starting_data["the_word"]
        self.trigger = False
        self.game_points = len(self.the_word)
        self.visualisation = ScreenPrint

    def gaming(self):
        """ The gameplay, turns the game and tracks for letter or command. """

        self.visualisation.welcoming(self.username, self.hil_points)
        self.visualisation(self.the_word).printing_empty_word()

        while True:
            if self.trigger:
                break

            letter = UserInput.asking_letter(self.game_points)
            guessed_right = 0

            letter_check = HangmanOne.analysing_letter(letter)
            is_command = letter_check[0]
            command = letter_check[1]
            if is_command:
                Commands(self, command).manage_comms()
            else:
                result = HangmanOne.check_letters(letter, guessed_right)
                self.trigger = result[0]
                self.hil_points = result[1]
                if self.trigger:
                    break


        change_var = UserInput.changing_state()
        if change_var[0]:
            # Exit of game
            self.saving_data()
            Database.exclude_word_save(["blank"])
            self.visualisation.leaving_game(self.hil_points)

        else:
            # Make changes to the game
            self.saving_data()
            change_command = int(change_var[1])
            changes = UserInput.change_logic(change_command, self.difficulty,
                                                      self.category)
            self.difficulty = changes[0]
            self.category = changes[1]
            player = HangmanApp(self.username, self.difficulty, self.category)
            player.gaming()

    def saving_data(self):
        """ Save user's score to the database. """

        self.usernames[self.username] = self.hil_points
        Database.users_save(self.usernames)

class Commands(object):
    '''
    Commands through the game for exit, hints, whole word suggestion, etc..
        1. Hint,
        2. Quit game/Change category/Change diff,
        3. Guess whole word,
        4. Show/hide guessed letters,
        5. Exchange HIL points to 1 additional try
    '''

    def __init__(self, player, command):

        self.player = player.__dict__
        self.command = int(command)
        self.the_word = self.player["the_word"]
        self.user_word = self.player["user_word"]
        self.username = self.player["username"]
        self.visualisation = ScreenPrint

    def giving_hint(self):
        """ Checks the possibility for hint letter and give it. """

        if self.player["game_points"] - 2 >= 0:
            self.player["game_points"] -= 2
            ind = self.user_word.index("_")
            self.user_word[ind] = self.the_word[ind]
            self.visualisation(self.user_word).printing_in_game()
        else:
            print("You haven't enough points for hint !")

    def stop_game(self):
        """ Stopping game. """

        self.player["trigger"] = True
        self.visualisation(self.username).leaving_game(self.player["hil_points"])

    def asking_whole_word(self):
        """ User tries to ask the whole word. """

        whole_word = input("Please, enter the whole word you think it is: ")
        if whole_word == self.the_word or whole_word == self.the_word.lower():
            self.player["trigger"] = True
            self.player["hil_points"] += 1
            self.visualisation(self.username).printing_win_result(self.player["hil_points"],
                                                                  self.player["game_points"])
        else:
            self.player["fail_count"] += 1
            self.visualisation(self.player["fail_count"]).printing_hangman()

    def printing_asked_letters(self):
        """ Represents all asked letters in this game to that moment. """

        self.visualisation(self.player["guessed_letters"]).presenting_asked_letters()

    def ask_additional_try(self):
        """ A possibility for one additional try after exchanging 10 HIL points. """

        if self.player["hil_points"] - 10 >= 0 and self.player["fail_count"] >= 1:
            self.player["fail_count"] -= 1
            self.player["hil_points"] -= 10
            print(f"Now you have one more try and {self.player['hil_points']} "
                  f"HIL points remaining !")
        else:
            print("You don't have enough HIL points !")

    def manage_comms(self):
        """ Method for handling commands:
            1. Hint
            2. Stop game
            3. Asking the whole word
            4. Printing the asked letters
            5. Additional try
        """

        ops = {1: self.giving_hint,
               2: self.stop_game,
               3: self.asking_whole_word,
               4: self.printing_asked_letters,
               5: self.ask_additional_try
               }

        func_name = ops[self.command].__name__
        func_obj = getattr(self, func_name)
        func_obj()


run()