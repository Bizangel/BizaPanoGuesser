import cv2
import numpy as np

def check_zerogreen_col(img,col,byrow=False,maxscanvalue = None):
    zeroarray = np.array([0,0,0])
    zerogreen = True
    #Very specific black, and error green
    if maxscanvalue is None:
        if not byrow:
            for rgb in img[:,col,:]:
                if not (rgb == [0,0,0]).all() and not (rgb == [76,112 ,71]).all(): #It contains a non-zero green
                    zerogreen = False
                    break
        else:
            for rgb in img[col,:,:]:
                if not (rgb == [0,0,0]).all() and not (rgb == [76,112 ,71]).all(): #It contains a non-zero green
                    zerogreen = False
                    break
    else:
        if not byrow:
            for rgb in img[:maxscanvalue,col,:]:
                if not (rgb == [0,0,0]).all() and not (rgb == [76,112 ,71]).all(): #It contains a non-zero green
                    zerogreen = False
                    break
        else:
            for rgb in img[col,:maxscanvalue,:]:
                if not (rgb == [0,0,0]).all() and not (rgb == [76,112 ,71]).all(): #It contains a non-zero green
                    zerogreen = False
                    break
    return zerogreen

def fix_cropping(filename):
    img = cv2.imread(filename)
    ylen,xlen,_ = np.shape(img)

    foundcol = None
    for col in range(xlen):
        if check_zerogreen_col(img,col,byrow=False):
            foundcol = col
            break
            
    foundrow = None
    for row in range(ylen):
        if check_zerogreen_col(img,row,byrow=True,maxscanvalue=foundcol):
            foundrow = row
            break


    if foundcol is None or foundrow is None:
        raise(ValueError('No greenblack col and row found'))
    else:
        print(col,row)

    # gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # _,thresh = cv2.threshold(gray,1,255,cv2.THRESH_BINARY)

    # contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    # cnt = contours[0]
    # x,y,w,h = cv2.boundingRect(cnt)

    crop = img[0:foundrow,0:foundcol]
    cv2.imwrite(filename,crop)
    