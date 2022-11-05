import sys
import os

from ManualPlayer import ManualPlayer
from pickomino import Pickomino




if __name__ == "__main__":
    """Where the game takes place, we create the game and the players and let them play """


    nb_game = 20
    nb_player = 2

    pickomino = Pickomino(nb_player)
    p1 = ManualPlayer(pickomino)
    p2 = ManualPlayer(pickomino)

    players = [p1, p2]
    score = [0]*nb_player
    for i in range(nb_game):
        root = "./Games-1v2/Game" + str(i) + "/"
        if not os.path.isdir(root):
            os.makedirs(root)

        # reset
        pickomino = Pickomino(nb_player)
        for p in players:
            p.pickomino = pickomino

        while len(pickomino.central_tiles) != 0:
            pickomino.next_play(players, root)

        for p in pickomino.winning_player():
            score[p] +=1
        print(score)

    print("final score : " + str(score))
    