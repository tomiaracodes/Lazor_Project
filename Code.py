# class for reading bff file
# another class to udnerstand blocks
# another class for laser trajectory
# attribute number to x   
class grid()

    def __init__(self, unsolved_file):
        self.unsolved_file = unsolved_file
    
    def read_bff(self):
        with open(unsolved_file, 'rb') as file:
            game = file.read()
            delim_game = game.decode('utf-8')
            formatted_game = delim_game.split('\n')
            print(formatted_game)
            game_board = []
            for i in formatted_game:
                if i.startswith('o') or i.startswith('x'):
                    game_board.append(i)
            print(game_board)
    return grid_coord
    def create_bff()

    return solved_file

class blocks:
    
    def __init__(self, A, B, C):
    
        self.A = 0
        self.B = 0
        self.C = 0
    '''Initialise number of reflect, 
    opaque and refract blocks to be 0'''

    def block_type(self, A,B,C):
        countA = 0
        countB = 0
        countC = 0
        if A:
            countA = countA+1
        if B:
            countB = countB+1
        if C:
            countC = countC+1


class laser_move:
    


