from abc import ABCMeta, abstractmethod
from six import with_metaclass
from hangman_package.hangman_display import *
from hangman_package.hangman_input import *


def run_hangman():
    """ For starting the game """

    input_data = UserInput.entering_game()
    username = input_data[0]
    level = input_data[1]
    category = input_data[2]
    player = HangmanApp(username, level, category)
    player.game_cycle()


class AbcHangman(with_metaclass(ABCMeta)):
    @abstractmethod
    def check_letters(self):
        pass

    @abstractmethod
    def save_data(self):
        pass

    @abstractmethod
    def give_hint(self):
        pass

    @abstractmethod
    def stop_game(self):
        pass

    @abstractmethod
    def ask_whole_word(self):
        pass

    @abstractmethod
    def print_asked_letters(self):
        pass

    @abstractmethod
    def ask_additional_try(self):
        pass

    @abstractmethod
    def manage_comms(self):
        pass

    @abstractmethod
    def game_cycle(self):
        pass


class HangmanApp(object):
    """ The game manager. """

    user_input = UserInput()
    data_input = DatabaseInput()

    def __init__(self, name, diff, cat):
        self.letter_mark = "_"
        self.commands_symbol = "@"
        self.visualisation = ScreenPrint
        self.usernames = self.data_input.username_list
        self.username = name
        self.difficulty = diff
        self.category = cat
        self.game_list = self.data_input.defining_game_list(diff, cat)
        self.hil_points = self.data_input.extracting_hil_points(name)
        self.starting_data = self.data_input.setting_start_data(self.game_list)
        self.the_word = self.starting_data["the_word"]
        self.user_word = self.starting_data["user_word"]
        self.game_points = len(self.the_word)
        self.asked_letters = []
        self.display_list = {"print_in_game": False, "print_hangman": False,
                             "print_asked_letters": False, "print_win_result": False,
                             "print_lost_result": False, "print_no_hint": False,
                             "print_ask_whole_word": False, "print_additional_try": False,
                             "print_leave_game": False}
        self.fail_count = 0
        self.end_trigger = False
        self.additional_try = False


# ***************************** The game logic ***************************************************

    def check_letters(self, letter, guessed_right):
        """ The core of gamelogic, checks for accurate letter and manages win and lost result. """

        self.asked_letters.append(letter)
        for i in range(len(self.the_word)):
            if self.the_word[i] == letter or self.the_word[i] == letter.lower() \
                    or self.the_word[i] == letter.upper():
                self.user_word[i] = self.the_word[i]
                guessed_right += 1

        if guessed_right != 0:
            self.display_list["print_in_game"] = True
            if self.letter_mark not in self.user_word:
                self.end_trigger = True
                self.hil_points += 1
                self.display_list["print_win_result"] = True
        else:
            self.fail_count += 1
            self.game_points -= 1
            if self.game_points < 0:
                self.game_points = 0
            self.display_list["print_hangman"] = True

            if self.fail_count == len(self.the_word):
                self.display_list["print_lost_result"] = True
                self.end_trigger = True

        return self

# ********************************* Saving data **************************************************

    def save_data(self):
        """ Save user's score to the database. """

        self.usernames[self.username] = self.hil_points
        Database.users_save(self.usernames)

# *********************************** Special commands sector *************************************

    def give_hint(self):
        """ Checks the possibility for hint letter and give it. """

        if self.game_points - 2 >= 0:
            self.game_points -= 2
            ind = self.user_word.index(self.letter_mark)
            self.user_word[ind] = self.the_word[ind]
            self.display_list["print_in_game"] = True
        else:
            self.display_list["print_no_hint"] = True

    def stop_game(self):
        """ Stopping game. """

        self.end_trigger = True
        self.display_list["print_leave_game"] = True

    def ask_whole_word(self):
        """ User tries to ask the whole word. """

        whole_word = self.display_list["ask_whole_word"] = True
        if whole_word == self.the_word or whole_word == self.the_word.lower():
            self.end_trigger = True
            self.hil_points += 1
            self.display_list["print_win_result"] = True

        else:
            self.fail_count += 1
            self.display_list["print_hangman"] = True

    def print_asked_letters(self):
        """ Represents all asked letters in this game to that moment. """
        self.display_list["print_asked_letters"] = True

    def ask_additional_try(self):
        """ A possibility for one additional try after exchanging 10 HIL points. """

        if self.hil_points - 10 >= 0 and self.fail_count >= 1:
            self.fail_count -= 1
            self.hil_points -= 10
            self.additional_try = True
        else:
            self.additional_try = False

        self.display_list["print_additional_try"] = True

    def manage_comms(self, command):
        """ Method for handling commands:
            1. Hint
            2. Stop game
            3. Asking the whole word
            4. Printing the asked letters
            5. Additional try
        """

        ops = {1: self.give_hint,
               2: self.stop_game,
               3: self.ask_whole_word,
               4: self.print_asked_letters,
               5: self.ask_additional_try
               }

        func_name = ops[command].__name__
        func_obj = getattr(self, func_name)
        func_obj()

# ********************************* The game lifecycle ****************************************************

    def game_cycle(self):
        """ The gameplay, turns the game and tracks for letter or command. """

        self.visualisation.welcoming(self)
        self.visualisation.print_empty_word(self)

        while True:
            if self.end_trigger:
                break

            letter_check = self.user_input.asking_letter(self)
            guessed_right = 0

            is_command = letter_check[0]
            letter = letter_check[1]
            if is_command:
                self.manage_comms(letter)
            else:
                self.check_letters(letter, guessed_right)
                if self.end_trigger:
                    PrinterLogic.printer_cycle(self)
                    break

            PrinterLogic.printer_cycle(self)

# ********************** State change ****************************************

        change_var = UserInput.changing_state()
        if change_var[0]:
            # Exit of game
            self.save_data()
            Database.exclude_word_save(["blank"])
            self.end_trigger = True

        else:
            # Make changes to the game
            self.save_data()
            change_command = int(change_var[1])
            changes = self.user_input.change_logic(self.difficulty, self.category,
                                                   change_command)
            self.difficulty = changes[0]
            self.category = changes[1]
            player = HangmanApp(self.username, self.difficulty, self.category)
            player.game_cycle()

# **************************************************************************************

run_hangman()