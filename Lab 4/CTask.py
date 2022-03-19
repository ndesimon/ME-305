"""!
@file CTask.py
@brief Determines actuation for motor control
@details This task computes the actuation for motors.  It receives desired velocity 
         values from the UTask, measured velocity values from the ETask, and sends 
         the required duty cycle to the MTask.  
         
         See source code:
         https://bitbucket.org/bbartl01/mechatronics-labs/src/master/Lab4/CTask.py
         
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

## @brief Creates a state called S1_RUN
#  @details Variable will be the state 1 for reading and wriing values
#
S1_RUN = micropython.const (1)

def loopFunction(taskName, period, kFlag, CLC, encData, wFlag, KpVal,KiVal, RefVal, duty1, deltaTime):
    '''! @brief Generator function that passes the duty cycles to the motor.
         @details This function passes the duty cycle to the method setduty which then
                  sends the value to the motor. 
         @param taskName Names the task so that multiple tasks can be run simultaneously.
         @param period Passes in the period at which the code is run.
         @param kFlag A shared parameter that indicates if the 'k' key has been pressed.
         @param CLC A shared parameter that indicates the gain and duty values.
         @param encdata A tuple containing time, position, and delta of the encoder.
         @param wFlag A shared parameter that indicates if the closed loop control keys have been pressed.
         @param KpVal A shared parameter that indicates the gain value Kp.
         @param KiVal A shared parameter that indicates the gain value Ki.
         @param RefVal A shared parameter that indicates the value of the reference velocity.
         @param duty1 A shared parameter that indicates the value of the duty cycle for motor 1.
         @param deltaTime A tuple containing time, position, and delta of the encoder.
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
    
    ## @brief creates a variable called controller
    #  @details Variable set to be the values of gain and duty cycle passed in
    #           from closed loop
    #
    controller = CLC
     
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