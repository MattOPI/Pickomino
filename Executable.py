import sys
from ManualPlayer import ManualPlayer
from pickomino import Pickomino



root = "./Game1/"

if __name__ == "__main__":
    """Where the game takes place, we create the game and the players and let them play """

    pickomino = Pickomino(2)
    p1 = sys.argv[1]
    p2 = ManualPlayer(pickomino)
    p3 = ManualPlayer(pickomino)

    players = [p2, p3]
    while len(pickomino.central_tiles) != 0:
        pickomino.next_play(players, root)