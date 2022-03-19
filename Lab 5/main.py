"""!
@file main.py
@brief Runs all the tasks.  
@details This file runs all the tasks and classes necessary to run the user interface.  
         
         See source code:
         https://bitbucket.org/bbartl01/mechatronics-labs/src/master/Lab2/main.py
         
@author Baxter Bartlett
@author Nick DeSimone
@author Miles Ibarra
@date 02-24-22
"""
#import ETask5
import UTask5
import MTask5
#import STask4
import CTask5
import IMUTask
import shares
import motor5
import BNO055
import closedloop5
from pyb import Pin

## @brief Character flag to allow if true the values to be zeroed.
#  @details This variable is used in conjunction with the shares class to enable 
#           the two tasks to communicate when to change states.  
#
zFlag = shares.Share(False)

## @brief Character flag to allow if true the values to be cleared and re enable motor.
#  @details This variable is used in conjunction with the shares class to enable 
#           the two tasks to communicate when to change states.  
#
cFlag = shares.Share(False)

## @brief Character flag to allow if true to re enable the motor.
#  @details This variable is used in conjunction with the shares class to enable 
#           the two tasks to communicate when to change states.  
#
eFlag = shares.Share(False)

## @brief Character flag to allow if true to set the Kp value.
#  @details This variable is used in conjunction with the shares class to enable 
#           the two tasks to communicate when to change states.  
#
kFlag = shares.Share(False)

# @brief Share variable for motor 1 duty cycle.
# @details The variable allows a value duty1 to read and write when filled
#          in the encoder module 
#
duty1 = shares.Share(0)

# @brief Share variable for motor 2 duty cycle.
# @details The variable allows a value duty2 to read and write when filled
#          in the encoder module 
#
duty2 = shares.Share(0)

## @brief Share variable for an encoder tuple
#  @details Creates a tuple containing time, position, delta, velocity, and 
#           duty cycle all obtained from the Encoder Task and CTask.
#
encData = shares.Share((0,0,0,0,0))

# tuple for calib status
calStat = shares.Share((0,0,0,0))

# tuple for euler angles
eulAng = shares.Share((0,0,0))

# tuple for gyr angular velocities
gyrVel = shares.Share((0,0,0))

## @brief Share variable for Kp
#  @details Shares user input Kp values to all necessary tasks
#
KpShare = shares.Share(0)

## @brief Share variable for Ki
#  @details Shares user input Ki values to all necessary tasks
#
KdShare = shares.Share(0)
KiShare = shares.Share(0)

## @brief Share variable for the setpoint
#  @details Shares user input setpoint values to all necessary tasks
#
yShare = shares.Share(0)

## @brief Share variable for initiation of closed loop control
#  @details Communicates to other tasks whether user has selected closed 
#           loop control of motor.
#
wFlag = shares.Share(False)
dFlag = shares.Share(False)

gain = shares.Share(0)

## @brief Share variable chnage in time between updates
#  @details Communicates to other tasks wthe chnage in time between updates.  
#           This is usd in the calculation of multiple quantities.  
#
deltaTime = shares.Share(0)

### @brief creates a variable called ENC1
##  @details Pushes forward the ENC1 variable from the encoder module
##
#ENC1 = encoder.Encoder(Pin.cpu.B6, Pin.cpu.B7, 4)

# @brief Object for the DRV8847 module.
# @details This object pulls in the timer and pins defined in the DRV8847 module 
#          and DRV8847 class
#
#motor_drv = DRV8847.DRV8847(3, Pin(Pin.cpu.A15, mode=Pin.OUT_PP), Pin(Pin.cpu.B2, mode=Pin.OUT_PP)) # Object of DRV8847 class

# @brief Object for the motor method of the DRV8847 class that instantiates the pins and channels.
# @details This object pulls in the pins and channels defined in the motor method 
#          to communicate with DRV8847
#
motor_1 = motor5.Motor(3, Pin.cpu.B4, Pin.cpu.B5, 1, 2)

# @brief Object for the motor method of the DRV8847 class that instantiates the pins and channels.
# @details This object pulls in the pins and channels defined in the motor method 
#          to communicate with DRV8847
#
motor_2 = motor5.Motor(3, Pin.cpu.B0, Pin.cpu.B1, 3, 4)

# bno driver object
bno_obj = BNO055.BNO055()


CLC = closedloop5.ClosedLoop (KpShare, KdShare, KiShare, yShare, 50, -50)



if __name__ == '__main__':
    
    ## @brief Creates a list of tasks to be computed simultaneously.
    #  @details Contains the two tasks that are used to run the User Interface.
    #           The two tasks run simultaneously.       
    #
    taskList = [UTask5.taskUserFCN ('Task User', 50_000, zFlag, eulAng, gyrVel, calStat, duty1, duty2, KpShare, KdShare, KiShare, yShare, wFlag, dFlag),
                #ETask5.updateFunction ('Task Encoder', 10_000, zFlag, encData, ENC1, deltaTime, CLC),
                MTask5.motorFunction ('Task Motor 1', 10_000, motor_1, duty1),
                MTask5.motorFunction ('Task Motor 2', 10_000, motor_2, duty2),
                #STask4.safetyFunction('Task Safety', 10_000, motor_drv, cFlag, eFlag),
                
                CTask5.loopFunction('Task Closed Loop 1', 10_000, kFlag, CLC, eulAng, wFlag, KpShare, KdShare, KiShare, yShare, duty1, gyrVel, 1, 1, dFlag),
                CTask5.loopFunction('Task Closed Loop 2', 10_000, kFlag, CLC, eulAng, wFlag, KpShare, KdShare, KiShare, yShare, duty2, gyrVel, 2, 0, dFlag),
                IMUTask.bnoFunction('Task IMU', 10_000, calStat, bno_obj, eulAng, gyrVel)]
    
    while True:
        try:
            for task in taskList:
                next(task)
        except KeyboardInterrupt:
            KpShare.write(0)
            KdShare.write(0)
            duty1.write(0)
            duty2.write(0)
            break
    print('Stopping Motor')