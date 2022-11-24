from abc import ABCMeta, abstractmethod
from six import with_metaclass

class AbcPrint(with_metaclass(ABCMeta)):
    """ In this module is immplemented the whole visualisation of the game, no matter
        of the print media.

        Main methods are:
        entering_game -> start screen, welcomes and takes data from user
        welcoming -> giving info about starting HIL points
        print_empty_word -> prints the entire empty word in the beggining of the game
        print_in_game -> prints the word during the game
        print_hangman -> prints the progress of wrong answers (hanging man)
        present_asked_letters -> prints the all asked letters to this moment, on demand
        print_win_result -> used when the player guesses the word
        print_lost_result -> used when the player doesn't guess the word
        print_no_hint -> when the user has no points to take a hint
        print_ask_whole_word -> if the user wants to ask the whole word
        print_additional_try -> taking additional try exchanging HIL points
        leave_game -> printing total HIL points at the end of the game
    """


    @abstractmethod
    def welcoming(self):
        pass

    # @abstractmethod
    # def print_empty_word(self):
    #     pass

    @abstractmethod
    def print_in_game(self):
        pass

    @abstractmethod
    def print_hangman(self):
        pass

    @abstractmethod
    def present_asked_letters(self):
        pass

    @abstractmethod
    def print_win_result(self):
        pass

    @abstractmethod
    def print_lost_result(self):
        pass

    @abstractmethod
    def print_no_hint(self):
        pass

    @abstractmethod
    def print_ask_whole_word(self):
        pass

    @abstractmethod
    def print_additional_try(self):
        pass

    @abstractmethod
    def leave_game(self):
        pass

# ********************************** ASCII print class ********************************************

class ScreenPrint(AbcPrint):
    """ Printing on the screen in ASCII format only. """

    def __init__(self):
        # self.display_list = display_list
        pass

    @staticmethod
    def welcoming(player):
        """ Presenting current HIL points saved to the user in database. """

        print()
        print(f"Hello {player.username}, you have {player.hil_points} HIL points, let's play !")

    # def print_empty_word(self):
    #     """ Prints the chosen word with dashes for start of the game. """

        for i in player.user_word:
            print(i, end=" ")
        print()

    @staticmethod
    def print_in_game(player):
        """ Regular prints the word asking progress. """

        print(" ".join(player.user_word))

    @staticmethod
    def print_hangman(player):
        """ Prints the hanging progress. """

        print("It's wrong ! Hanging in progress...")
        print("*" * player.fail_count)

    @staticmethod
    def present_asked_letters(player):
        """ Presents a list of asked letters. """

        print(player.asked_letters)

    @staticmethod
    def print_win_result(player):
        """ Prints exit data when the player wins the game. """

        print(f"{player.username}, you won !")
        print(f"Total game points left: {player.game_points}")
        print(f"Total HIL points: {player.hil_points}")

    @staticmethod
    def print_lost_result(player):
        """ Prints exit data when the player looses the game. """

        print(f"Game over! {player.username}, you've lost !")
        print(f"The word is -> {player.the_word}")
        print(f"Total earned game points: {player.game_points}")
        print(f"Total HIL points: {player.hil_points}")

    @staticmethod
    def print_no_hint():
        print("You haven't enough points for hint !")

    @staticmethod
    def print_ask_whole_word():
        whole_word = input("Please, enter the whole word you think it is: ")
        return whole_word

    @staticmethod
    def print_additional_try(player):
        if player.additional_try:
            print(f"Now you have one more try and {player.hil_points} "
                  f"HIL points remaining !")
        else:
            print("You can't take addittional try before at least one missed letter or "
                  "you don't have enough HIL points !")

    @staticmethod
    def leave_game(player):
        """ Final print. """

        print("OK, bye ! Leaving...")
        print(f"Your total saved HIL points: {player.hil_points}")

# ********************************** Independent printer logic ***********************************

class PrinterLogic(object):
    """ Logic that controls print proccesses independent of the main game body. This class could
    manage the game data flow  no matter what is the exit format (ASCII, graphic, etc..).
    self.visualisation is the attribute of the object that manages the print format
    """

    def printer_cycle(self):
        """ A cycle to check triggers status from the main logic of the game and to manage
        what and how to print.
        """

        while True:

            if self.display_list["welcoming"]:
                self.visualisation.welcoming(self)
                self.display_list["welcoming"] = False

            elif self.display_list["print_in_game"]:
                self.visualisation.print_in_game(self)
                self.display_list["print_in_game"] = False

            elif self.display_list["print_hangman"]:
                self.visualisation.print_hangman(self)
                self.display_list["print_hangman"] = False

            elif self.display_list["print_asked_letters"]:
                self.visualisation.present_asked_letters(self)
                self.display_list["print_asked_letters"] = False

            elif self.display_list["print_win_result"]:
                self.visualisation.print_win_result(self)
                self.display_list["print_win_result"] = False

            elif self.display_list["print_lost_result"]:
                self.visualisation.print_lost_result(self)
                self.display_list["print_lost_result"] = False

            elif self.display_list["print_no_hint"]:
                self.visualisation.print_no_hint(self)
                self.display_list["print_no_hint"] = False

            elif self.display_list["print_ask_whole_word"]:
                self.display_list["print_ask_whole_word"] = False
                self.whole_word = self.visualisation.print_ask_whole_word()
                if self.whole_word == self.the_word or self.whole_word == self.the_word.lower():
                    self.end_trigger = True
                    self.hil_points += 1
                    self.whole_word = None
                    self.display_list["print_win_result"] = True

                else:
                    self.fail_count += 1
                    self.display_list["print_hangman"] = True

            elif self.display_list["print_additional_try"]:
                self.visualisation.print_additional_try(self)
                self.display_list["print_additional_try"] = False

            elif self.display_list["print_leave_game"]:
                self.visualisation.leave_game(self)
                self.display_list["print_leave_game"] = False

            else:
                break

        return self
# **************************************************************************************************
