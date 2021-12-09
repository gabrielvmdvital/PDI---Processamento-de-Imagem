import math
import cv2
import numpy as np
import time

width = 640
height = 480

referencePoints = [np.float32([[width/8,height/8],[1*width/4,height/8],[1*width/4,1*height/4],[width/8,1*height/4]]), 
np.float32([[width/4,height/2],[3*width/8,height/2],[3*width/8,3*height/4],[width/4,3*height/4]])]

currentPoint = [-1,-1,-1]

calibrating = True
fullScreen = False




cap1 = cv2.VideoCapture('videotest_roma.mp4')
cap2 =  cv2.VideoCapture('video2.mp4')


ret1, frame1 = cap1.read()
ret2, frame2 = cap2.read()
 
##################################################################################
#teste para o video estático
#inputimage1 = frame1
#inputimage2 = frame2

#rows1, cols1 = inputimage1.shape[:2]
#pts1 = np.float32([[0,0],[cols1,0],[cols1,rows1],[0,rows1]])

#rows2, cols2 = inputimage2.shape[:2]
#pts2 = np.float32([[0,0],[cols2,0],[cols2,rows2],[0,rows2]])
##################################################################################



v1_width = int(cap1.get(3))  # Width
v1_height = int(cap1.get(4))  # Height

v2_width = cap2.get(3)  # Width
v2_height = cap2.get(4)  # Height

pts2 = np.float32([[0, 0], [v2_width, 0], [0, v2_height], [v2_width, v2_height]])


##################################################################################
#Intervalo das cores

# Purple color
low_purple = np.array([47, 15, 48])
high_purple = np.array([80, 45, 70])


# Red color
low_red = np.array([0, 0, 115])
high_red = np.array([90, 90, 255])


# Green color
low_green = np.array([0, 100, 0])
high_green = np.array([40, 255, 50])


# Blue color
low_blue = np.array([94, 0, 0])
high_blue = np.array([255, 90, 55])

##################################################################################
image = np.zeros((height, width, 3), np.uint8)



def pointColor(n):
    if n == 0:
        return (0,0,255)
    elif n == 1:
        return (0,255,255)
    elif n == 2:
        return (255,255,0)
    else:
        return (0,255,0)

def mouse(event, x, y, flags, param):
    global currentPoint 

    if event == cv2.EVENT_LBUTTONDOWN:
        cp = 0
        cp2 = 0
        
        for point in referencePoints[0]:
            dist = math.sqrt((x-point[0])*(x-point[0])+(y-point[1])*(y-point[1]))
            if dist < 4:
                currentPoint[0] = cp
                break
            else:
                cp = cp + 1

        for point in referencePoints[1]:
            dist = math.sqrt((x-point[0])*(x-point[0])+(y-point[1])*(y-point[1]))
            if dist < 4:
                currentPoint[1] = cp2
                break
            else:
                cp2 = cp2 + 1

        
    if event == cv2.EVENT_LBUTTONUP:
        currentPoint = [-1,-1,-1]

    if currentPoint[0] != -1:
        referencePoints[0][currentPoint[0]] = [x,y]

    if currentPoint[1] != -1:
        referencePoints[1][currentPoint[1]] = [x,y]


    
cv2.namedWindow("test", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("test", mouse)

while cap1.isOpened() and cap2.isOpened():
    
    image[:] = (0,0,0)

    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()
    blur = cv2.GaussianBlur(frame1, (15, 15), 0)

    
    inputimage1 = frame1
    inputimage2 = frame2
    
    if calibrating:
        color = 0
        for point in referencePoints[0]:
            cv2.circle(image, (int(point[0]), int(point[1])),5,pointColor(color), -1)
            color = color + 1
        color2 = 0
        for point in referencePoints[1]:
            cv2.circle(image, (int(point[0]), int(point[1])),5,pointColor(color2), -1)
            color2 = color2 + 1
        color3 = 0

#######################################################################################################

#Reconhecimento das bolinhas coloridas que delimitarão a área em que o vídeo 2 será exibido no vídeo 1.


    #Red
    red_c = cv2.inRange(blur, low_red, high_red)
    red_c = cv2.GaussianBlur(red_c, (15, 15), 0)
    contours_red = cv2.findContours(red_c, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    #Identificação da cor vermelha e determinação dos centros da cor vermelha.
    if contours_red:
        cmax_red = max(contours_red, key=cv2.contourArea)
        cv2.drawContours(frame1, cmax_red, -1, (0, 0, 255), 1)
        Mr = cv2.moments(cmax_red)
        if Mr['m00'] == 0:
            cr_X = np.nan
            cr_Y = np.nan
        else:
            cr_X, cr_Y = int(Mr["m10"] / Mr["m00"]), int(Mr["m01"] / Mr["m00"])
        
        
    #Blue
    blue_c = cv2.inRange(blur, low_blue, high_blue)
    blue_c = cv2.GaussianBlur(blue_c, (15, 15), 0)
    contours_blue = cv2.findContours(blue_c, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    #Identificação da cor azul e determinação dos centros da cor azul.
    if contours_blue:
        cmax_blue = max(contours_blue, key=cv2.contourArea)
        cv2.drawContours(frame1, cmax_blue, -1, (255, 0, 0), 1)
        Mb = cv2.moments(cmax_blue)
        if Mb['m00'] == 0:
            cb_X = np.nan
            cb_Y = np.nan
        else:
            cb_X, cb_Y = int(Mb["m10"] / Mb["m00"]), int(Mb["m01"] / Mb["m00"])


    #Purple
    purple_c = cv2.inRange(blur, low_purple, high_purple)
    purple_c = cv2.GaussianBlur(purple_c, (15, 15), 0)
    contours_purple = cv2.findContours(purple_c, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    
    #Identificação da cor roxa e determinação dos centros da cor roxa
    if contours_purple:
        cmax_purple = max(contours_purple, key=cv2.contourArea)
        cv2.drawContours(frame1, cmax_purple, -1, (128, 0, 128), 1)
        Mp = cv2.moments(cmax_purple)
        if Mp['m00'] == 0:
            cp_X = np.nan
            cp_Y = np.nan
        else:
            cp_X, cp_Y = int(Mp["m10"] / Mp["m00"]), int(Mp["m01"] / Mp["m00"])
        
    #Green
    green_c = cv2.inRange(blur, low_green, high_green)
    green_c = cv2.GaussianBlur(green_c, (15, 15), 0)
    contours_green = cv2.findContours(green_c, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    
    #Identificação da cor verde e determinação dos centros da cor verde.
    if contours_green:
        cmax_green = max(contours_green, key=cv2.contourArea)
        cv2.drawContours(frame1, cmax_green, -1, (0, 255, 0), 1)
        Mg = cv2.moments(cmax_green)
        if Mg['m00'] == 0:
            cg_X = np.nan
            cg_Y = np.nan
        else: 
            cg_X, cg_Y = int(Mg["m10"] / Mg["m00"]), int(Mg["m01"] / Mg["m00"])


    # Localização dos centros
        #para o video test de roma a ordem dos centros de cores abaixo está invertida
        #pts1 = np.float32([[cr_X, cr_Y], [cg_X, cg_Y], [cb_X, cb_Y], [cp_X, cp_Y]])  
        
        #ordem dos centro das cores para o video test de roma
        pts1 = np.float32([[cr_X, cr_Y], [cb_X, cb_Y], [cg_X, cg_Y], [cp_X, cp_Y]])
    # Reproduz o vídeo 2 na área delimitada pelos centros das bolinhas coloridas no vídeo 1.
        M = cv2.getPerspectiveTransform(pts2, pts1)
        saida = cv2.warpPerspective(inputimage2, M, (frame1.shape[1], frame1.shape[0]), frame1,
                            borderMode=cv2.BORDER_TRANSPARENT)
    
    
    #teste com os videos
    #vis1 = np.hstack((frame1, cap1.read()[1]))



    cv2.imshow("test", saida)


 #Teste para os vídeo estatico.           
    # M = cv2.getPerspectiveTransform(pts1,referencePoints[0])
    # M2 = cv2.getPerspectiveTransform(pts2,referencePoints[1])
    #cv2.warpPerspective(inputimage1, M, (width,height), image, borderMode=cv2.BORDER_TRANSPARENT)
    #cv2.warpPerspective(inputimage2, M2, (width,height), image, borderMode=cv2.BORDER_TRANSPARENT)
   
    #cv2.imshow("test", image)


#########################################################################################################################
    key = cv2.waitKey(25) & 0xFF

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
    if key == ord("c"):
        calibrating = not calibrating

    if key == ord("f"):
        if fullScreen == False:
            cv2.setWindowProperty("test", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        else:
            cv2.setWindowProperty("test", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
        fullScreen = not fullScreen

cv2.destroyAllWindows()