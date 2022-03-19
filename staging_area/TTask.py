"""!
@file TTask.py
@brief Determines actuation for motor control
@details This task computes the actuation for motors.  It receives desired velocity 
         values from the UTask, measured velocity values from the ETask, and sends 
         the required duty cycle to the MTask.  
         
         See source code:
         https://bitbucket.org/bbartl01/mechatronics-labs/src/master/Lab4/CTask.py
         
@author Baxter Bartlett
@author Nick DeSimone
@author Miles Ibarra
@date 03-18-22
"""
   
from time import ticks_us, ticks_ms, ticks_add, ticks_diff
import micropython
import os
import gc
from ulab import numpy as np

## @brief Creates a state called S0_INIT
#  @details Variable will be the state 0 for starting the program
#
S0_INIT = micropython.const(0)

## @brief Creates a state called S1_RUN
#  @details Variable will be the state 1 for reading and wriing values
#
S1_RUN = micropython.const (1)

## @brief Creates a state called S2_CALIB
#  @details Variable will be the state 2 for calibrating the touchpad
#
S2_CALIB = micropython.const (2)

## @brief Creates a state called S3_SAVE_CAL_COEFFS
#  @details Variable will be the state 3 for storing the calibration coefficients
#
S3_SAVE_CAL_COEFFS = micropython.const (3)

## @brief Creates a state called S4_WRITE_CAL_COEFFS
#  @details Variable will be the state 4 for writing the calibration coefficients
#
S4_WRITE_CAL_COEFFS = micropython.const (4)

## @brief Creates a variable for the center of the pad
#  @details Variable will be the location in the center used for calibration
#
CAL_CENTER = micropython.const(0)

## @brief Creates a variable for the top left of the pad
#  @details Variable will be the location in the top left used for calibration
#
CAL_TOP_LEFT = micropython.const(1)

## @brief Creates a variable for the top right of the pad
#  @details Variable will be the location in the top right used for calibration
#
CAL_TOP_RIGHT = micropython.const(2)

## @brief Creates a variable for the bottom left of the pad
#  @details Variable will be the location in the bottom left used for calibration
#
CAL_BOTTOM_LEFT = micropython.const(3)

## @brief Creates a variable for the bottom right of the pad
#  @details Variable will be the location in the bottom right used for calibration
#
CAL_BOTTOM_RIGHT = micropython.const(4)

def TouchpadFunction(taskName, period, Pos, touch, alpha, betaf, abfShare):
    '''! @brief Touchpad function that passes values for the balls positions and velocities.
         @details This function passes the values of the balls positions and velocities
                  on the touch pad with respect to the center of the pad. 
         @param taskName Names the task so that multiple tasks can be run simultaneously.
         @param period Passes in the period at which the code is run.
         @param Pos A tuple containing positions of the x,y,z direction.
         @param touch An object of the touchpad driver
         @param alpha A value for the alpha variable of the filtering
         @param betaf A value for the betaf variable of the filtering
         @param abfshare A shared parameter that indicates the position and velocities of the ball for filtering.
    '''
    
    ## @brief creates a variable called state
    #  @details Variable will be used for setting the states
    #
    state = S0_INIT
    
    ## @brief creates a variable called start_time
    #  @details Variable set to be the starting time in micro seconds
    #
    start_time = ticks_us()
    
    ## @brief creates a variable called next_time
    #  @details Variable set to be the next time which will be subtracted
    #           from the current_time
    #
    next_time = ticks_add(start_time, period)
    
    filename = "Touchpad_cal_coeffs.txt"
    
    filestring = ''
    
    n = 0
    
    vxk = 0
    
    vyk = 0
    
    zc = 0
    
    zf = 0
    
    xk = 0
    yk = 0
    
    #share
    alpha = alpha
    
    betaf = betaf
    
    c = CAL_CENTER
    
    t = 0
     
    while True:
    
        ## @brief creates a variable called current_time
        #  @details Variable set to ticks_us() within the loop to continue to set
        #           a new time stamp.
        #
        current_time = ticks_us()
        if ticks_diff(current_time, next_time) >= 0:
            
            if state == S0_INIT:
                
                if filename in os.listdir():
                    # File exists, read from it
                    state = S4_WRITE_CAL_COEFFS
                else:
                    # File doesnt exist, calibrate manually and 
                    # write the coefficients to the file
                    
                    print('--- Touch Panel Calibration Interface ---')
                    print('To calibrate the touch panel, touch the panel'
                          'in the specified locations with something pointy (like' 
                          'a pencil).  There will be 5 locations in total.')
                    print('First touch the panel in the center.')
                    state = S2_CALIB
                                
                
            elif state == S1_RUN:
                abfShare.write((-xk,-vxk,yk,vyk,zf))
                Ts = ticks_diff(current_time, t)*(1E-6)
                t = ticks_us()
                Pos.write(touch.XYZ_Scan())
                x, y, z = Pos.read()
                if z == 0:
                    xk += 0
                    yk += 0
                    vxk += 0
                    vyk += 0
                    zc+=1
                    zf += 0
                    if zc > 10:
                        xk = 0
                        yk = 0
                        vxk = 0
                        vyk = 0
                        zf = 0
                    #print(f'xk: {xk}, vxk: {vxk}, yk: {yk}, vyk: {vyk}, 0')
                #computation loop
                elif z == 1:
                    
                    if zc != 0:
                        if zc >= 10:
                            xk = x
                            yk = y
                            zf = 1
                        zc = 0
                        
                    xk1 = xk + alpha*(x-xk)+Ts*vxk
                    vxk1 = vxk + (betaf/Ts)*(x-xk)
                    
                    yk1 = yk + alpha*(y-yk)+Ts*vyk
                    vyk1 = vyk + (betaf/Ts)*(y-yk)
                    #after computing, update for next iteration
                    xk = xk1
                    vxk = vxk1
                    
                    yk = yk1
                    vyk = vyk1
                    #print(f'xk: {xk}, vxk: {vxk}, yk: {yk}, vyk: {vyk}')
                
                    
            
                
                #print('x: ' + str(x), 'y: ' + str(y), 'z: ' + str(z))
                
#                eulAng.write(BNO.get_euler())
#                head, pitch, roll = eulAng.read()
##                print('head: ' +str(head), 'pitch: ' +str(pitch), 'roll: ' +str(roll))
#                gyrVel.write(BNO.get_omega())
#                gyr_x,gyr_y,gyr_z = gyrVel.read()
##                print('ang_vel_x: ' +str(gyr_x), 'ang_vel_y: ' +str(gyr_y), 'ang_vel_z: ' +str(gyr_z))
                
                
                    
            elif state == S2_CALIB:
                
                if c == CAL_CENTER:
                    xC,yC,zC = touch.XYZ_Scan()
                    if zC == 1:
                        xd,yd,zF = touch.XYZ_Scan()
                        if zF == 0:
                            print('Touch the panel in the top left corner')
                            c = CAL_TOP_LEFT
                            
                        
                elif c == CAL_TOP_LEFT:
                    xTL, yTL, zTL = touch.XYZ_Scan()
                    if zTL == 1:
                        xd,yd,zF = touch.XYZ_Scan()
                        if zF == 0:
                            print('Touch the panel in the top right corner')
                            c = CAL_TOP_RIGHT
                            
                        
                elif c == CAL_TOP_RIGHT:
                    xTR, yTR, zTR = touch.XYZ_Scan()
                    if zTR == 1:
                        xd,yd,zF = touch.XYZ_Scan()
                        if zF == 0:                            
                            print('Touch the panel in the bottom left corner')
                            c = CAL_BOTTOM_LEFT
                        
                elif c == CAL_BOTTOM_LEFT:
                    xBL, yBL, zBL = touch.XYZ_Scan()
                    if zBL == 1:
                        xd,yd,zF = touch.XYZ_Scan()
                        if zF == 0:                            
                            print('Touch the panel in the bottom right corner')
                            c = CAL_BOTTOM_RIGHT
                        
                elif c == CAL_BOTTOM_RIGHT:
                    xBR, yBR, zBR = touch.XYZ_Scan()
                    if zBR == 1:
                        xd,yd,zF = touch.XYZ_Scan()
                        if zF == 0:
                            print('Computing calibration coefficients')
                            c = CAL_CENTER
                            state = S3_SAVE_CAL_COEFFS
                    
            elif state == S3_SAVE_CAL_COEFFS:
                X = np.array([[xC, yC, 1], [xTL, yTL, 1], [xTR, yTR, 1], [xBL, yBL, 1], [xBR, yBR, 1]])
                print(X)
                X_t = X.transpose()
                Y = np.array([[0, 0], [-80, 40], [80, 40], [-80, -40], [80, -40]])
                print(Y)
                # multiply X transpose and X
                X_tX = np.dot(X_t, X)
                # find the inverse of the product of X transpose and X
                X_tX1 = np.linalg.inv(X_tX)
                # find the product of the inverse and X transpose
                X_tX1_X_t = np.dot(X_tX1, X_t)
                # Find the product that yields the calibration coefficients
                beta = np.dot(X_tX1_X_t, Y)
                print(beta)
                # Pull each element out of the calibration coefficient matrix
                Kxx = beta[0][0]
                Kyx = beta[0][1]
                Kxy = beta[1][0]
                Kyy = beta[1][1]
                xo = beta[2][0]
                yo = beta[2][1]
                
                #set the calibration coefficients
                touch.set_cal_coeff(Kxx, Kxy, xo, Kyx, Kyy, yo)
                
                with open(filename, 'w') as f:
                    # Perform manual calibration
                    buf = [Kxx, Kxy, xo, Kyx, Kyy, yo]
                    gc.collect()
                    
                    for element in buf:
                        filestring += str(element)
                        filestring += ','
                        n += 1
                                                   
                    if n == 6:
                        print(filestring)
                        print('writing to file')
                        filestring = filestring[:-1]
                        f.write(filestring)
                        state = S1_RUN
                        t = ticks_us()
                        
            elif state == S4_WRITE_CAL_COEFFS:
                    
                with open(filename, 'r') as f:
                    # Read the first line of the file
                    cal_data_string = f.readline()
                    print(cal_data_string)
                    # Split the line into multiple strings
                    # and then convert each one to a float
                    cal_values = [float(cal_value) for cal_value in cal_data_string.strip().split(',')]
                    print(cal_values)
                    
                    Kxx = cal_values[0]
                    Kxy = cal_values[1]
                    xo = cal_values[2]
                    Kyx = cal_values[3]
                    Kyy = cal_values[4]
                    yo = cal_values[5]
                    
                    touch.set_cal_coeff(Kxx, Kxy, xo, Kyx, Kyy, yo)
                state = S1_RUN
                t = ticks_us()
                
            else:
                pass
            
            next_time = ticks_add(next_time, period)
                
            yield state

        else:
            
            yield None
            
def calInfo():
    '''
    @brief Prints IMU calibration instructions
    @details Prints three strings in a 3 second interval in order to inform the user

    '''
    start_time = ticks_ms()
    cdn = 4 # countdown number
    while cdn >= 0:
        round_time = ticks_ms()
        if ((ticks_diff(round_time,start_time)) > 1000):
            if cdn == 4:
                print('Instructions: ')
            elif cdn == 3:
                print(' - Touch the panel as instructed on screen')
            elif cdn == 2:
                print(' - 5 locations in total')
            elif cdn == 1:
                print(' - Repeat touches may be necessary')
            elif cdn == 0:
                print('\n')
            start_time = ticks_ms()
            cdn -= 1

def getReady():
    '''
    @brief Gives three ready statements as a buffer before calibration
    @details Prints three strings in a 3 second interval in order to inform the user

    '''
    start_time = ticks_ms()
    cdn = 3 # countdown number
    while cdn >= 0:
        round_time = ticks_ms()
        if ((ticks_diff(round_time,start_time)) > 1000):
            if cdn == 3:
                print('Get ready')
            elif cdn == 2:
                print('Get set')
            elif cdn == 1:
                print('Calibrate')
            elif cdn == 0:
                print('\n')
            start_time = ticks_ms()
            cdn -= 1