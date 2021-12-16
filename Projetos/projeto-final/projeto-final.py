import cv2
import numpy as np

#controlar os movimentos do mouse e clicar
from pynput.mouse import Button, Controller 

#obter a resolução de exibição do monitor
import tkinter as tk


#Inicialização dos controles do mouse e do vídeo
mouse=Controller()
root = tk.Tk()
sx = root.winfo_screenwidth()
sy = root.winfo_screenheight()


#Definição da resolução da imagem capturada
(video_width,video_height)=(320,240)

#Definição do range das cores dos marcadores
#Para escolher a cor do marcador que você irá utilizar descomente a cor desejada

# Green color
lowerColor=np.array([33,80,40])
upperColor=np.array([102,255,255])

# Purple color
#lowerColor = np.array([47, 15, 48])
#upperColor = np.array([80, 45, 70])

# Red color
#lowerColor = np.array([0, 0, 115])
#upperColor = np.array([90, 90, 255])

# Blue color
#lowerColor = np.array([94, 0, 0])
#upperColor = np.array([255, 90, 55])

#########################################################################

video_cap = cv2.VideoCapture(0)

#Kernels e flag de controle
k_open=np.ones((5,5))
k_close=np.ones((20,20))
pFlag=0

while True:
    
    #leitura e redimensionamento do frame
    ret, img=video_cap.read()
    img=cv2.resize(img,(340,220))

    #conversão de BGR para HSV
    imgHSV= cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    
    # criação da Mascara para identificação dos marcadores verde
    mask=cv2.inRange(imgHSV,lowerColor,upperColor)
        
    #morphology    
    #Remoção de ruído
    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,k_open)
    #fechar orifícios dentro dos objetos em primeiro plano ou pequenos pontos pretos no objeto
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,k_close)
    maskFinal=maskClose
    
    conts,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    
    print(h, conts)
    
    #lógica para o gesto de abertura, mova o mouse sem clicar
    if(len(conts)==2):
        if(pFlag==1):
            pFlag=0
            mouse.release(Button.left)
			
		
        #desenhar um retângulo aproximado ao redor da imagem binária. 
        #Esta função é usada principalmente para destacar a região de 
        #interesse após a obtenção dos contornos de uma imagem.
        x1,y1,w1,h1=cv2.boundingRect(conts[0])
        x2,y2,w2,h2=cv2.boundingRect(conts[1])
		
		#indicar a posição do marcador
        # desenhando retângulo sobre os "marcadores"
        cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(255,0,0),2)
        cv2.rectangle(img,(x2,y2),(x2+w2,y2+h2),(255,0,0),2)
		
		#coordenada do primeiro centroide (cx1,cy1)
        cx1=int(x1+w1/2)
        cy1=int(y1+h1/2)
        
		#coordenada do segundo centroide (cx2,cy2)
        cx2=int(x2+w2/2)
        cy2=int(y2+h2/2)
        
		#Ponto médio da semireta que passa por (cx1,cy1) e (cx2,cy2)
        cx=int((cx1+cx2)/2)
        cy=int((cy1+cy2)/2)
        
		#desenho da semireta
        cv2.line(img, (cx1,cy1),(cx2,cy2),(255,0,0),2)
		
        
		#desenho do ponto médio sobre a semireta
        cv2.circle(img, (cx,cy),2,(0,0,255),2)
		
        #mouse event
		
        mouseLoc= int((sx-(cx*sx/video_width))), int(cy*sy/video_height)
        mouse.position=mouseLoc 
        
        while mouse.position!=mouseLoc:
            pass
    elif(len(conts)==1):
	
		#logica para o gesto de click
		
        x,y,w,h=cv2.boundingRect(conts[0])
        if(pFlag==0):
            pFlag=1
            mouse.press(Button.left)
        
        #indicar a posição do marcador
		#desenhando o retangulo sobre o "marcador"
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
		
		#calculo do centroide do "marcador"
        cx=int((x+w/2))
        cy=int((y+h/2))
		
		#desenho do circulo do ponto médio
        cv2.circle(img,(cx,cy),int((w+h)/4),(0,0,255),2)
		
        #mouse event
		#posicionando o ponteiro do mouse no centroide do gesto
        mouseLoc=int((sx-(cx*sx/video_width))), int(cy*sy/video_height)
        mouse.position=mouseLoc     
        while mouse.position!=mouseLoc:
            pass
        
        print('Coordenadas do mouse:', mouseLoc)
    cv2.imshow("video_cap",img)
    cv2.waitKey(10)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
        