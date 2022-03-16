import time, copy, math

def copy_list(lst):
  new_list=[]
  for i in range(len(lst)):
    new_list.append([])
    for j in lst[i]:
      if(type(j) is int):
        new_list[i].append(j)
      else:
        new_list[i].append(0)
  return new_list

def print_board(board):
  for i in range(len(board)):
      print(board[i])

class Sudoku:
  def __init__(self, array):
    self.board=array
    self.permanent=array

  def print(self):
    for i in range(len(self.board)):
      print(self.board[i])

  def dups_in_rows(self, rowIdx):
    row=self.board[rowIdx]
    for i in range(len(self.board)):
      for j in range(len(self.board)):
        if((type(self.board[rowIdx][i]) is int) and (type(self.board[rowIdx][j]) is int)):
          if (i!=j and row[i]==row[j]):
            return True
    return False
      
  def dups_in_cols(self, colIdx):
    for i in range(len(self.board)):
      for j in range(len(self.board)):
        if((type(self.board[i][colIdx]) is int) and (type(self.board[j][colIdx]) is int)):
          if(i!=j and self.board[i][colIdx]==self.board[j][colIdx]):
            return True
    return False

  # Removes any numbers already contained in the row from the 
  # array of possible numbers
  def is_contained_in_row(self, rowIdx, possibles):
    row=self.board[rowIdx]
    for i in range(len(self.board)):
      if (type(self.board[rowIdx][i]) is int) and self.board[rowIdx][i] in possibles:
        possibles.remove(self.board[rowIdx][i])

    return possibles
  # Removes any numbers already contained in the col from the 
  # array of possible numbers
  def is_contained_in_col(self, colIdx, possibles):
    for i in range(len(self.board)):
      if (type(self.board[i][colIdx]) is int) and self.board[i][colIdx] in possibles:
        possibles.remove(self.board[i][colIdx])

    return possibles

  # Checks if 3x3 grid at starting column and starting row 
  # has duplicates
  def dups_in_box(self, row, col):
    colStart=(col//int(math.sqrt(len(self.board)))*int(math.sqrt(len(self.board))))
    rowStart=(row//int(math.sqrt(len(self.board))))*(int(math.sqrt(len(self.board))))
    colEnd = colStart + int(math.sqrt(len(self.board)))
    rowEnd = rowStart + int(math.sqrt(len(self.board)))

    elements = []
    for colIdx in range(colStart, colEnd):
      for rowIdx in range (rowStart, rowEnd):
        if type(self.board[rowIdx][colIdx]) is int and self.board[rowIdx][colIdx] in elements:
          return True
        elements.append(self.board[rowIdx][colIdx])

    return False

  # Removes items already in the box
  def is_contained_in_box(self, row, col, possibles):
    colStart=(col//int(math.sqrt(len(self.board)))*int(math.sqrt(len(self.board))))
    rowStart=(row//int(math.sqrt(len(self.board)))*int(math.sqrt(len(self.board))))
    colEnd = colStart + int(math.sqrt(len(self.board)))
    rowEnd = rowStart + int(math.sqrt(len(self.board)))

    for colIdx in range(colStart, colEnd):
      for rowIdx in range (rowStart, rowEnd):
        if (type(self.board[rowIdx][colIdx]) is int) and self.board[rowIdx][colIdx] in possibles:
          possibles.remove(self.board[rowIdx][colIdx])

    return possibles
  def is_valid(self):
    for i in range(9):
      if(self.dups_in_cols(i) or self.dups_in_rows(i)):
        return False
    for i in range(0,len(self.board),int(math.sqrt(len(self.board)))):
      for j in range(0,len(self.board),int(math.sqrt(len(self.board)))):
        if(self.dups_in_box(i,j)):
          return False
    return True
  
  def finished(self):
    if(self.is_valid()):
      for i in range(len(self.board)):
        for j in range(len(self.board[i])):
          if(not (self.board[i][j] is int)):
            return False
      return True
    return False


class Solution:
  def __init__(self, sudoku):
    self.sudoku=sudoku
    self.solved=False
    self.frontier=[]

  def possible_sols_board(self):
    for i in range(len(self.sudoku.board)):
      for j in range(len(self.sudoku.board[i])):
        if(not(type(self.sudoku.board[i][j]) is int) or self.sudoku.board[i][j]==0):
          possibles=[x for x in range(1,len(self.sudoku.board)+1)]
          possibles=self.sudoku.is_contained_in_row(i,possibles)
          possibles=self.sudoku.is_contained_in_col(j,possibles)
          possibles=self.sudoku.is_contained_in_box(i,j,possibles)
          self.sudoku.board[i][j]=possibles
  
    
  # Gets a possible soln for row,col
  def minimal(self):
    row,col,min=0,0,len(self.sudoku.board)
    for i in range(len(self.sudoku.board)):
      for j in range(len(self.sudoku.board[i])):
        if(not(type(self.sudoku.board[i][j]) is int) and len(self.sudoku.board[i][j])<min):
          row,col,min=i,j,len(self.sudoku.board[i][j])
    
    # print("Minimal row and col is ", row, col, self.sudoku.board[row][col], "with length", min) 
    return row, col, min
  
  # Solves the Sudoku
  def solve(self):
    # while(not(self.sudoku.finished())):
    while(True):
      self.possible_sols_board()
      minrow,mincol, minl = self.minimal()
      if(minl==len(self.sudoku.board) and minrow==0 and mincol==0):
        break
      if(minl==0):
        if(len(self.frontier)>0):
          if(copy_list(self.sudoku.board)==copy.deepcopy(self.frontier[-1][0])):
            del self.frontier[-1]
          self.sudoku.board=copy.deepcopy(self.frontier[-1][0])
        else:
          print_board(copy_list(self.sudoku.board))
          break
        continue
      if(len(self.frontier)>0 and self.frontier[-1][0] == copy_list(self.sudoku.board)):
        self.frontier[-1][3]+=1
        if(len(self.sudoku.board[self.frontier[-1][1]][self.frontier[-1][2]])<=self.frontier[-1][3]):
          del self.frontier[-1]
          if(len(self.frontier) > 0):
            self.sudoku.board = copy.deepcopy(self.frontier[-1][0])
            continue
          else:
            print_board(copy_list(self.sudoku.board))
            break
        else:
          self.sudoku.board[self.frontier[-1][1]][self.frontier[-1][2]]=self.sudoku.board[self.frontier[-1][1]][self.frontier[-1][2]][self.frontier[-1][3]]
      elif(len(self.sudoku.board[minrow][mincol])>1):
        self.frontier.append([copy_list(self.sudoku.board),minrow,mincol,0])
        self.sudoku.board[minrow][mincol]=self.sudoku.board[minrow][mincol][0]
      elif(len(self.sudoku.board[minrow][mincol])==1):
        self.sudoku.board[minrow][mincol]=self.sudoku.board[minrow][mincol][0]
      else:
        if(len(self.frontier)>0):
          if(copy_list(self.sudoku.board)==self.frontier[-1][0]):
            del self.frontier[-1]
          self.sudoku.board=copy.deepcopy(self.frontier[-1][0])
        else:
          print_board(copy_list(self.sudoku.board))
          break
        continue
      if(not(self.sudoku.is_valid())):
        if(len(self.frontier)>0):
          self.sudoku.board=copy.deepcopy(self.frontier[-1][0])
        else:
          print_board(copy_list(self.sudoku.board))
          break
    

  # Check if a valid solution has been found
  def is_valid(self, board):
    # Check all columns, rows, and 3x3 grids for duplicates
    for colIdx in range(len(board)):
      if board.dups_in_cols(colIdx):
        return False 

    for rowIdx in range(len(board)):
      if board.dups_in_rows(rowIdx):
        return False

    for rowIdx in range(len(board)):
      for colIdx in range(len(board)):
        if board.dups_in_box(rowIdx, colIdx):
          return False
    return True

def main():
  print("Starting...")
  b=open("board.txt","r")
  board=[]
  line=b.readline()
  i=0
  while line:
    board.append([])
    for j in line.split():
      board[i].append(int(j))
    i+=1
    line=b.readline()

  mySudoku = Sudoku(board)
  mySudoku.print()
  start = time.time()

  soln = Solution(mySudoku)
  soln.solve()
  print( "Solved in {} seconds".format( time.time() - start ) )
  print("Final board:")
  soln.sudoku.print()

if __name__== "__main__":
	main()
