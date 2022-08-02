import pyautogui
import calendar
import time
from datetime import datetime
import os
import pygetwindow
from PIL import Image

  
def get_current_timestamp():
    # get info here: https://pynative.com/python-timestamp/
    # Current GMT time in a tuple format
    current_GMT = time.gmtime()
    # ts stores timestamp
    ts = calendar.timegm(current_GMT)
    # ts convert to datetime
    dt = datetime.fromtimestamp(ts)
    return ts, dt  


def recognize(path):
    # based on https://pyimagesearch.com/2017/02/13/recognizing-digits-with-opencv-and-python/
    from skimage import util
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import numpy as np
    import cv2
    import imutils
    from imutils import contours
        
    image = cv2.imread(path, 0)
    image = imutils.resize(image, height=500)
    edged = cv2.Canny(image, 50, 100)
    gray = edged

    dig_lookup = {
	(1, 1, 1, 0, 1, 1, 1): 0,
	(0, 0, 1, 0, 0, 1, 0): 1,
	(1, 0, 1, 1, 1, 0, 1): 2,
	(1, 0, 1, 1, 0, 1, 1): 3,
	(0, 1, 1, 1, 0, 1, 0): 4,
	(1, 1, 0, 1, 0, 1, 1): 5,
	(1, 1, 0, 1, 1, 1, 1): 6,
	(1, 0, 1, 0, 0, 1, 0): 7,
	(1, 1, 1, 1, 1, 1, 1): 8,
	(1, 1, 1, 1, 0, 1, 1): 9  }
     
    # threshold the warped image, then apply a series of morphological operations to cleanup the thresholded image
    thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (32, 80))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    thresh = util.invert(thresh)  #Invert image

    # find contours in the thresholded image, then initialize the digit contours lists
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    digitCnts = [] 
      
    set_x =[]
    set_y =[]
    set_w =[]
    set_h =[]
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        set_x.append(x)
        set_y.append(y)
        set_w.append(w)
        set_h.append(h)
        
        # if (w >= 25 and w <= 45) and (h >= 25 and h <= 45):
        #     digitCnts.append(c)
        # elif w >= 30 and (h >= 250 and h <= 650):
        #     digitCnts.append(c)


        if (w >= 20 and w <= 80) and (h >= 20 and h <= 80):
            digitCnts.append(c)
        elif w >= 20 and (h >= 250 and h <= 700):
            digitCnts.append(c)

    # fig, ax = plt.subplots()
    # ax.imshow(thresh)
    # for jj in range(len(cnts)):
    #     ix = []
    #     iy = []
    #     for ii in range(len(cnts[jj])):
    #         ix.append(cnts[jj][ii][0][0])
    #         iy.append(cnts[jj][ii][0][1])
    #     ax.scatter(ix, iy, c='r', s=40)    
    # for ii in range(len(set_x)):
    #     rect = patches.Rectangle((set_x[ii], set_y[ii]), set_w[ii], set_h[ii], linewidth=1, edgecolor='r', facecolor='none')
    #     ax.add_patch(rect)
    # # plt.show()
   
    
    # sort the contours from left-to-right, then initialize the actual digits themselves
    digitCnts = contours.sort_contours(digitCnts,method="left-to-right")[0] 
    digits = []
    outputvalue = ['']*len(digitCnts)
    
    # loop over each of the digits
    indx = 0    
    for c in digitCnts:
 	    # extract the digit ROI
        (x, y, w, h) = cv2.boundingRect(c)
        
        if (h/w)>=0.4 and (h/w)<=1.6:
            outputvalue[indx] = '.'
            indx = indx + 1
            continue
        elif (h/w)>=7. and (h/w)<=13.:
            outputvalue[indx] = '1'
            indx = indx + 1
            continue
        
        roi = thresh[y:y + h, x:x + w]
        # compute the width and height of each of the 7 segments we are going to examine
        (roiH, roiW) = roi.shape
        (dW, dH) = (int(roiW * 0.25), int(roiH * 0.15))        
        dHC = int(roiH * 0.05)
        # define the set of 7 segments
        # rectI = patches.Rectangle((x, y), w, dH, linewidth=2, edgecolor='g', facecolor='none')  # top
        # ax.add_patch(rectI)
        # rectI = patches.Rectangle((x, y), dW, h//2, linewidth=2, edgecolor='g', facecolor='none')  # top-left
        # ax.add_patch(rectI)
        # rectI = patches.Rectangle((x+w-dW, y), dW, h//2, linewidth=2, edgecolor='g', facecolor='none')  # top-right
        # ax.add_patch(rectI)
        # rectI = patches.Rectangle((x, y+h//2-dHC), w, 2*dHC, linewidth=2, edgecolor='g', facecolor='none') # center
        # ax.add_patch(rectI)
        # rectI = patches.Rectangle((x, y+h//2), dW, h//2, linewidth=2, edgecolor='g', facecolor='none') # bottom-left
        # ax.add_patch(rectI)
        # rectI = patches.Rectangle((x+w-dW, y+h//2), dW, h//2, linewidth=2, edgecolor='g', facecolor='none') # bottom-right
        # ax.add_patch(rectI)
        # rectI = patches.Rectangle((x, y+h-dH), w, dH, linewidth=2, edgecolor='g', facecolor='none') # bottom
        # ax.add_patch(rectI)
        segments = [
                ((0, 0), (w, dH)),	# top
        		((0, 0), (dW, h // 2)),	# top-left
        		((w - dW, 0), (w, h // 2)),	# top-right
        		((dW, (h // 2) - dHC) , (w-2*dW, (h // 2) + dHC)), # center
        		((0, h // 2), (dW, h)),	# bottom-left
        		((w - dW, h // 2), (w, h)),	# bottom-right
        		((0, h - dH), (w, h))	# bottom
        ]
        
        on = [0] * len(segments)
        
        # loop over the segments
        for (i, ((xA, yA), (xB, yB))) in enumerate(segments):
      		# extract the segment ROI, count the total number of
      		# thresholded pixels in the segment, and then compute
      		# the area of the segment
            segROI = roi[yA:yB, xA:xB]
            total = cv2.countNonZero(segROI)
            area = (xB - xA) * (yB - yA)

            # if the total number of non-zero pixels is greater than
      		# 35% of the area, mark the segment as "on"
            # print('seg: ', i, total / float(area))
            if total / float(area) > 0.35:
                on[i]= 1
                
        # lookup the digit and draw it on the image
        digit = dig_lookup[tuple(on)]
        # print(indx, on, digit)
        outputvalue[indx] = str(digit)

    
        indx = indx + 1
    
    # display the digits
    compose = ''
    for ii in range(len(outputvalue)):
        compose = compose + outputvalue[ii]
    
    realvalue = np.float8(compose)
    # plt.show()

    # cv2.rectangle(thresh, (x, y), (x + w, y + h), (0, 255, 0), 1)
    # cv2.putText(thresh, str(digit), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)   
    # cv2.imshow("Input", image)
    # cv2.imshow("Output", thresh)
    # cv2.waitKey(0)
    
    return realvalue




def main():
    ts, dt = get_current_timestamp()
    # specify following path acording to your system
    path_f = 'C:/Users/Lab/Pictures/hvps_'+str(ts)+'.txt'
    f = open(path_f, 'w')
    f.close()
    
    # get screensize
    x,y = pyautogui.size()
    # print(f"width={x}\theight={y}")   
    x2,y2 = pyautogui.size()
    x2,y2=int(str(x2)),int(str(y2))
    # start application (set path for the control software for the HVPS module)
    os.startfile('C:/Users/Lab/Desktop/Program/Program/G_HVPS_USERcorr_aoff.exe')
    appTitle = 'G_HVPS_USERcorr_aoff'
    time.sleep(5)
   
    my = pygetwindow.getWindowsWithTitle(appTitle)[0]
    # resize to quarter of screen screensize
    x3 = 960 #x2 // 2
    y3 = 540 #y2 // 2
    my.resizeTo(x3,y3)
    # move to top-right
    my.moveTo(x3, 0)
    # time.sleep(3)

    ii = 0
    # this cycle runs within aprox. 24 hours
    while ii in range(30000):        
        f = open(path_f, 'a')
        # save screenshot
        time.sleep(1)
        path = 'C:/Users/Lab/Pictures/shot.png'
        screenshot = pyautogui.screenshot()
        screenshot.save(path)
        
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
                
        frames={'high_volt' : (1215, 138, 1431, 219),
                'high_curr' : (1442, 138, 1664, 219),
                'fil_volt' : (1292, 269, 1587, 349),
                'fil_curr' : (1598, 269, 1892, 349),
                }
        
        # edit screenshot
        im = Image.open(path)
        
        # grab a high voltage value 
        im_crop = im.crop(frames['high_volt'])
        path_ed = 'C:/Users/Lab/Pictures/shotcut-hv.png'
        im_crop.save(path_ed, quality=100)
        try:
            # recognize value
            HV = recognize(path_ed)
        except:
            # left blank sign if it was failed
            HV = '--'
        
        # grab a beam current value
        im_crop = im.crop(frames['high_curr'])
        path_ed = 'C:/Users/Lab/Pictures/shotcut-hi.png'
        im_crop.save(path_ed, quality=100)
        try:
            HI = recognize(path_ed)
        except:
            HI = '--'        
        
        # grab a filament voltage value
        im_crop = im.crop(frames['fil_volt'])
        path_ed = 'C:/Users/Lab/Pictures/shotcut-fv.png'
        im_crop.save(path_ed, quality=100)
        try:
            FV = recognize(path_ed)
        except:
            FV = '--'
        
        # grab a filament current value
        im_crop = im.crop(frames['fil_curr'])
        path_ed = 'C:/Users/Lab/Pictures/shotcut-fi.png'
        im_crop.save(path_ed, quality=100)
        try:
            FI = recognize(path_ed)
        except:
            FI = '--'        
        
        # write the data line in an output file and the console.
        line = f'{current_time}\t{FV}\t{FI}\t{HV}\t{HI}\n'
        print(line)
        f.write(line)
        f.close()
        ii += 1   

        
        
if __name__ == '__main__':
    main()