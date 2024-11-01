import numpy as np
import cv2
import procesImage
import tensorflow as tf

import sudoku
import augment

solutions={}
# load model
model = tf.keras.models.load_model("model.hdf5")
 
cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)

while cap.isOpened():
  _,img=cap.read()

  img=cv2.resize(img,(800,800))
  #process image
  imgProcessed=procesImage.preprocess(img)

  imgWarped,corners=procesImage.warp(img)

  if imgWarped is not None:
    imgWarpedProcessed=procesImage.preprocess(imgWarped)
    
    #get lines and make grid mask
    
    mask=procesImage.generateGrid(imgWarpedProcessed)
    if mask is not None:
        #use mask to remove grid lines
      imgWarpedProcessedNoGrid = cv2.bitwise_and(mask, imgWarpedProcessed)
    
      squares=procesImage.split_into_squares(imgWarpedProcessedNoGrid)

      squaresProcesed,emptySquaresIndex=procesImage.resizeCleanSquares(squares)

      nonEmptySquares=np.array(squaresProcesed)

      all_preds = list(map(np.argmax, model(tf.convert_to_tensor(nonEmptySquares))))
      
      s=""
      numNonEmptySquares=0
      for i in range(len(all_preds)):
        if i in emptySquaresIndex:
          s+="0"
        else:
          numNonEmptySquares+=1
          s+=str(all_preds[i] + 1) 
      if numNonEmptySquares<17:
        continue

      if s in solutions:
        print("loaded from memory")
        sudokuTableSolved=augment.stringToNpArray(solutions.get(s))
        sudokuTable=augment.stringToNpArray(s)
        sudokuSolutionsOnly=np.subtract(sudokuTableSolved,sudokuTable)

        imgAugmented=augment.augment(sudokuSolutionsOnly,img,imgWarped,corners)
        img=imgAugmented
      else:
        sudokuTableSolved=sudoku.solve_wrapper(s)
        if sudokuTableSolved is not None:
          print("calculated")
          sudokuTableSolved_string=augment.npArrayToString(sudokuTableSolved)
          solutions[s]=sudokuTableSolved_string

          sudokuTable=augment.stringToNpArray(s)
          sudokuSolutionsOnly=np.subtract(sudokuTableSolved,sudokuTable)

          imgAugmented=augment.augment(sudokuSolutionsOnly,img,imgWarped,corners)
          img=imgAugmented

  cv2.imshow("cap",img)
  if cv2.waitKey(1) == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()