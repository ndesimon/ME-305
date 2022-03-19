"""!
@file ETask.py
@brief Obtains data from the encoder.
@details Constantly collects position, time, delta, and velocity values from the encoder.
         The state transition diagram for this task is depicted below:
         @image html ETaskSTD3.png width=500px
         
         See source code:
         https://bitbucket.org/bbartl01/mechatronics-labs/src/master/Lab3/ETask.py
         
@author Baxter Bartlett
@author Nick DeSimone
@author Miles Ibarra
@date 02-17-22
"""
   
from time import ticks_us, ticks_add, ticks_diff, ticks_ms
import micropython
#import encoder
#import pyb

## @brief Creates a state called S0_INIT
#  @details Variable will be the state 0 for starting the program
#
S0_INIT = micropython.const(0)

## @brief Creates a state called S1_UPDATE
#  @details Variable will be the state 1 for updating the program
#
S1_UPDATE = micropython.const (1)

## @brief Creates a state called S2_ZERO
#  @details Variable will be the state 2 for zeroing the program
#
S2_ZERO = micropython.const(2)

def updateFunction(taskName, period, zFlag, encData, ENC1, deltaTime, CLC):
    '''! @brief Updates and zeros the encoder.
         @details Collects all values from the encoder.
         @param taskName Names the task so that multiple tasks can be run simultaneously.
         @param period Passes in the period at which the code is run.
         @param zFlag A shared parameter that indicates if the 'z' key has been pressed.
         @param encData A tuple containing time, position, and delta of the encoder.
         @param ENC1 passes in the values from the encoder module.
    '''
    
    ## @brief creates a variable called state
    #  @details Variable will be used for setting the states
    #
    state = S0_INIT
    
    ## @brief creates a variable called start_time
    #  @details Variable set to be the starting time in micro seconds
    #
    start_time = ticks_us()
    
    #previous_time = ticks_us()
    
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
                state = S1_UPDATE
                
            elif state == S1_UPDATE:
                ENC1.update()
                encData.write((ticks_ms(), ENC1.get_position(), ENC1.get_delta(), ENC1.get_vel(), CLC.get_Actuation()))
                deltaTime.write(ENC1.get_deltaTime())
                if zFlag.read():        
                    state = S2_ZERO
                    
            elif state == S2_ZERO:
                ENC1.zero()
                zFlag.write(False)
                state = S1_UPDATE
                
            else:
                pass
            next_time = ticks_add(next_time, period)
                
            yield state
        else:
            
            yield None
