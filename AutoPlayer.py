from Player import Player
from pickomino import Pickomino
import math as m

class AutoPlayer(Player):
    """Player manipulated"""

    def __init__(self, pickomino):
        self.pickomino: Pickomino = pickomino

        # ---Current turn constant---
        self.curr_turn = -1
        self.accessible_tiles = {} # for a given sum, give the tiles that can be accessed
        self.stealable_tiles = []
        self.loss = 0

        # a state is a 6-tuple, describing the number of each dice value owned
        # This map store the expected worm gain of each state
        self.states = {}


    def set_loss(self):
        """Set the value loss from the current state of the game"""
        self.loss = 0
        if self.pickomino.players_stacks[self.pickomino.current_player] : #loss of the last tile
            self.loss = -self.pickomino.tile_values[self.pickomino.players_stacks[self.pickomino.current_player][-1]]

    def set_stealable_tiles(self):
        """"Set all the tiles possibly stealable"""

        for i,s in enumerate(self.pickomino.players_stacks):
            if i != self.pickomino.current_player and len(s) != 0 :
                self.stealable_tiles.append(s[-1])

    def set_accesible_tiles(self):
        """Found which tile is accesible from each sum of dice"""
        # init
        for i in range(0,41):
            self.accessible_tiles[i] = []

        # found which central tile is going to be picked
        for t in self.pickomino.central_tiles:
            for i in range(t,41):
                if not self.accessible_tiles[i] or self.accessible_tiles[i][0] <= t:
                    self.accessible_tiles[i] = [t]

        # add the stealable tiles
        # when a tile is stealable, there is multiple tiles available
        for t in self.stealable_tiles:
            self.accessible_tiles[t].append(t)

    def get_immediat_gain(self, state):
        """Give the maximum immediat gain of the state, if we pass or take worms"""

        if(state[-1] == 0): # if we don't have worms, we pass
            return self.loss # the state value is negativ if we pass, cause we lose a tile

        total_sum = 0
        for i,n in enumerate(state):
            total_sum += (i+1)*n
        total_sum -= state[-1] # worms are only worth 5

        acc_tile = self.accessible_tiles[total_sum]
        if not acc_tile :
            return self.loss
        elif len(acc_tile) == 1:
            return self.pickomino.tile_values[acc_tile[0]]
        else: # we value more the stole tiles cause the oponent lose points
            # static gain + average loss of the oponents because of the stealing
            return (1+1/(self.pickomino.n-1))*self.pickomino.tile_values[acc_tile[1]]

    def compute_states(self, state):
        """Compute recursivly the expected gain of the state
        It depend of the expected gain of the futur states and the immediat gain of the current state
        """

        available_dice = self.pickomino.dice_number - sum(state)
        if state in self.states.keys(): # we already computed this state
            pass

        elif available_dice == 0 or state.count(0) == 0:
            self.states[state] = self.get_immediat_gain(state)

        else :
            expected_futur_gain = 0
            for i,n in enumerate(state):
                if n != 0:
                    continue

                expected_futur_gain +=  (1/state.count(0)) * (5/6)**available_dice * self.loss
                for k in range(1, available_dice+1):
                    tmp_state = list(state)
                    tmp_state[i] = k
                    expected_futur_gain += (1/state.count(0))* m.comb(available_dice, k) * (1/6)**k * (5/6)**(available_dice-k) * self.compute_states(tuple(tmp_state))

            self.states[state] = max(self.get_immediat_gain(state), expected_futur_gain)
        return self.states[state]

    def get_state(self):
        """give a tuple discribing the dices own from the current state of the game"""

        state = [0]*6
        for d in self.pickomino.dices_own:
            state[int(d)-1] +=1
        return tuple(state)

    def best_dice(self, choices, state, dice_thrown):
        """Give the dice corresponding to the best state-value"""

        best_dice = 0
        max_value = self.loss
        for d in choices:
            tmp_state = list(state)
            tmp_state[int(d)-1] = dice_thrown.count(int(d))
            #print(tuple(tmp_state), self.states[tuple(tmp_state)])
            if self.states[tuple(tmp_state)] >= max_value:
                max_value = self.states[tuple(tmp_state)]
                best_dice = d
        return best_dice

    def get_action(self):
        if self.curr_turn != self.pickomino.current_turn: # actualise the turn information
            self.curr_turn = self.pickomino.current_turn
            self.set_stealable_tiles()
            self.set_accesible_tiles()
            self.set_loss()

            self.states = {} # reInit the states values
            self.compute_states(tuple([0]*6))

        state = self.get_state()
        state_value = self.get_immediat_gain(state)

        if len(self.pickomino.dices_thrown) != 0: # chose a dice
            best_dice = self.best_dice(self.pickomino.choices, state, self.pickomino.dices_thrown)
            return best_dice

        if "Steal" in self.pickomino.choices and self.states[state] <= state_value:
            return "Steal"
        elif "Middle" in self.pickomino.choices and self.states[state] <= state_value:
            return "Middle"
        elif "Throw" in self.pickomino.choices:
            return "Throw"
        else:
            return "Pass"



