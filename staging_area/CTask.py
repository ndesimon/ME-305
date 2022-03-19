"""!
@file CTask.py
@brief Allows control of individual motors.  
@details This task allows users to control the speed of individual motors by receiving
         user-inputted duty cycles from the UTask.  
         The state transition diagram for this task is depicted below:
         @image html MTaskSTD3.png width=500px
         
         See source code:
         https://bitbucket.org/bbartl01/mechatronics-labs/src/master/Lab3/MTask.py
         
@author Baxter Bartlett
@author Nick DeSimone
@author Miles Ibarra
@date 02-24-22
"""
   
from time import ticks_us, ticks_add, ticks_diff
import micropython

## @brief Creates a state called S0_INIT
#  @details Variable will be the state 0 for starting the program
#
S0_INIT = micropython.const(0)

## @brief Creates a state called S1_WAIT
#  @details Variable will be the state 1 for waiting for the command
#
S1_RUN = micropython.const (1)

## @brief Creates a state called S2_CONTROLLER
#  @details Variable will be the state 1 for waiting for the command
#
S2_SET_GAIN = micropython.const (2)

## @brief Creates a state called S2_CONTROLLER
#  @details Variable will be the state 1 for waiting for the command
#
S3_SET_SETPOINT = micropython.const (3)


def loopFunction(taskName, period, kFlag, CLC, encData, wFlag, KpVal,KiVal, RefVal, duty1, deltaTime):
    '''! @brief Generator function that passes the duty cycles to the motor.
         @details This function passes the duty cycle to the method setduty which then
                  sends the value to the motor. 
         @param taskName Names the task so that multiple tasks can be run simultaneously.
         @param period Passes in the period at which the code is run.
         @param kFlag A shared parameter that indicates if the 'k' key has been pressed.
         @param CLC A shared parameter that indicates the value of th duty cycle.
         @param encdata A tuple containing time, position, and delta of the encoder.
         @param wFlag A shared parameter that indicates if the closed loop control keys have been pressed.
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
    
    controller = CLC
    #motorNum = motor
     
    while True:
    
        ## @brief creates a variable called current_time
        #  @details Variable set to ticks_us() within the loop to continue to set
        #           a new time stamp.
        #
        current_time = ticks_us()
        if ticks_diff(current_time, next_time) >= 0:
            
            if state == S0_INIT:
                state = S1_RUN                
                
            elif state == S1_RUN:                
                if wFlag.read():
                    controller.set_Gain(KpVal.read(), KiVal.read())
                    controller.set_Reference(RefVal.read())
                    act_sig = controller.run(encData.read()[3], deltaTime.read())
                    duty1.write(act_sig)
                    
            else:
                pass
            
            next_time = ticks_add(next_time, period)
                
            yield state

        else:
            
            yield None