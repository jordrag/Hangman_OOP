from abc import ABCMeta, abstractmethod
from six import with_metaclass

class AbcPrint(with_metaclass(ABCMeta)):
    """ In this module is immplemented the whole visualisation of the game, no matter
        of the print media.

        Main methods are:
        entering_game -> start screen, welcomes and takes data from user
        welcoming -> giving info about starting HIL points
        printing_empty_word -> prints the entire empty word in the beggining of the game
        asking_letter -> asks for letter or command in the word
        analysing_letter -> make difference between letter and command
        changing_state -> purpose to quit or make changes in game parameters
        change_logic -> making changes in game parameters
        printing_in_game -> prints the word during the game
        printing_hangman -> prints the progress of wrong answers (hanging man)
        presenting_asked_letters -> prints the all asked letters to this moment, on demand
        printing_win_result -> used when the player guesses the word
        printing_lost_result -> used when the player doesn't guess the word
        leaving_game -> printing total HIL points at the end of the game
    """


    @abstractmethod
    def welcoming(self):
        pass

    @abstractmethod
    def printing_empty_word(self):
        pass

    @abstractmethod
    def printing_in_game(self):
        pass

    @abstractmethod
    def printing_hangman(self):
        pass

    @abstractmethod
    def presenting_asked_letters(self):
        pass

    @abstractmethod
    def printing_win_result(self):
        pass

    @abstractmethod
    def printing_lost_result(self):
        pass

    @abstractmethod
    def leaving_game(self):
        pass


class ScreenPrint(AbcPrint):
    """ Printing on the screen in ASCII format only. """

    def __init__(self, value):
        self.value = value


    @staticmethod
    def welcoming(username, hil_points):
        """ Presenting current HIL points saved to the user in database. """

        print()
        print(f"Hello {username}, you have {hil_points} HIL points, let's play !")

    def printing_empty_word(self):
        """ Prints the chosen word with dashes for start of the game. """

        print()
        for i in self.value:
            print(" _ ", end="")
        print()

    def printing_in_game(self):
        """ Regular prints the word asking progress. """

        print(" ".join(self.value))

    def printing_hangman(self):
        """ Prints the hanging progress. """

        print("It's wrong ! Hanging in progress...")
        print("*" * self.value)

    def presenting_asked_letters(self):
        """ Presents a list of asked letters. """

        print(self.value)

    def printing_win_result(self, hil_points, game_points):
        """ Prints exit data when the player wins the game. """

        print(f"{self.value}, you won !")
        print(f"Total game points left: {game_points}")
        print(f"Total HIL points: {hil_points}")

    def printing_lost_result(self, hil_points, word, game_points):
        """ Prints exit data when the player looses the game. """

        print(f"Game over! {self.value}, you've lost !")
        print(f"The word is -> {word}")
        print(f"Total earned game points: {game_points}")
        print(f"Total HIL points: {hil_points}")

    def leaving_game(self, points):
        """ Final print. """

        print ("OK, bye ! Leaving...")
        print(f"Your total saved HIL points: {points}")

# **************************************************************************************************
