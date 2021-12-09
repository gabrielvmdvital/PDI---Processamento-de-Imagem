import cv2
import numpy as np
import time

try:
    import sim
except:
    print('"sim.py" could not be imported. Check whether "sim.py" or the remoteApi library could not be found. Make sure both are in the same folder as this file')

def load_image(image, resolution):
    return cv2.flip(np.array(image, dtype=np.uint8).reshape((resolution[1], resolution[0], 3)), 0)


def main():
    print('Program Started')
    sim.simxFinish(-1) # just in case, close all opened connections 
    clientID = sim.simxStart('127.0.0.1', 19999, True, True, 5000, 5) # establishes a connection between python and coppelia
    if clientID != -1:
        print('Connected to remote API server')
    else:
        print('Failed connecting to remote API server')

    return_code, camera = sim.simxGetObjectHandle(clientID, "kinect_rgb", sim.simx_opmode_oneshot_wait)
    return_code, left_motor = sim.simxGetObjectHandle(clientID, "Pioneer_p3dx_leftMotor", sim.simx_opmode_oneshot_wait)
    return_code, right_motor = sim.simxGetObjectHandle(clientID, "Pioneer_p3dx_rightMotor", sim.simx_opmode_oneshot_wait)
    return_code, pioneer = sim.simxGetObjectHandle(clientID, "Pioneer_p3dx", sim.simx_opmode_oneshot_wait)
    
    sim.simxSetJointTargetVelocity(clientID, left_motor, 0, sim.simx_opmode_streaming)
    sim.simxSetJointTargetVelocity(clientID, right_motor, 0, sim.simx_opmode_streaming)

    return_code, _, _ = sim.simxGetVisionSensorImage(clientID, camera, 0, sim.simx_opmode_streaming)
    return_code, position = sim.simxGetObjectPosition(clientID, pioneer, -1,  sim.simx_opmode_streaming)
    time.sleep(0.5)


    # inicialização das variáveis e dimensões da imagem.
    l_speed = 0
    r_speed = 0
    posicao = 0
  
    

   # resolução da imagem 640x480
    
    while clientID != -1:
        
        #test do while
        # sim.simxSetJointTargetVelocity(clientID, left_motor, 1, sim.simx_opmode_streaming)
        # sim.simxSetJointTargetVelocity(clientID, right_motor, -1, sim.simx_opmode_streaming)
        
        #################################
         return_code, resolution, image = sim.simxGetVisionSensorImage(clientID, camera, 0, sim.simx_opmode_buffer)               
         if return_code == sim.simx_return_ok:
             # Load image
            
            frame = load_image(image, resolution)
            
            # passando a imagem para escala de cinza.
            
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            
            #filtro gaussiano para suavizar os contornos
            frame = cv2.GaussianBlur(frame, (5,5), 0)
            #frame = cv2.medianBlur(frame, 5)
            
            # Bilinearização da imgaem
            
            return_code, img_bin = cv2.threshold(frame, 100,255,cv2.THRESH_BINARY)
            
           # img_bin = cv2.dilate(img_bin,None,iterations=2)
           # img_bin = cv2.bitwise_not(img_bin)
            
            
            for i in range (img_bin.shape[1]):
                if(img_bin[320, i]) == 0:
                    Posicao = i
                    break    
            if Posicao < 280:
                l_speed = 0
                r_speed = 1   
            elif Posicao > 360:
                l_speed = 1
                r_speed = 0
            else:
                l_speed = 1
                r_speed = 1
                    
            print("vl = {}, vr = {}".format(l_speed, r_speed))
            sim.simxSetJointTargetVelocity(clientID, left_motor, l_speed, sim.simx_opmode_streaming)
            sim.simxSetJointTargetVelocity(clientID, right_motor, r_speed, sim.simx_opmode_streaming)

          

            cv2.imshow('Robot camera', frame)	
            if cv2.waitKey(1) & 0xFF == 27:
                cv2.destroyAllWindows()
                break

    # Now close the connection to CoppeliaSim:
    sim.simxFinish(clientID)
    # Stop simulation
    sim.simxStopSimulation(clientID,sim.simx_opmode_oneshot_wait)
if __name__ == '__main__':
    main()