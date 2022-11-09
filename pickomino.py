import os

from random import randint
from typing import List
from xmlrpc.client import boolean
from time import sleep





class Pickomino:
    """Represent the game as a whole, we add the players apart"""

    def __init__(self, nb_player: int, short_game: boolean = False, nb_dice: int = 8):
        "construct an instance of the pickomino"

        # ---Rules---
        self.dice_number = nb_dice
        self.short_game = short_game
        self.tile_values = {}
        for i in range(21,25):
            self.tile_values[i] = 1
        for i in range(25,29):
            self.tile_values[i] = 2
        for i in range(29,33):
            self.tile_values[i] = 3
        for i in range(33,37):
            self.tile_values[i] = 4

        # ---State parameters---
        self.n: int = nb_player  # number of player
        self.central_tiles: List[int] = list(range(21,37)) # central tiles
        self.players_stacks: List[List[int]] = [[] for _ in range(self.n)] # stack of each player
        self.dices_own: List[int] = []
        self.dices_thrown: List[int] = []
        self.choices: List[str] = []

        # ---Counters---
        self.current_turn: int = 0
        self.current_player: int = 0
        self.current_throw: int = 0

    def _state_reset(self):
        self.dices_own = []
        self.dices_thrown = []
        self.choices = []

    def _get_choices(self):
        if len(self.dices_thrown) != 0:
            return # choose a dice

        self.choices = ["Pass"]
        if len(self.dices_own) != self.dice_number:
            self.choices.append("Throw")

        if self.dices_own.count(6) == 0:  # you have no worms
            return

        dices_sum = sum(self.dices_own) - self.dices_own.count(6) # worms are worth only 5
        if dices_sum >= min(self.central_tiles):
            self.choices.append("Middle") # Take the pickomino in the middle

        for i,s in enumerate(self.players_stacks):
            if i != self.current_player and len(s) != 0 and dices_sum == s[-1]:
                self.choices.append("Steal")  # Steal someone pickomino's


    def _pass(self):
        if len(self.players_stacks[self.current_player]) != 0:
            lost_tile = self.players_stacks[self.current_player].pop()

            if(lost_tile < max(self.central_tiles)):
                self.central_tiles.remove(max(self.central_tiles))

            if not self.short_game :
                self.central_tiles.append(lost_tile)
        return False # your turn stop

    def _throw(self):
        for _ in range(self.dice_number - len(self.dices_own)):
            self.dices_thrown.append(randint(1,6))

        for d in self.dices_thrown:
            if(d in self.dices_own or str(d) in self.choices):
                continue
            self.choices.append(str(d))

        if len(self.choices) == 0:
            return self._pass() # you have already all the dices you (rick)-rolled
        return True

    def _middle(self):
        dices_sum = sum(self.dices_own) - self.dices_own.count(6)
        closest_number = 0
        for i in self.central_tiles:
            if i > dices_sum or i < closest_number:
                continue
            closest_number = i

        self.central_tiles.remove(closest_number)
        self.players_stacks[self.current_player].append(closest_number)
        return False # your turn stop


    def _steal(self):
        dices_sum = sum(self.dices_own) - self.dices_own.count(6)
        bad_player = 0
        for player,s in enumerate(self.players_stacks):
            if len(s) != 0 and dices_sum == s[-1]:
                bad_player = player # the player your going to steal to

        self.players_stacks[self.current_player].append(self.players_stacks[bad_player].pop())
        return False # your turn stop


    def _numbers(self, wanted_dice):
        for _ in range(self.dices_thrown.count(wanted_dice)):
            self.dices_own.append(wanted_dice)

        if len(self.dices_own) == self.dice_number and self.dices_own.count(6) == 0:
            return self._pass() # on don't have warms in the dices you chose

        self.dices_thrown = []
        return True # your turn continue


    def _do_actions(self, action):
        if action not in self.choices :
            raise AssertionError("Not a valid action")

        self.choices = []
        if action == "Pass":
            return self._pass()

        if action == "Throw":
            return self._throw()

        if action == "Middle":
            return self._middle()

        if action == "Steal":
            return self._steal()

        if action.isdigit():
            return self._numbers(int(action))



    def _generate_file(self, state_file, action_file):
        sf = open(state_file, "w")

        # Name of the file in which the action should be writen
        sf.write(action_file+"\n")

        # Choices
        for c in self.choices:
            sf.write(str(c)+" ")
        sf.write("\n")

        # Initially own dices
        for d in self.dices_own:
            sf.write(str(d)+" ")
        sf.write("\n")

        # Thrown Dices
        for d in self.dices_thrown:
            sf.write(str(d)+" ")
        sf.write("\n")

        # Central tiles
        for t in self.central_tiles:
            sf.write(str(t)+" ")
        sf.write("\n")

        # Number of players
        sf.write(str(self.n)+"\n")

        # Players stacks, the first tile of the statck is the one at the bottom
        for s in self.players_stacks:
            for p in s:
                sf.write(str(p)+" ")
            sf.write("\n")

        sf.close()


    def display(self):
        """Display the current state of the game"""

        print("Turn " + str(self.current_turn))
        print("Player " + str(self.current_player))
        print("Throw "+ str(self.current_throw))
        print("central tiles : " + str(self.central_tiles))
        print("players stacks : ")
        for s in self.players_stacks:
            print(str(s))
        print("dices own : " + str(self.dices_own))
        print("dices thrown : " + str(self.dices_thrown))
        print("choices : " + str(self.choices))


    def next_play(self, players, root):
        """Execute the next move of the right player and record stata/action in a file"""

        self._get_choices()

        # Generate current state file
        file_code = str(self.current_turn)+"_"+str(self.current_player)+"_"+str(self.current_throw)
        state_file = root + file_code + "__state"
        action_file = root + file_code + "_action"
        self._generate_file(state_file, action_file)

        # Launch the right player program on this state and get the action
        af = open(action_file, "w")
        if isinstance(players[self.current_player], str):
            os.system(players[self.current_player] + " " + state_file)
            sleep(5)
        else:
            p_action = players[self.current_player].get_action()
            af.write(p_action)  # python class


        af = open(action_file, "r")
        action = af.read()

        # actualise the game
        keep_playing = self._do_actions(action)
        if keep_playing:
            self.current_throw +=1
            return

        ending_turn_file = root + file_code + "_zending_state"
        self._generate_file(ending_turn_file, action_file)
        self._state_reset()
        self.current_throw = 0
        self.current_player = (self.current_player+1)%self.n
        if self.current_player == 0:
            self.current_turn += 1

    def winning_player(self):
        scores = [0]*self.n
        for i,s in enumerate(self.players_stacks):
            scores[i] = sum([self.tile_values[t] for t in s])

        best_score = max(scores)
        winner = []
        for p,s in enumerate(scores):
            if s == best_score:
                winner.append(p)
        return winner
