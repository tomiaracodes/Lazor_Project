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
            self.formatted_game = formatted_game # Added this line to store formatted_game as an instance variable

class blocks(grid):
    
    def __init__(self, grid_instance):
      self.formatted_game = grid_instance.formatted_game
      super().__init__(grid_instance.unsolved_file)
      
    def block_type(self):
        A = []
        B = []
        C = []
        A_group = []
        B_group = []
        C_group = []
        for i in self.formatted_game:
          if i.startswith('A'):
              A_group.append(i)
              parts_A = A_group[0].split()
              reflect = int(parts_A[1])
              A = reflect
          elif i.startswith('B'):
              B_group.append(i)
              parts_B = B_group[0].split()
              opaque = int(parts_B[1])
              B = opaque
          elif i.startswith('C'):
              C_group.append(i)
              parts_C = C_group[0].split()
              refract = int(parts_C[1])
              C = refract
                    
class laser(grid):
    
    def __init__(self):

    
    def laser_coord():
        laser_str = []
        for i in formatted_game:
        if i.startswith('L'):
            laser_str.append(i)
        lasersx = []
        lasersy = []
        for i in range(len(laser_str)):
        L = laser_str[i].split()
        print(L)
        lasersx.append(int(L[1]))
        lasersy.append(int(L[2]))     
        print(lasersx, lasersy)
        L1 = lasersx[0], lasersy[0]
        L2 = lasersx[1], lasersy[1]
        L3 = lasersx[2], lasersy[2]
        L4 = lasersx[3], lasersy[3]
        print(L1, L2, L3, L4)
    def moving():
        # start at 0,0
        # locate the L in the file and use those coordinates to start
        # need to find a way to initialise a grid and give it coordinates
        # using dimensions of the grid learned by 
        # print(f"This game board is {game_board[1].count('o')} by {len(game_board)}
        # create a x by y grid
        # create 2D list? of each point * 3 - i.e. a 3x3=9 board is really a 9x9=81 board
        # each of those 81 points can be accessed by a block but only in half steps and 
        # corners are not allowed by laser

