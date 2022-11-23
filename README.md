# <center> **** User manual **** </center>

*A short guide for the game "Hangman" made by me.\
It could be played by Pycharm or direct in console mode.
My examples will be from PyCharm Community Edition.*

If you want to test in Pycharm you have to preinstall it before next steps below.

### *Step 1: Taking the game*

<img src="images/Manual_hangman_1.jpg">

<p> 1. You can download the game from this [repository page](https://github.com/jordrag/Exercises/tree/main/hangman).
The easiest way is to clone it following the instructions.
<p> 2. First copy the link marked in red rectangle on the picture
<p> 3. Open Pycharm
<p> 4. Go to "Get from VCS"

<p> <img src="images/Manual_hangman_2.jpg">

<p> 5. Paste the link copied before in the URL field and choose the directory where to clone on your computer, after that click on Clone

<p> <img src="images/Manual_hangman_3.jpg">

### *Step 2: Playing the game*

1. **After the repository has been cloned, run "hangman.py" with right click on it in the Project menu** 

<p></p>

<img src="images/Manual_hangman_4.1.jpg">

2. **At the start screen fill in your username, difficulty and level**

<p> <img src="images/Manual_hangman_5.jpg">

3. **On the next screen you'll see your initial data: username wtih HIL points earned from all previous played games and the starting Game points for this game. \
They depend on the length of the current word and the rules for them are:**
   * Each wrong guess will subtract 1 from the max score
   * Each hint used will subtract 2 from the max score and the last chance to take a hint is when you have 2 points left
   * The score cannot be negative so if you reach 0 game points the game ends

<p> <img src="images/Manual_hangman_6.jpg">

4. **There is one magic symbol **"@"** for entering in submenu where you can choose from some additional options**
    
    <img src="images/Manual_hangman_7.jpg">
    
    * **The first one is "Hint" (1). The game gives you a random letter from the word.**
    <br>
    <img src="images/Manual_hangman_8.jpg">
   
    The circled stars are your wrong guessed letters from the word. Their maximum number is the length of the word and increased with each wrong answer in opposition of the Game points.
    * **The second option is multiple choice: (2) to quit the game, change category or level**
    <br>
    <img src="images/Manual_hangman_9.jpg">
    
    * **If you feel lucky or very clever you can choose the third option: (3) guess the whole word. You can type it with first capital or only smallcaps.**
    <br>
    <img src="images/Manual_hangman_12.jpg">
    
    And if you guess it you win 1 HIL point and can choose to play again or to quit.
    <br>
    <img src="images/Manual_hangman_13.jpg">
    
    * **In every single moment of the game you can show a list of all your asked letters (4)**
    <br>
    <img src="images/Manual_hangman_11.jpg">
    
    * **If you have too many letters more to guess but have no more lives you can exchange 10 HIL points (if you have them) for one more try in the fifth option (5)**
    <br>
    <img src="images/Manual_hangman_14.jpg">
    <br>
    <img src="images/Manual_hangman_15.jpg">
    
5. **If you choose to leave the game from (2) your HIL points are saved to the database and next time you play with this username the game will begin with them.**
    <br>
6. **If you hang on the rope (loose the game), you'll see the right word, your current HIL points and if you want, you can quit the game.**
    <br>
    <img src="images/Manual_hangman_16.jpg">
    
# <center> **** Enjoy the game !!! ****
