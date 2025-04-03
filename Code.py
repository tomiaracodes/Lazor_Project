# class for reading bff file
# another class to udnerstand blocks
# another class for laser trajectory
# attribute number to x   
class grid():

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
    # return grid_coord
    # def create_bff()

class blocks(grid):
    
    def block_type(self):
        reflect = []
        opaque = []
        refract = []
        A_group = []
        B_group = []
        C_group = []
        for i in formatted_game:
        if i.startswith('A'):
            A_group.append(i)
            parts_A = A_group[0].split()
            A = int(parts_A[1])
            reflect = A
        elif i.startswith('B'):
            B_group.append(i)
            parts_B = B_group[0].split()
            B = int(parts_B[1])
            opaque = B
        elif i.startswith('C'):
            C_group.append(i)
            parts_C = C_group[0].split()
            C = int(parts_C[1])
            refract = C
    return(reflect, opaque, refract)
                    


class laser_move:
    


