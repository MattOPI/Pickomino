from abc import abstractmethod

class Player:
    """what each player should do at least"""

    @abstractmethod
    def get_action(self):
        """Output an action considering the game state"""
        pass