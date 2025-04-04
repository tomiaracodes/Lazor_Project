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
        rows = game_board[1].count('o')
        cols = len(game_board)
        dims = rows*cols 
        game_area = [[0 for x in range(rows)] for y in range(cols)]
        
class blocks(grid):
    
    def __init__(self, grid_instance):
      self.formatted_game = grid_instance.formatted_game
      super().__init__(grid_instance.unsolved_file)
      self.dims = grid_instance.dims
      self.game_area = grid_instance.game_area

    def def_blocks(self):  
        reflect = []
        opaque = []
        refract = []
        A = 0
        B = 0
        C = 0
        for i in self.formatted_game:
            if i.startswith('A'):
                reflect.append(i)
                A = int(reflect[0].split()[1])
            elif i.startswith('B'):
                opaque.append(i)
                B = int(opaque[0].split()[1])
            elif i.startswith('C'):
                refract.append(i)
                C = int(refract[0].split()[1])
        return A, B, C

    def place_blocks(self)
                    
class laser(grid):
    
    def __init__(self):
        self.formatted_game = grid_instance.formatted_game
        super().__init__(grid_instance.unsolved_file)
    
    def laser_coord(self):
        laser_str = []
        for i in formatted_game:
        if i.startswith('L'):
            laser_str.append(i)
        lasersx = []
        lasersy = []
        for i in range(len(laser_str)):
        L = laser_str[i].split()
        # print(L)
        lasersx.append(int(L[1]))
        lasersy.append(int(L[2]))     
        # print(lasersx, lasersy)
        # print(L1, L2, L3, L4)
        x_coords = []
        y_coords = []
        laser_pair = []
        for item in range(len(lasersx)):
        x_coords.append(lasersx[item])
        y_coords.append(lasersy[item])
        laser_pair.append((x_coords[item],y_coords[item]))     
        # print(lasersx, lasersy)
        # print(L1, L2, L3, L4)
    
    def point_coord(self):
        
        point_str = []
        for i in formatted_game:
            if i.startswith('L'):
                laser_str.append(i)
                lasersx = []
                lasersy = []
                lasersdirx = []
                lasersdiry = []
        for i in range(len(laser_str)):
            L = laser_str[i].split()
            # print(L)
            lasersx.append(int(L[1]))
            lasersy.append(int(L[2]))
            lasersdirx.append(int(L[3]))
            lasersdiry.append(int(L[4]))
            # print(lasersx, lasersy)
            # print(L1, L2, L3, L4)
            x_coords = []
            y_coords = []
            loc_pair = []
            dir_pair = []
        for item in range(len(lasersx)):
            x_coords.append(lasersx[item])
            y_coords.append(lasersy[item])
            loc_pair.append((x_coords[item],y_coords[item]))
            dir_pair.append((lasersdirx[item], lasersdiry[item]))

    def move_laser(self)   

        # moving the laser
        laser_posx = []
        laser_posy = []
        laser_pos = []
        directions = [(1, 1), (1,-1), (-1,1), (-1,-1)]

        # in reflect block: 

        for i in range(len(loc_pair)):
        start = loc_pair[i]
        start_dir = dir_pair[i]
        if loc_pair[i][0] % 2 == 1 and  dir_pair[i] == (-1,1): # if x coord of block is odd - continue checking all conditions
            laser_movex = loc_pair[i][0]*directions[2][0]
            laser_posx.append(laser_movex)
            laser_movey = loc_pair[i][1]*directions[2][1]
            laser_posy.append(laser_movey)
        elif loc_pair[i][0] % 2 == 0:
            laser_movex = loc_pair[i][0]*directions[1][0]
            laser_posx.append(laser_movex)
            laser_movey = loc_pair[i][1]*directions[1][1]
            laser_posy.append(laser_movey)
        # print(laser_posx, laser_posy)
         
        # start at 0,0
        # locate the L in the file and use those coordinates to start
        # need to find a way to initialise a grid and give it coordinates
        # using dimensions of the grid learned by 
        # print(f"This game board is {game_board[1].count('o')} by {len(game_board)}
        # create a x by y grid
        # create 2D list? of each point * 3 - i.e. a 3x3=9 board is really a 9x9=81 board
        # each of those 81 points can be accessed by a block but only in half steps and 
        # corners are not allowed by laser

