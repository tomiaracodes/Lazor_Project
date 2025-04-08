import itertools

class Grid():
  
  def __init__(self, unsolved_file):
    self.unsolved_file = unsolved_file
    self.formatted_game = self.read_bff()
    self.game_board, self.game_area, self.game_grid, self.dims, self.rows, self.cols = self.game_set_up(self.formatted_game)
    self.blocks = Blocks(self)

  def read_bff(self):
    # unsolved_file = "mad_7.bff"
    with open(self.unsolved_file, 'rb') as file:
        game = file.read()
        delim_game = game.decode('utf-8')
        formatted_game = delim_game.split('\n')
        self.formatted_game = formatted_game
    return formatted_game

  def game_set_up(self, formatted_game):     
    d_game_board = []
    parsing = False
    for line in self.formatted_game:  
      if line.startswith("GRID START"): # ensures correct counting of game_board elements
        parsing = True
      elif line.startswith("GRID STOP"):
        parsing = False
      if parsing:
        if line.startswith('o') or line.startswith('x') or line.startswith('A') or line.startswith('B') or line.startswith('C'):
          d_game_board.append(line)
    game_board = [row.replace(" ", "") for row in d_game_board]
    rows = game_board[0].count("x") + game_board[0].count("o") + game_board[0].count("A") + game_board[0].count("B") + game_board[0].count("C")
    self.rows = rows
    cols = len(game_board)
    self.cols = cols
    dims = rows*cols
    self.dims = dims
    game_area = [[0 for x in range(rows)] for y in range(cols)]
    self.game_area = game_area
    game_grid = list(itertools.product(range((3*rows)), range((3*cols))))
    self.game_grid = game_grid
    return game_board, game_area, game_grid, dims, rows, cols

class Blocks():
  def __init__(self, Grid_instance):
    self.formatted_game = Grid_instance.formatted_game
    # super().__init__(Grid_instance.unsolved_file)
    self.game_area = Grid_instance.game_area
    self.game_board = Grid_instance.game_board
    self.rows = Grid_instance.rows
    self.cols = Grid_instance.cols
    self.block_size = 3
    self.all_blocks = self.all_block_spaces()
    self.not_allowed = self.no_go()
    self.allowed = self.allowed_blocks()
  
  def def_blocks(self, formatted_game, game_board):

    reflect = []
    opaque = []
    refract = []
    A = 0
    B = 0
    C = 0
    F_A_list =[] # fixed reflect block
    F_B_list =[] # fixed opaque block
    F_C_list =[] # fixed refract block
    for row in self.game_board:
      for char in row:
        if char =='A':
          F_A_list.append(1)
        elif char =='B':
          F_B_list.append(1)
        elif char =='C':
          F_C_list.append(1)

    F_A = sum(F_A_list)
    F_B = sum(F_B_list)
    F_C = sum(F_C_list)

    parsing = False
    for row in self.formatted_game:  
      if row.startswith("GRID STOP"):
        parsing = True
      elif row.startswith("L"):
        parsing = False
      if parsing:
        if row.startswith('A'):
          reflect.append(row)
          A = int(reflect[0].split()[1])
        elif row.startswith('B'):
          opaque.append(row)                
          B = int(opaque[0].split()[1])
        elif row.startswith('C'):
          refract.append(row)
          C = int(refract[0].split()[1])
    
    
    self.A = A
    self.B = B
    self.C = C
    self.F_A = F_A
    self.F_B = F_B
    self.F_C = F_C

    return A, B, C, F_A, F_B, F_C
    
  
  def all_block_spaces(self):
    grid_size_rows = self.rows * self.block_size  # Total number of rows
    grid_size_cols = self.cols * self.block_size  # Total number of columns

    all_blocks = []
    for row in range(0, grid_size_rows, self.block_size):
      for col in range(0, grid_size_cols, self.block_size):
        block = []
        for i in range(self.block_size):
          for j in range(self.block_size):
                # Add coordinates of the block
            block.append((row + i, col + j))
        all_blocks.append(block)
        self.all_blocks = all_blocks
    return all_blocks

  def no_go(self):
    block_index = []
    not_allowed = []
    for i in range(len(self.game_board)):
      for j in range(len(self.game_board[i])):
          if self.game_board[i][j] == 'x':
            block_index.append(i*self.block_size + j)
    for index in block_index:
      if 0 <= index < len(self.all_blocks):  # Fix: Added a check to ensure index is within bounds
        not_allowed.append(self.all_blocks[index])
    self.not_allowed = not_allowed 
    return not_allowed

  def allowed_blocks(self):
    allowed = []
    for i in range(len(self.all_blocks)):
      if self.all_blocks[i] not in self.not_allowed:
        allowed.append(self.all_blocks[i])
    return allowed

class Laser():
  def __init__(self, grid_instance):
    self.formatted_game = grid_instance.formatted_game
    # super().__init__(grid_instance.unsolved_file)
    self.game_area = grid_instance.game_area
    self.game_board = grid_instance.game_board
    self.rows = grid_instance.rows
    self.cols = grid_instance.cols

  def laser_set_up(self):
    
    laser_str = []
    for i in self.formatted_game:
      if i.startswith('L'):
          laser_str.append(i)
      lasersx = []
      lasersy = []
      lasersdirx = []
      lasersdiry = []
    for i in range(len(laser_str)):
      L = laser_str[i].split()
      lasersx.append(int(L[1]))
      lasersy.append(int(L[2]))
      lasersdirx.append(int(L[3]))
      lasersdiry.append(int(L[4]))
    x_coords = []
    y_coords = []
    loc_pair = []
    dir_pair = []
    for item in range(len(lasersx)):
      x_coords.append(lasersx[item])
      y_coords.append(lasersy[item])
      loc_pair.append((x_coords[item],y_coords[item]))
      self.loc_pair = loc_pair
      dir_pair.append((lasersdirx[item], lasersdiry[item]))
      self.dir_pair = dir_pair
    return loc_pair
    return dir_pair
  
  def point_set_up(self):
    point_str = []
    for i in self.formatted_game:
      if i.startswith('P'):
        point_str.append(i)
    pointx = []
    pointy = []
    for i in range(len(point_str)):
      P = point_str[i].split()
      pointx.append(int(P[1]))
      pointy.append(int(P[2]))
    px_coords = []
    py_coords = []
    point_pair = []
    for item in range(len(pointx)):
      px_coords.append(pointx[item])
      py_coords.append(pointy[item])
      point_pair.append((px_coords[item],py_coords[item]))
      self.point_pair = point_pair
    return point_pair

  
  def reflect(self):
    if self.A > 0:
      pass
      for j in range(len(self.allowed)):
        itertools.combinations(self.allowed, self.A)
        for i in (range(self.A)):
          x1_pos = []
          y1_pos = []
          x2_pos = []
          y2_pos = []
          new_x1_pos = []
          new_y1_pos = []
          new_x2_pos = []
          new_y2_pos = []
          x_pos = []
          y_pos = []
          laser_pos_reflect = []
      
          directions = [(1,1), (1, -1), (-1,1), (-1, -1)]
      
          for i in range(len(self.loc_pair)):
            laser_pos.append(self.loc_pair[i])

            if self.loc_pair[i][0] % 2 == 1 and self.loc_pair[i][1] % 2 == 0: # how to move if x,y = odd, even
              x1_pos.append(self.loc_pair[i][0]+self.dir_pair[i][0])
              y1_pos.append(self.loc_pair[i][1]+self.dir_pair[i][1])
              for j in range(len(x1_pos)):
                if x1_pos[j] % 2 == 1 and y1_pos[j] % 2 == 0: # treating new coords (odd, even)
                  new_x1_pos.append(x1_pos[j] + self.dir_pair[i][0]*directions[1][0])
                  new_y1_pos.append(y1_pos[j] + self.dir_pair[i][1]*directions[1][1])
              
                elif x1_pos[j] % 2 == 0 and y1_pos[j] % 2 == 1: # treating new coords (even, odd)
                  new_x1_pos.append(x1_pos[j] + self.dir_pair[i][0]*directions[2][0])
                  new_y1_pos.append(y1_pos[j] + self.dir_pair[i][1]*directions[2][1])
            
            elif self.loc_pair[i][0] % 2 == 0 and self.loc_pair[i][1] % 2 == 1: # how to move if x,y = even, odd
              x2_pos.append(self.loc_pair[i][0]+self.dir_pair[i][0])
              y2_pos.append(self.loc_pair[i][1]+self.dir_pair[i][1])
         
              for j in range(len(x2_pos)):
                
                if x2_pos[j] % 2 == 1 and y2_pos[j] % 2 == 0: # treating new coords (odd, even)
                  new_x2_pos.append(x2_pos[j] + self.dir_pair[i][0]*directions[1][0])
                  new_y2_pos.append(y2_pos[j] + self.dir_pair[i][1]*directions[1][1])
                
                elif x2_pos[j] % 2 == 0 and y2_pos[j] % 2 == 1: # treating new coords (even, odd)
                  new_x2_pos.append(x2_pos[j] + self.dir_pair[i][0]*directions[2][0])
                  new_y2_pos.append(y2_pos[j] + self.dir_pair[i][1]*directions[2][1])

          laser_pos_reflect.extend([(x, y) for x, y in zip((new_x1_pos), (new_y1_pos))])
          laser_pos_reflect.extend([(x, y) for x, y in zip((new_x2_pos), (new_y2_pos))])
    
    elif self.A == 0:
        None
    return laser_pos_reflect


# checking that things work
# open_file = Grid("showstopper_4.bff")
# read_file = open_file.read_bff()
# set_up = open_file.game_set_up(read_file)
# block_intro = Blocks(open_file)
# a_blocks = block_intro.def_blocks(open_file.formatted_game, open_file.game_board)
# grid_layout = block_intro.all_block_spaces()
# no_go_blocks = block_intro.no_go()
# allow_blocks = block_intro.allowed_blocks()
# l_set_up = Laser(open_file)
# laser_set = l_set_up.laser_set_up()
# point_set = l_set_up.point_set_up()