import numpy as np
import cv2
import procesImage
import tensorflow as tf
import sudoku 


def augment(grid,img,imgWarped,originalCorners):

  for line in range(9):
    for column in range(9):
      if(grid[line][column]==0):
        continue
      cellWidth=imgWarped.shape[0]//9
      textScale=cellWidth/35
      textThickness=cellWidth//20
      orgx=cellWidth*(column)+cellWidth//3
      orgy=cellWidth*(line+1)-cellWidth//6

      cv2.putText(imgWarped,str(grid[line][column]),(orgx,orgy),cv2.FONT_HERSHEY_SIMPLEX,textScale,(0, 0, 255),textThickness)

  imgUnwarped=procesImage.unwarp(img,imgWarped,originalCorners)
  return imgUnwarped

def stringToNpArray(s):
  data=np.array(list(s), dtype='int64')
  grid=np.array_split(data,9)
  return grid

def npArrayToString(nparray):
  flat=nparray.flatten()
  arr=np.char.mod('%i', flat)
  string = "".join(arr)
  return string
