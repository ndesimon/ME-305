"""!
@file MTask5.py
@brief Allows control of individual motors.  
@details This task allows users to control the speed of individual motors either by
         accepting user-inputted duty cycles from the UTask or by accpeting them from 
         the CTask.  
         
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
S1_WAIT = micropython.const (1)


def motorFunction(taskName, period, motor, dutyVal):
    '''! @brief Generator function that passes the duty cycles to the motor.
         @details This function passes the duty cycle to the method setduty which then
                  sends the value to the motor. 
         @param taskName Names the task so that multiple tasks can be run simultaneously.
         @param period Passes in the period at which the code is run.
         @param motor A shared parameter that indicates which motor to work with.
         @param dutyVal A shared parameter that indicates the value of th duty cycle.   
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
    
    ## @brief Generalizes the motor parameter
    #  @details Allows this task to be used for multiple motors simultaneously
    #
    motorNum = motor
     
    while True:
    
        ## @brief creates a variable called current_time
        #  @details Variable set to ticks_us() within the loop to continue to set
        #           a new time stamp.
        #
        current_time = ticks_us()
        if ticks_diff(current_time, next_time) >= 0:
            
            if state == S0_INIT:
                state = S1_WAIT                
                
            elif state == S1_WAIT:
                motorNum.set_duty(dutyVal.read())
                    
            else:
                pass
            
            next_time = ticks_add(next_time, period)
                
            yield state

        else:
            
            yield None