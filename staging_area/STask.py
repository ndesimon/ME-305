"""!
@file STask.py
@brief Calls functions of the DRV8847 module.
@details This task enables all assigned motors when the user inputs a 'c' or an 's'
         into the UTask.  This task also disables all assigned motors if a fault
         condition is triggered.  
         @image html STaskSTD3.png width=500px
         
         See source code:
         https://bitbucket.org/bbartl01/mechatronics-labs/src/master/Lab3/STask.py
         
@author Baxter Bartlett
@author Nick DeSimone
@author Miles Ibarra
@date 02-17-22
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


def safetyFunction(taskName, period, motor_drv, cFlag, eFlag):
    '''! @brief Enables and disables motors.
         @details This is the function that controls enabling and disabling of the motors.  
         @param taskName Names the task so that multiple tasks can be run simultaneously.
         @param period Passes in the period at which the code is run.
         @param motor_drv Object that pulls in the pins and timer from the DRV8847 module.
         @param cFlag A shared parameter that indicates if the 'c' key has been pressed.
         @param eFlag A shared parameter that indicates if the 'e' key has been pressed.
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
    
    while True:
    
        ## @brief creates a variable called current_time
        #  @details Variable set to ticks_us() within the loop to continue to set
        #           a new time stamp.
        #
        current_time = ticks_us()
        if ticks_diff(current_time, next_time) >= 0:
            
            if state == S0_INIT:
                motor_drv.enable()
                state = S1_WAIT               
                
            elif state == S1_WAIT:
                
                # Clear motor faults if a 'c' is pressed
                if cFlag.read():
                    motor_drv.enable()
                    cFlag.write(False)
                
                # Enable motors if an 'e' is pressed
                if eFlag.read():
                    motor_drv.enable()
                    eFlag.write(False)
                
            else:
                pass
            next_time = ticks_add(next_time, period)
                
            yield state
        else:
            
            yield None