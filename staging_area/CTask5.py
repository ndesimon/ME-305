"""!
@file CTask5.py
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
   
from time import ticks_us, ticks_add, ticks_diff
import micropython

## @brief Creates a state called S0_INIT
#  @details Variable will be the state 0 for starting the program
#
S0_INIT = micropython.const(0)

## @brief Creates a state called S1_RUN_OUTER
#  @details Variable will be the state for running the outer loop
#
S1_RUN_OUTER = micropython.const (1)

## @brief Creates a state called S2_RUN_INNER
#  @details Variable will be the state for running the inner loop
#
S2_RUN_INNER = micropython.const (2)

def loopFunction(taskName, period, CLC_OUT, CLC_IN, eulAng, wFlag, KpShare, KdShare, KiShare, KpOut, KdOut, KiOut, duty, gyrVel, numEul, numGyr, dFlag, DFlag, abfShare, posIdx, velIdx, RefVal, yFlag):
    '''! @brief ClosedLoop function that passes the values for closed loop control.
         @details This function passes the euler angles, angular velocities, gain values, and flags to 
                  read and write the values used in closed loop control.
         @param taskName Names the task so that multiple tasks can be run simultaneously.
         @param period Passes in the period at which the code is run.
         @param CLC_OUT A shared parameter that indicates the outer loop reference angle limits.
         @param CLC_IN A shared parameter that indicates the inner loop saturation limits.
         @param eulAng A tuple containing the angular position for x,y,z.
         @param wFlag A shared parameter that indicates if the closed loop control keys have been pressed.
         @param KpShare A shared parameter that indicates the gain value Kp for the inner loop.
         @param KdShare A shared parameter that indicates the gain value Kd for the inner loop.
         @param KiShare A shared parameter that indicates the gain value Ki for the inner loop.
         @param KpOut A shared parameter that indicates the gain value Kp for the outer loop.
         @param KdOut A shared parameter that indicates the gain value Kd for the outer loop.
         @param KiOut A shared parameter that indicates the gain value Ki for the outer loop.
         @param duty A shared parameter that indicates the value of the duty cycle for the motor.
         @param gyrVel A tuple the angular velocities for x,y,z.
         @param numEul An input parameter for angles to determine if we are in the x or y axis for platform.
         @param numGyr An input parameter for angular velocities to determine if we are in the x or y axis for the platform.
         @param dFlag A shared parameter that indicates if the value for duty cycle of motor 1 are wanted.
         @param DFlag A shared parameter that indicates if the value for duty cycle of motor 2 are wanted.
         @param abfshare A shared parameter that indicates the position and velocities of the ball for filtering.
         @param posIdx An input parameter for the position to determine if we are in the x or y axis for the ball.
         @param velIdx An input parameter for the velocities to determine if we are in the x or y axis for the ball.
         @param RefVal A shared parameter that indicates the value of the reference velocity.
         @param yFlag A shared parameter that indicates if the set motor angle control keys have been pressed.
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
    
    ## @brief creates a variable called duty_val
    #  @details Variable set to be the value of duty passed in from main
    #
    duty_val = duty
     
    while True:
    
        ## @brief creates a variable called current_time
        #  @details Variable set to ticks_us() within the loop to continue to set
        #           a new time stamp.
        #
        current_time = ticks_us()
        if ticks_diff(current_time, next_time) >= 0:
            
            if state == S0_INIT:                
                state = S1_RUN_OUTER     
                
                    
                
            elif state == S1_RUN_OUTER:                
                if wFlag.read():
                    #Run outer                    
                    CLC_OUT.set_Gain(KpOut.read(), KdOut.read(), KiOut.read())
#                    CLC.OUT.set_Reference(RefVal.read())
                    act_sig_out = CLC_OUT.run(abfShare.read()[posIdx], abfShare.read()[velIdx], 0, 0, abfShare.read()[4])
                    if not yFlag.read():
                        RefVal.write(act_sig_out)
                    state = S2_RUN_INNER

                        
            elif state == S2_RUN_INNER:
                CLC_IN.set_Gain(KpShare.read(), KdShare.read(), KiShare.read())
#                CLC_IN.set_Reference(RefVal.read())
                act_sig = CLC_IN.run(eulAng.read()[numEul], gyrVel.read()[numGyr], RefVal.read(), 1, 1)                    
                duty_val.write(act_sig)
                if dFlag.read():
                    if wFlag.read():
                        if taskName == 'Task Motor Control 1':
                            print(f'{taskName}: {act_sig}')
                            dFlag.write(False)
                if DFlag.read():
                    if wFlag.read():
                        if taskName == 'Task Motor Control 2':
                            print(f'{taskName}: {act_sig}')
                            DFlag.write(False)
                state = S1_RUN_OUTER 
                
            else:
                pass
            
            next_time = ticks_add(next_time, period)
                
            yield state

        else:
            
            yield None