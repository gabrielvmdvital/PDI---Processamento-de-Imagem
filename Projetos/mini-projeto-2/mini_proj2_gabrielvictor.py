import cv2
import numpy as np


name = "video.mp4"
name0 = "video"
video_cap = cv2.VideoCapture(name)

freezeFrame = True #flag que trava o primeiro frame do video
flag1 = False #flag que permite o controle para apagar onde foi pintado
flag_mouse = False # flag que identifica o click do mouse
flag_b = False  #flag que identifica a solicitação da borracha para apagar a mascara.




video_width = int(video_cap.get(3))  # largura
video_height = int(video_cap.get(4))  # Altura
video_fps = video_cap.get(5)  # FPS
mask = np.zeros((video_height, video_width), dtype="uint8")

exhibition_mode = "Inpainted"  # Flag que identifica a escolha do modo de exibição
fourcc = cv2.VideoWriter_fourcc(*'XVID')

out = cv2.VideoWriter('output_inpait.avi', fourcc, 30.0, (video_width, video_height))





def mouse_event(event, x, y, flags, params):
    global flag1, cord_x, cord_y, flag_mouse

    if event == cv2.EVENT_LBUTTONDOWN or event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
            cord_x, cord_y = x, y
            flag_mouse = True
            
    elif event == cv2.EVENT_MBUTTONDOWN:
        flag1 = not flag1
        flag_mouse = False
        
    else:
        flag_mouse = False



cv2.namedWindow(winname='Freeze Frame')
cv2.setMouseCallback("Freeze Frame", mouse_event)
ret, frame = video_cap.read()
freeze_frame = frame.copy()

while video_cap.isOpened():

    while freezeFrame:
        cv2.destroyWindow(exhibition_mode)
        # checagem da existencia de uma mascara na pasta do arquivo.
        aux = np.array(cv2.imread("name.jpg"))
              
        if aux.all() != None: 
            mask = cv2.imread("name.jpg", cv2.IMREAD_GRAYSCALE)
            freezeFrame = False
            cv2.destroyAllWindows()
            break
        else:
            # Caso não haja a mascara, aqui criamos a mascara
            if flag_mouse and not flag1:
                                    
                if flag_b == False:
                    cv2.circle(freeze_frame, (cord_x, cord_y), 6, (255, 255, 255), -1)
                    cv2.circle(mask, (cord_x, cord_y), 6, 255, -1)
                else:
                    cv2.circle(freeze_frame, (cord_x, cord_y), 6, (0, 0, 0), 8)
                  #  cv2.circle(mask, (cord_x, cord_y), 6, 255, -1)               

            elif flag_mouse and flag1:
                x_, y_ = cord_x - 10, cord_y - 10
                freeze_frame[y_:(y_ + 2 * 10), x_:(x_ + 2 * 10)] = frame.copy()[y_:(y_ + 2 * 10), x_:(x_ + 2 * 10)]
                cv2.circle(mask, (cord_x, cord_y), 12, 0, -1)
                
            
            
            key = cv2.waitKey(25) & 0xFF
            
            if cv2.waitKey(1) & 0xFF == ord('m'):

                freezeFrame = False
                cv2.destroyAllWindows()
                print("Exhibition Modes Keys:\n")
                print("----- Original press o -----\n")
                print("----- Inpainted press i -----\n")
                print("----- Inpainted - Borracha press b -----\n")                
                break

            mask_show = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
            
            frame_show = freeze_frame
            cv2.imshow("Freeze Frame", freeze_frame)
            
            
            if key & 0xFF == ord('b'):
               flag_b = not flag_b

    # Key inputs
    key = cv2.waitKey(1)
    if key == ord('q'):
        cv2.imwrite("name.jpg", mask)
        break
    if key == ord('p'):
        freezeFrame = True
        freeze_frame = frame.copy()

    if key == ord('o'):
        exhibition_mode = "Original"
        cv2.destroyAllWindows()
    if key == ord('i'):
        exhibition_mode = "Inpainted"
        cv2.destroyAllWindows()
   

    ret, frame = video_cap.read()
    frame_painted = cv2.inpaint(frame, mask, 3, cv2.INPAINT_TELEA)


    if exhibition_mode == "Original":
        frame_show = frame
    elif exhibition_mode == "Inpainted":
        frame_show = frame_painted

    frame_show = cv2.resize(frame_show, (960, 500))
    cv2.imshow(exhibition_mode, frame_show)
    out.write(frame_painted)

video_cap.release()
out.release()
cv2.destroyAllWindows()
