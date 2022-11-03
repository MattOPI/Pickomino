Each state file is generated is as follow :

0. the file in which the output should be written
1. the choices available
2. The dices owned by the player
3. The dices rolled
4. The central tiles
5. The number of player
6+n. The stack of each player (the stack is ending with the last added pickomino, the visible one)

## How to use it
- python :
Create your own class taking exemple on the ManualPlayer.
1. You should import pickomino and have it in your class to get the state of the game
2. You have to implementthe Player interface and have the methode GetAction() (the signature is not fixed in python)
this method should return a action considering the state of the game
3. Modify the Executable to include your class among the players



## TODO_1
I tried to do an example for java but it's not quite working... I don't manage to create the manual user...
Actually, it should be easier for a non Manual user cause it will write directly in the file...
My current problem is that i don't manage interact with user with the java file, and make the python file wait tile the java file finished his things

- java (and other programming languages):
1. The java file should be gave in argument to the python executable, (there may have some things to comment and uncomment)
and the path of the file will be added as a players.
2. Then the pickomino will compute your file in the shell with a game state in argument
3. You should read the file gave in argument and include all the state-information in your class to have the state of the game
4. Finally You'll have to write the action you want to do among the choices, in the action_file.
(probably look at the shape of the ManualPlayer.java first)

## TODO_2
- the manual chose is a but annoying... a number would certainly be better to choose the different options

- Java and other kind of files should also work along, but this is really not ideal since the program will be restart at each different step...
that's a way to make the things interact, but there may be a way to keep the java file runnning and to continue interacting with it.
Avoiding closing it and open a new one at each step...