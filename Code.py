import itertools
from itertools import combinations, product
import random

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
    self.allowed_fixed = self.allowed_if_fixed()
    self.A, self.B, self.C, self.F_A, self.F_B, self.F_C = self.def_blocks()
    self.init_place = self.init_place_blocks()
    self.board_state = self.build_board()
    self.F_A_loc = self.F_A_loc
    self.F_B_loc = self.F_B_loc
    self.F_C_loc = self.F_C_loc
    

  def def_blocks(self):

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
    self.F_A = F_A
    F_B = sum(F_B_list)
    self.F_B = F_B
    F_C = sum(F_C_list)
    self.F_C = F_C

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
      allowed = [block for block in self.all_blocks if block not in self.not_allowed]
      self.allowed = allowed
      return allowed

  def allowed_if_fixed(self):
    all_laser_paths = []
    allowed_if_fixed = []
    F_A_block_index, F_B_block_index, F_C_block_index = [], [], []
    F_A_loc, F_B_loc, F_C_loc = [], [], []
    for i in range(len(self.game_board)):
      for j in range(len(self.game_board[i])):
          if self.game_board[i][j] == 'A':
            F_A_block_index.append(i*self.block_size + j)
          elif self.game_board[i][j] == 'B':
            F_B_block_index.append(i*self.block_size + j)
          elif self.game_board[i][j] == 'C':
            F_C_block_index.append(i*self.block_size + j)
    for index in F_A_block_index:
      if 0 <= index < len(self.allowed):
        F_A_loc.append(self.allowed[index])
    for index in F_B_block_index:
      if 0 <= index < len(self.allowed):
        F_B_loc.append(self.allowed[index])
    for index in F_C_block_index:
      if 0 <= index < len(self.allowed):
        F_C_loc.append(self.allowed[index])
    self.allowed_fixed = [block for block in self.allowed 
                        if block not in F_A_loc and block not in F_B_loc and block not in F_C_loc]
    self.F_A_loc = F_A_loc
    self.F_B_loc = F_B_loc
    self.F_C_loc = F_C_loc
    return self.allowed_fixed
  

  def init_place_blocks(self):
    # Decide which list to use for placement
   
    if self.F_A == 0 and self.F_B == 0 and self.F_C == 0:
        allowed_space = self.allowed
    else:
        allowed_space = self.allowed_fixed  # Your new helper function
    
    init_place_A, init_place_B, init_place_C = [], [], []
    random.shuffle(allowed_space)

    while True: 
      init_place_A, init_place_B, init_place_C = [], [], []

      if self.A > 0:
          combination_A = itertools.combinations(allowed_space, self.A)
          combi_A = list(combination_A)
          if combi_A:
              init_place_A = random.choice(combi_A)
          else:
            init_place_A = []
      if self.B > 0:
          remaining_space_B = [block 
                               for block in allowed_space 
                               if not any(coord in [c for b in list(init_place_A) for c in b] for coord in block)] 
          combination_B = itertools.combinations(allowed_space, self.B)
          combi_B = list(combination_B)
          if combi_B:
              init_place_B = random.choice(combi_B)
          else: 
            init_place_B = []
      if self.C > 0:
          remaining_space_C = [block 
                               for block in allowed_space 
                               if not any(coord in [c for b in list(init_place_A) + list(init_place_B) for c in b] for coord in block)]
          combination_C = itertools.combinations(allowed_space, self.C)
          combi_C = list(combination_C)
          if combi_C:
              init_place_C = random.choice(combi_C)
          else: 
            init_place_C = []

      all_placed_blocks = [tuple(block) for block in list(init_place_A) + list(init_place_B) + list(init_place_C)]  
      if len(all_placed_blocks) == len(set(all_placed_blocks)):
            break
    
    self.init_place = {
    'A': init_place_A,
    'B': init_place_B,
    'C': init_place_C,
    'F_A': self.F_A_loc,
    'F_B': self.F_B_loc,
    'F_C': self.F_C_loc}

    return self.init_place

  '''Place the blocks before mapping laser traj'''
  def build_board(self):
    
    allowed_space = self.allowed if self.F_A == 0 and self.F_B == 0 and self.F_C == 0 else self.allowed_fixed
    flattened_coords = [item for sublist in allowed_space for item in sublist]
    board_state = {coord: None for coord in flattened_coords}

    for block_type, positions in self.init_place.items():
      for coord in positions:
        for block_coord in coord:  
          board_state[block_coord] = block_type
    
    self.board_state = board_state
    
    return self.board_state

class Laser():
  def __init__(self, Grid_instance, Block_instance):
    self.formatted_game = Grid_instance.formatted_game
    # super().__init__(grid_instance.unsolved_file)
    self.game_area = Grid_instance.game_area
    self.game_board = Grid_instance.game_board
    self.rows = Grid_instance.rows
    self.cols = Grid_instance.cols
    self.all_blocks = Block_instance.all_blocks
    self.allowed = Block_instance.allowed
    self.F_A = Block_instance.F_A
    self.F_B = Block_instance.F_B
    self.F_C = Block_instance.F_C
    self.A = Block_instance.A
    self.B = Block_instance.B
    self.C = Block_instance.C
    self.block_size = 3
  

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
    las_x = []
    las_y = []
    las_start = []
    dir_start = []
    for item in range(len(lasersx)):
      las_x.append(lasersx[item])
      las_y.append(lasersy[item])
      las_start.append((las_x[item],las_y[item]))
      dir_start.append((lasersdirx[item], lasersdiry[item]))
    self.las_start = las_start
    self.dir_start = dir_start
    self.las_x = las_x
    self.las_y = las_y
    return self.las_start, self.dir_start

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
    return self.point_pair

class Solver():
  def __init__(self, Grid_instance, Block_instance, Laser_instance):
    self.point_pair = Laser_instance.point_set_up()
    self.las_start, self.dir_start = Laser_instance.laser_set_up()
    self.board_state = Block_instance.build_board()
    self.F_A_loc = Block_instance.F_A_loc
    self.F_B_loc = Block_instance.F_B_loc
    self.F_C_loc = Block_instance.F_C_loc
    self.init_place = Block_instance.init_place_blocks()
    self.tried_combis = set()
    self.F_A = Block_instance.F_A
    self.F_B = Block_instance.F_B
    self.F_C = Block_instance.F_C
    self.allowed = Block_instance.allowed
    self.allowed_fixed = Block_instance.allowed_fixed
    self.all_blocks = Block_instance.all_blocks
    self.las_x = Laser_instance.las_x
    self.las_y = Laser_instance.las_y
    self.las_start = Laser_instance.las_start
    self.dir_start = Laser_instance.dir_start
    self.init_place_A = Block_instance.init_place['A']
    self.init_place_B = Block_instance.init_place['B']
    self.init_place_C = Block_instance.init_place['C']
    self.build_board = Block_instance.build_board
    self.A = Block_instance.A
    self.B = Block_instance.B
    self.C = Block_instance.C
   
  
  def reflect(self, x, y, dir):
    
    directions = [(1,1), (1, -1), (-1,1), (-1, -1)]
    next_positions = []
    if x % 2 == 1 and y % 2 == 0: # how to move if x,y = odd, even (top)
      dir = directions[1]
      nxt_x = x + dir[0]
      nxt_y = y + dir[1]
      next_positions.append((nxt_x, nxt_y, dir))

    elif x % 2 == 0 and y % 2 == 1: # even, odd (sides)
      dir = directions[2]
      nxt_x = x + dir[0]
      nxt_y = y + dir[1]
      next_positions =[]
      next_positions.append((nxt_x, nxt_y, dir))

    self.next_positions = next_positions
    return self.next_positions

  def opaque(self, x, y):
    return None, None

  def refract(self, x, y, dir):
    directions = [(1,1), (1, -1), (-1,1), (-1, -1)]
    refracted_directions = []
    if x % 2 == 1 and y % 2 == 0:  # odd, even
      refracted_directions.append(directions[1]) 
      refracted_directions.append(dir)
    elif x % 2 == 0 and y % 2 == 1:  # even, odd
      refracted_directions.append(directions[2])
      refracted_directions.append(dir)
    next_positions = []
    for new_dir in refracted_directions:
      nxt_x = x + new_dir[0]
      nxt_y = y + new_dir[1]
      next_positions.append((nxt_x, nxt_y, new_dir))
      self.next_positions = next_positions
    return self.next_positions

  def init_place_blocks(self):
    return self.init_place

  def pos_chk(self, x, y, allow_blck):
    self.x = self.las_x
    self.y = self.las_y
    las_start = (self.x, self.y)
    self.laser_start = las_start
    for i in range(len(self.all_blocks)):
      for j in range(len(self.all_blocks[i])):
        if self.all_blocks[i][j] == (x,y):
          return True
    return False

  def hit_chk(self, laser_path, points):
    for i in range(len(laser_path)):
      for j in range(len(points)):
        if laser_path[i] == points[j]:
          return True

  def game_play(self):
    reset_board = self.board_state
    if self.F_A == 0 and self.F_B == 0 and self.F_C == 0:
      allowed_space = self.allowed
    else:
      allowed_space = self.allowed_fixed
    all_laser_paths = []

    combis_A = itertools.combinations(allowed_space, self.A) if self.A > 0 else [()]
    combis_B = itertools.combinations(allowed_space, self.B) if self.B > 0 else [()]
    combis_C = itertools.combinations(allowed_space, self.C) if self.C > 0 else [()]
    self.all_combis = list(product(
        combinations(allowed_space, self.A),
        combinations(allowed_space, self.B),
        combinations(allowed_space, self.C)
    ))
    random.shuffle(self.all_combis)  

    for combo_A, combo_B, combo_C in self.all_combis:
      flat_A = [coord for block in combo_A for coord in block]
      flat_B = [coord for block in combo_B for coord in block]
      flat_C = [coord for block in combo_C for coord in block]
        
      if set(flat_A) & set(flat_B): 
        continue
      if set(flat_A + flat_B) & set(flat_C): 
        continue
      if set(flat_B) & set(flat_C):  
        continue

      self.init_place = {
        'A': combo_A if self.A > 0 else [],
        'B': combo_B if self.B > 0 else [],
        'C': combo_C if self.C > 0 else [],
        'F_A': self.F_A_loc,
        'F_B': self.F_B_loc,
        'F_C': self.F_C_loc
        }
      self.board_state = self.build_board()

      laser_paths = self.trace_laser_paths()

      if self.hit_chk(laser_paths, self.point_pair):
        all_laser_paths = laser_paths
        break

    self.init_place = self.init_place_blocks() # Assuming you'll rename this method
    self.board_state = self.build_board()  # Update the board state
    self.init_place_A = self.init_place['A']
    self.init_place_B = self.init_place['B']
    self.init_place_C = self.init_place['C']
    self.F_A_loc = self.init_place['F_A']
    self.F_B_loc = self.init_place['F_B']
    self.F_C_loc = self.init_place['F_C']
  
    laser_path = []
    for i in range(len(self.las_x)):
      start_x = self.las_x[i] 
      start_y = self.las_y[i]
      dir_x, dir_y = self.dir_start[i]

      laser_path.append((start_x, start_y))
      
      nxt_stp_x, nxt_stp_y = start_x + dir_x, start_y + dir_y

      while self.pos_chk(nxt_stp_x, nxt_stp_y, self.all_blocks):
        laser_path.append((nxt_stp_x, nxt_stp_y))
        block_type = self.board_state.get((nxt_stp_x, nxt_stp_y))
        if block_type:
          if block_type in ('A', 'F_A'):
            next_positions = self.reflect(nxt_stp_x, nxt_stp_y, (dir_x, dir_y))
            if next_positions:
              nxt_stp_x, nxt_stp_y, (dir_x, dir_y) = next_positions[0]
            # else:
            #     break
          elif block_type in ('B', 'F_B'):
            nxt_stp_x, nxt_stp_y = self.opaque(nxt_stp_x, nxt_stp_y)
            break
          elif block_type in ('C', 'F_C'):
            next_positions = self.refract(nxt_stp_x, nxt_stp_y, (dir_x, dir_y))
            if next_positions:
              nxt_stp_x, nxt_stp_y, (dir_x, dir_y) = next_positions[0]
            # else:
            #     break

        else:
            nxt_stp_x += dir_x  # move in the x-direction
            nxt_stp_y += dir_y # move in the y-direction
          
      if self.hit_chk(laser_path, self.point_pair):
        all_laser_paths.append(laser_path)
        self.all_laser_paths = all_laser_paths
        break
      else:
        laser_path = []
        reflect = False  
        opaque = False 
        refract = False 
    
    all_laser_paths.append(laser_path)
    self.all_laser_paths = all_laser_paths
          
    finished_board = all_laser_paths + list(self.init_place_A) + list(self.init_place_B) + list(self.init_place_C) + list(self.F_A_loc) + list(self.F_B_loc) + list(self.F_C_loc)
    return finished_board

  def save_solution(self):
    with open("Solution.txt", "w") as file:
      file.write(f"Board State:\n{self.board_state}\n")
      file.write(f"Laser Paths:\n")
      for path in self.all_laser_paths:
          file.write(f"{path}\n")
    return self.all_laser_paths, self.board_state

  def trace_laser_paths(self):
    all_laser_paths_for_combi = []
    return all_laser_paths_for_combi