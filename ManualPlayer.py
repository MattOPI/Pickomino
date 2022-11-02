from Player import Player

class ManualPlayer(Player):
    """Player manipulated by the user"""

    def __init__(self, pickomino):
        self.pickomino = pickomino

    def get_action(self):
        self.pickomino.display()
        action = input("write your action : ")
        while action not in self.pickomino.choices :
            action = input("write a correct action : ")
        return action


