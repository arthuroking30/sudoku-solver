import cv2
import numpy as np

def preprocess(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # blur it blur = cv2.GaussianBlur(img_gray, (13, 13), 0) e bun dar blur = cv2.GaussianBlur(img_gray, (9, 9), 0) e original
    blur = cv2.GaussianBlur(img_gray, (9, 9), 0)

    # threshold it thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 17, 2) e bun dar thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # invert it so the grid lines and text are white
    inverted = cv2.bitwise_not(thresh, 0)

    # get a rectangle kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    # morph it to remove some noise like random dots
    morph = cv2.morphologyEx(inverted, cv2.MORPH_OPEN, kernel)

    # dilate to increase border size
    result = cv2.dilate(morph, kernel, iterations=1)
    return result

def split_into_squares(warped_img):
    squares = []

    width = warped_img.shape[0] // 9

    # find each square assuming they are of the same size
    for j in range(9):
        for i in range(9):
            p1 = (i * width, j * width)  # Top left corner of a bounding box
            p2 = ((i + 1) * width, (j + 1) * width)  # Bottom right corner of bounding box
            square=warped_img[p1[1]:p2[1], p1[0]:p2[0]]
            squares.append(square)

    return squares


def resizeCleanSquares(squares):
    cleanSquares=[]
    emptySquaresIndex=[]
    width = 32
    mid = width // 2
    for i,square in enumerate(squares):


        square=cv2.resize(square, (width, width))

        if(np.average(square)>12):
            contours,hierarchy=cv2.findContours(square,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

            maxContour=getBiggestContour(contours)
            x, y, w, h = cv2.boundingRect(maxContour)

            start_x = (width - w) // 2
            start_y = (width - h) // 2
            new_square = np.zeros_like(square)
            new_square[start_y:start_y + h, start_x:start_x + w] = square[y:y + h, x:x + w]
            
            cleanSquares.append(new_square)

        else:
            emptySquaresIndex.append(i);
            cleanSquares.append(np.zeros_like(square))

    return cleanSquares,emptySquaresIndex


def warp(img):
    height,width,_=img.shape
    imgProcessed=preprocess(img)
    contours,hierarchy=cv2.findContours(imgProcessed,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    if(len(contours)<4):
        return None,None

    #get biggest area contour
    maxContour=getBiggestContour(contours)
    corners=getCornersOrdered(maxContour)

    if corners is None:
        return None,None


    #warp perspective
    # pts1=np.float32([corners[0],corners[2],corners[1],corners[3]])
    pts2=np.float32([[0,0],[width,0],[width,width],[0,width]])

    # M = cv2.getPerspectiveTransform(pts1,pts2)
    M = cv2.getPerspectiveTransform(corners,pts2)
    imgWarped = cv2.warpPerspective(img,M,(width,width))

    return imgWarped,corners

def unwarp(img,imgWarped,corners):
    width=imgWarped.shape[0]
    pts1=np.float32([[0,0],[width,0],[width,width],[0,width]])
    # pts1=np.float32([[0,0],[width,0],[0,width],[width,width]])
    # pts2=np.float32([corners[0],corners[2],corners[1],corners[3]])


    # M = cv2.getPerspectiveTransform(pts1,pts2)
    M = cv2.getPerspectiveTransform(pts1,corners)
    imgUnWarped = cv2.warpPerspective(imgWarped,M,(width,width))
    if imgUnWarped is None:
        return None
    pts=np.array([[corners[0]],[corners[1]],[corners[2]],[corners[3]]],dtype = "int32")
    cv2.fillPoly(img,[pts],(0,0,0),16)
    combined=cv2.add(img,imgUnWarped)
    return combined


def getBiggestContour(contours):
        #get biggest area contour
    maxArea=0
    maxContour=contours[0]
    for contour in contours:
        currArea=cv2.contourArea(contour)
        if currArea>maxArea:
            maxArea=currArea
            maxContour=contour
    return maxContour

# def getCornersOrdered(maxContour):
#         #get corners of contour
#     epsilon = 0.1*cv2.arcLength(maxContour,True)
#     approx= cv2.approxPolyDP(maxContour,epsilon,True)

#     # Calculate the sum of elements in each subarray
#     sums = np.sum(approx, axis=2)
#     # Sort the indices based on the sum of elements
#     sorted_indices = np.argsort(sums, axis=0)


#     # Rearrange the array based on the sorted indices
#     approx_sorted = approx[sorted_indices]
#     approx_sorted=approx_sorted.squeeze()
#     return approx_sorted

def getCornersOrdered(maxContour):
    rect = np.zeros((4, 2), dtype = "float32")
    #get corners of contour
    # epsilon = 0.1*cv2.arcLength(maxContour,True)
    # approx= cv2.approxPolyDP(maxContour,epsilon,True)
    maxContourLen=len(maxContour)
    if maxContourLen<4: return
    pts = maxContour.reshape(maxContourLen, 2)

    # the top-left point has the smallest sum whereas the
    # bottom-right has the largest sum
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # compute the difference between the points -- the top-right
    # will have the minumum difference and the bottom-left will
    # have the maximum difference
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    # return approx_sorted

    return rect

def generateGrid(imgWarpedProcessed):
    
    width = imgWarpedProcessed.shape[0]

    #get lines and make grid mask
    edges = cv2.Canny(imgWarpedProcessed,50,150,apertureSize = 3)
    mask=255 * np.ones((width,width,1), np.uint8)

    lines = cv2.HoughLines(edges,.3,np.pi/90,200)
    if lines is None:
        return None
    for line in lines:
        for rho,theta in line:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 2000*(-b))
            y1 = int(y0 + 2000*(a))
            x2 = int(x0 - 2000*(-b))
            y2 = int(y0 - 2000*(a))

            cv2.line(mask,(x1,y1),(x2,y2),(0,0,0),12)
    return mask




def showImage(img):
    cv2.imshow("img2",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def showImages(imgs):
    for img in imgs:
        showImage(img)