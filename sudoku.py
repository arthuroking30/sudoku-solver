import numpy as np

def checkAxis(grid,y,x,n):
  #check x axis
  for i in range(9):
    if(i==x):
      continue
    if(grid[y][i]==n):
      return False
  
  for i in range(9):
    if(i==y):
      continue
    if(grid[i][x]==n):
      return False
    
  return True


def possible(grid,y,x,n):
  if grid[y][x]!=0:
    return False
  
  if not checkAxis(grid,y,x,n):
    return False
    
  cellx=(x)//3+1 #find coord x of cell
  celly=(y)//3+1 #find coord y of cell

  #check grid
  for i in range((celly-1)*3,celly*3):
    for j in range((cellx-1)*3,cellx*3):
      if(grid[i][j]==0):
        continue
      if(grid[i][j]==n):

        return False #"Number repeats in grid"

  return True

def solve(grid):
  for y in range(9):
    for x in range(9):
      if(grid[y][x]==0):
        for n in range(1,10):
          if(possible(grid,y,x,n)):
            grid[y][x]=n
            solve(grid)

            #remove this to find all solutions, not just first:
            #......
            if(np.sum(grid)==405):
              return grid
            #......
            
            grid[y][x]=0
        return
      
  #add them to array here
  return




def solvable(grid,y,x,n):

  if not checkAxis(grid,y,x,n):
    return False
  
  cellx=(x)//3+1 #find coord x of cell
  celly=(y)//3+1 #find coord y of cell

  #check grid if number is twice in square
  counter=0
  for i in range((celly-1)*3,celly*3):
    for j in range((cellx-1)*3,cellx*3):
      if(grid[i][j]==0):
        continue
      if(grid[i][j]==n):
        counter+=1
  if(counter>1):
    return False
  return True

def checkSolvable(grid):
  for y in range(9):
    for x in range(9):
      if(grid[y][x]!=0):
        solution=solvable(grid,y,x,grid[y][x])
        if not solution:
          return False
  return True


def solve_wrapper(s):
  data=np.array(list(s), dtype='int64')
  grid=data.reshape((9,9))
  if not checkSolvable(grid):
    return None
  solution=solve(grid)
  return solution

