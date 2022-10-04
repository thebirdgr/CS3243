#dfs search
import sys
from collections import defaultdict
from collections import deque
pieces_dict = {
    'Knight': 'kn', 
    'King': 'k',
    "Rook": 'r',
    "Bishop": 'b',
    "Queen": 'q',
    "Ferz": 'f',
    "Princess": 'p',
    "Empress": 'e'
}
# import pprint
# pp = pprint.PrettyPrinter(width = 120, compact = True) 
# Helper functions to aid in your implementation. Can edit/remove
#############################################################################
######## Piece
#############################################################################
class Piece:
    pass

#############################################################################
######## Board
#############################################################################
class Board:
    adjacency_list = defaultdict(list)
    def __init__(self, rows, cols, grid, enemy_pieces, own_pieces, goals):
        #convert piecePositions into a tuple
        self.piecePositions = [[0 for i in range(cols)] for j in range(rows)]
        self.all_threats = []
        self.rows = rows
        self.cols = cols
        for i in range(rows):
            for j in range(cols):
                if(grid[i][j] >= 0):
                    self.piecePositions[i][j] = ['o', grid[i][j]]
                else:
                    self.piecePositions[i][j] = ['x', grid[i][j]]
        for piece in enemy_pieces:
            self.piecePositions[piece[1][0]][piece[1][1]] = (pieces_dict[piece[0]], grid[piece[1][0]][piece[1][1]])
        for piece in own_pieces:
            self.piecePositions[piece[1][0]][piece[1][1]] = ('s', grid[piece[1][0]][piece[1][1]])
        for piece in goals:
            self.piecePositions[piece[0]][piece[1]] = ('g', grid[piece[0]][piece[1]])
        # self.piecePositions[3][3] = ['q', 1]
        # creating adjacency list to move through the chess board
        # for i in range(self.rows):
        #     for j in range(self.cols):
        #         # left
        #         if(j-1 >= 0):
        #             Board.adjacency_list[(i,j)].append((i, j-1))
        #         # top-left
        #         if(j-1 >= 0 and i-1 >= 0):
        #             Board.adjacency_list[(i,j)].append((i-1, j-1))
        #         # up
        #         if(i-1 >= 0):
        #             Board.adjacency_list[(i,j)].append((i-1, j))
        #         # top-right
        #         if(j+1 < self.cols and i-1 >= 0):
        #             Board.adjacency_list[(i,j)].append((i-1, j+1))
        #         # right
        #         if(j+1 < self.rows):
        #             Board.adjacency_list[(i,j)].append((i, j+1))
        #         # down-right
        #         if(j+1 < self.cols and i+1 < self.rows):
        #             Board.adjacency_list[(i,j)].append((i+1, j+1))
        #         # down
        #         if(i+1 < self.rows):
        #             Board.adjacency_list[(i,j)].append((i+1, j))
        #         # down-left
        #         if(j-1 >= 0 and i+1 < self.rows):
        #             Board.adjacency_list[(i,j)].append((i+1, j-1))
        for e in enemy_pieces:
            if(e[0] == "King"):
                self.all_threats += self.king_moves(e[1])
            elif(e[0] == "Knight"):
                self.all_threats += self.knight_moves(e[1])
            elif(e[0] == "Rook"):
                self.all_threats += self.rook_moves(e[1])
            elif(e[0] == "Bishop"):
                self.all_threats += self.bishop_moves(e[1])
            elif(e[0] == "Queen"):
                self.all_threats += self.queen_moves(e[1])
            elif(e[0] == "Ferz"):
                self.all_threats += self.ferz_moves(e[1])
            elif(e[0] == "Princess"):
                self.all_threats += self.princess_moves(e[1])
            elif(e[0] == "Empress"):
                self.all_threats += self.empress_moves(e[1])
        # pp.pprint(self.piecePositions)
        # self.all_threats += self.queen_moves((3,3))
        self.populate_threats()
    def populate_threats(self):
        for t in self.all_threats:
            if(self.piecePositions[t[0]][t[1]][0] == 'o'):
                self.piecePositions[t[0]][t[1]][0] = 't'
    def king_moves(self, pose):
        steps = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]
        moves = []
        for step in steps:
            square = [pose[0] + step[0], pose[1] + step[1]]
            if(not(square[0] < 0 or square[0] >= self.rows or square[1] < 0 or square[1] >= self.cols)):
                moves.append(square)
        return moves
    def knight_moves(self, pose):
        moves = []
        steps = [[-2, -1],[-2, +1],[+2, -1],[+2, +1],[-1, -2],[-1, +2],[+1, -2],[+1, +2]]
        for step in steps:
            square = [pose[0] + step[0], pose[1] + step[1]]
            if(not(square[0] < 0 or square[0] >= self.rows or square[1] < 0 or square[1] >= self.cols)):
                moves.append(square)
        return moves
    def rook_moves(self, pose):
        moves = []
        steps = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        for step in steps:
            moves += self.iterative_steps(pose, step)
        return moves
    def bishop_moves(self, pose):
        moves = []
        steps = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
        for step in steps:
            moves += self.iterative_steps(pose, step)
        return moves
    def queen_moves(self, pose):
        moves = []
        steps = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]
        for step in steps:
            moves += self.iterative_steps(pose, step)
        return moves
    def ferz_moves(self, pose):
        moves = []
        steps = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
        for step in steps:
            square = [pose[0] + step[0], pose[1] + step[1]]
            if(not(square[0] < 0 or square[0] >= self.rows or square[1] < 0 or square[1] >= self.cols)):
                moves.append(square)
        return moves
    def princess_moves(self, pose):
        moves = []
        k_steps = [[-2, -1],[-2, +1],[+2, -1],[+2, +1],[-1, -2],[-1, +2],[+1, -2],[+1, +2]]
        steps = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
        for step in k_steps:
            square = [pose[0] + step[0], pose[1] + step[1]]
            if(not(square[0] < 0 or square[0] >= self.rows or square[1] < 0 or square[1] >= self.cols)):
                moves.append(square)
        for step in steps:
            moves += self.iterative_steps(pose, step)
        return moves
    def empress_moves(self, pose):
        moves = []
        k_steps = [[-2, -1],[-2, +1],[+2, -1],[+2, +1],[-1, -2],[-1, +2],[+1, -2],[+1, +2]]
        steps = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        for step in k_steps:
            square = [pose[0] + step[0], pose[1] + step[1]]
            if(not(square[0] < 0 or square[0] >= self.rows or square[1] < 0 or square[1] >= self.cols)):
                moves.append(square)
        for step in steps:
            moves += self.iterative_steps(pose, step) 
        return moves
    def iterative_steps(self, pose, step):
        moves = []
        k = 1
        # so you traverse as far in that direction as possible, and stop if it's out of the chess board or blocked by a piece
        while True:
            square = [pose[0] + k*step[0], pose[1] + k*step[1]]
            add_bool = not(square[0] < 0 or square[0] >= self.rows or square[1] < 0 or square[1] >= self.cols)
            if(add_bool):
                stop_bool = self.playable_move(square)
                if(stop_bool):
                    break
                else:
                    moves.append(square)
                    k+=1
            else:
                break
        return moves
    def playable_move(self, square):
        # check if it's blocked by anything
        # square = [row, col]
        return self.piecePositions[square[0]][square[1]][0] != 'o' # returns true if space is not free, so that means to stop, false if there is free space, so means to go

#############################################################################
######## State
#############################################################################
class State:
    pass

#############################################################################
######## Implement Search Algorithm
#############################################################################
def search(rows, cols, grid, enemy_pieces, own_pieces, goals):
    # moves = []
    #king's steps
    steps = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]
    for start in own_pieces:
        stack = [(start[1], [start[1]])]
        visited = [[False for i in range(cols)] for j in range(rows)]
        while stack:
            #current Node
            vertex, path = stack.pop(0)
            if(visited[vertex[0]][vertex[1]] == False):
                if vertex in goals:
                    return path
                visited[vertex[0]][vertex[1]] = True
                for step in steps:
                    square = (vertex[0] + step[0], vertex[1] + step[1])
                    # using or so that any point it's outside, it should not be searched
                    if(not(square[0] < 0 or square[0] >= rows or square[1] < 0 or square[1] >= cols)):
                        if(grid.piecePositions[square[0]][square[1]][0] == 'o' or grid.piecePositions[square[0]][square[1]][0] == 'g'):
                            if(visited[square[0]][square[1]] == False): 
                                stack.append((square, path + [square]))
                                if square in goals:
                                    return path + [square]
                    # for node in grid.adjacency_list[vertex]:
                        # stack.append((node, path + [node]))
    return []


#############################################################################
######## Parser function and helper functions
#############################################################################
### DO NOT EDIT/REMOVE THE FUNCTION BELOW###
# Return number of rows, cols, grid containing obstacles and step costs of coordinates, enemy pieces, own piece, and goal positions
def parse(testcase):
    handle = open(testcase, "r")

    get_par = lambda x: x.split(":")[1]
    rows = int(get_par(handle.readline())) # Integer
    cols = int(get_par(handle.readline())) # Integer
    grid = [[1 for j in range(cols)] for i in range(rows)] # Dictionary, label empty spaces as 1 (Default Step Cost)
    enemy_pieces = [] # List
    own_pieces = [] # List
    goals = [] # List

    handle.readline()  # Ignore number of obstacles
    for ch_coord in get_par(handle.readline()).split():  # Init obstacles
        r, c = from_chess_coord(ch_coord)
        grid[r][c] = -1 # Label Obstacle as -1

    handle.readline()  # Ignore Step Cost header
    line = handle.readline()
    while line.startswith("["):
        line = line[1:-2].split(",")
        r, c = from_chess_coord(line[0])
        grid[r][c] = int(line[1]) if grid[r][c] == 1 else grid[r][c] #Reinitialize step cost for coordinates with different costs
        line = handle.readline()
    
    line = handle.readline() # Read Enemy Position
    while line.startswith("["):
        line = line[1:-2]
        piece = add_piece(line)
        enemy_pieces.append(piece)
        line = handle.readline()

    # Read Own King Position
    line = handle.readline()[1:-2]
    piece = add_piece(line)
    own_pieces.append(piece)

    # Read Goal Positions
    for ch_coord in get_par(handle.readline()).split():
        r, c = from_chess_coord(ch_coord)
        goals.append((r, c))
    
    return rows, cols, grid, enemy_pieces, own_pieces, goals

def add_piece( comma_seperated) -> Piece:
    piece, ch_coord = comma_seperated.split(",")
    r, c = from_chess_coord(ch_coord)
    return [piece, (r,c)]

def from_chess_coord( ch_coord):
    return (int(ch_coord[1:]), ord(ch_coord[0]) - 97)

#############################################################################
######## Main function to be called
#############################################################################
### DO NOT EDIT/REMOVE THE FUNCTION BELOW###
# To return: List of moves
# Return Format Example: [[('a', 0), ('a', 1)], [('a', 1), ('c', 3)], [('c', 3), ('d', 5)]]
# import pprint
# pp = pprint.PrettyPrinter(width = 120, compact = True) 
def run_DFS():    
    testcase = sys.argv[1]
    rows, cols, grid, enemy_pieces, own_pieces, goals = parse(testcase)
    # print(own_pieces)
    b = Board(rows, cols, grid, enemy_pieces, own_pieces, goals)
    non_parsed_moves = search(rows, cols, b, enemy_pieces, own_pieces, goals)
    moves = []
    # print(non_parsed_moves)
    # pp.pprint(b.piecePositions)
    for i in range(len(non_parsed_moves)-1):
        #[(x1, y1), (x2, y2)]
        moves.append([(chr(non_parsed_moves[i][1]+97), non_parsed_moves[i][0]), (chr(non_parsed_moves[i+1][1]+97), non_parsed_moves[i+1][0])])
    return moves

run_DFS()