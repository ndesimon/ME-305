"""!
@file IMUTask.py
@brief Determines actuation for motor control
@details This task computes the actuation for motors.  It receives desired velocity 
         values from the UTask, measured velocity values from the ETask, and sends 
         the required duty cycle to the MTask.  
         
         See source code:
         https://bitbucket.org/bbartl01/mechatronics-labs/src/master/Lab4/CTask.py
         
@author Baxter Bartlett
@author Nick DeSimone
@author Miles Ibarra
@date 03-03-22
"""
   
from time import ticks_us, ticks_ms, ticks_add, ticks_diff
import micropython
import os
import gc

## @brief Creates a state called S0_INIT
#  @details Variable will be the state 0 for starting the program
#
S0_INIT = micropython.const(0)

## @brief Creates a state called S1_RUN
#  @details Variable will be the state 1 for reading and wriing values
#
S1_RUN = micropython.const (1)

S2_CALIB = micropython.const (2)

S3_SAVE_CAL_COEFFS = micropython.const (3)

S4_WRITE_CAL_COEFFS = micropython.const (4)

def bnoFunction(taskName, period, calStat, bno_obj, eulAng, gyrVel):
    '''! @brief Generator function that passes the duty cycles to the motor.
         @details This function passes the duty cycle to the method setduty which then
                  sends the value to the motor. 
         @param taskName Names the task so that multiple tasks can be run simultaneously.
         @param period Passes in the period at which the code is run.
         @param calStat A tuple containing 
         @param bno_obj 
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
    
    ## @brief creates an object of the BNO driver class
    #  @details 
    #
    BNO = bno_obj
    
    filename = "IMU_cal_coeffs.txt"
    
    filestring = ''
    
    n = 0
     
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
                    
                    print('--- IMU Calibration Interface ---')
                    print('To calibrate the BNO055 IMU, you will need to rotate'
                          'the platform about its center axis until all 4' 
                          'parameters, mag, acc, gyr, and sys have a value of'
                          '3.')
                    print('Be ready to calibrate in 3 seconds')
                    BNO.change_mode(12)
                    getReady()
                    state = S2_CALIB
                                
                
            elif state == S1_RUN:                
                eulAng.write(BNO.get_euler())
                head, pitch, roll = eulAng.read()
#                print('head: ' +str(head), 'pitch: ' +str(pitch), 'roll: ' +str(roll))
                gyrVel.write(BNO.get_omega())
                gyr_x,gyr_y,gyr_z = gyrVel.read()
#                print('ang_vel_x: ' +str(gyr_x), 'ang_vel_y: ' +str(gyr_y), 'ang_vel_z: ' +str(gyr_z))
                
                
                    
            elif state == S2_CALIB:
                calStat.write(BNO.get_cal_status())
                mag, acc, gyr, sys = calStat.read()
                print('mag: ' +str(mag), 'acc: ' +str(acc), 'gyr: ' +str(gyr), 
                      'sys: ' +str(sys))
                if (mag,acc,gyr,sys) == (3,3,3,3):  
                    print('--- End Calibration ---')
                    print('s2 -> s3')
                    state = S3_SAVE_CAL_COEFFS
                    
            elif state == S3_SAVE_CAL_COEFFS:    
                with open(filename, 'w') as f:
                    # Perform manual calibration
                    buf = bytearray(22*[0])
                    gc.collect()
                    cal_co_barr = BNO.get_cal_coeff(buf)
                    print(cal_co_barr)
                    
                    for byte in cal_co_barr:
                        filestring += hex(byte)
                        filestring += ','
                        n += 1
                                                   
                    if n == 22:
                        print(filestring)
                        print('writing to file')
                        filestring = filestring[:-1]
                        f.write(filestring)
                        state = S1_RUN
                        print('s3 -> s1')
                        
            elif state == S4_WRITE_CAL_COEFFS:
                    
                with open(filename, 'r') as f:
                    # Read the first line of the file
                    cal_data_string = f.readline()
                    # Split the line into multiple strings
                    # and then convert each one to a float
                    cal_values = bytearray([int(cal_value) for cal_value in cal_data_string.strip().split(',')])
                    print(cal_values)
                    BNO.change_mode(0)
                    BNO.set_cal_coeff(cal_values)
                state = S1_RUN
                print('s4 -> s1')
                BNO.change_mode(12)
                    
            
            else:
                pass
            
            next_time = ticks_add(next_time, period)
                
            yield state

        else:
            
            yield None
            

def getReady():
    '''
    @brief Gives three ready statements as a buffer before calibration

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