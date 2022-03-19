"""!
@file main.py
@brief Runs all the tasks.  
@details This file runs all the tasks and classes necessary to run the user interface.  
         
         See source code:
         https://bitbucket.org/bbartl01/mechatronics-labs/src/master/Lab2/main.py
         
@author Baxter Bartlett
@author Nick DeSimone
@author Miles Ibarra
@date 03-18-22
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
import TTask
import touchpad
from pyb import Pin

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

# @brief Share variable for calibration status.
# @details The tuple contains the values for the mag, gyro, accel, and system.
#
calStat = shares.Share((0,0,0,0))

# @brief Share variable for euler angles.
# @details The tuple contains the values for the angles in the x,y,z directions.
#
eulAng = shares.Share((0,0,0))

# @brief Share variable for angular velocities.
# @details The tuple contains the values for the angular velocities in the x,y,z directions.
#
gyrVel = shares.Share((0,0,0))

## @brief Share variable for Kp for inner loop
#  @details Shares user input Kp values to inner loop control
#
KpShare = shares.Share(0)

## @brief Share variable for Kd for inner loop
#  @details Shares user input Kd values to inner loop control
#
KdShare = shares.Share(0)

## @brief Share variable for Ki for inner loop
#  @details Shares user input Ki values to to inner loop control
#
KiShare = shares.Share(0)

## @brief Share variable for Kp for outer loop
#  @details Shares user input Kp values to to outer loop control
#
KpOut = shares.Share(0)

## @brief Share variable for Kd for outer loop
#  @details Shares user input Kd values to to outer loop control
#
KdOut = shares.Share(0)

## @brief Share variable for Ki for outer loop
#  @details Shares user input Ki values to to outer loop control
#
KiOut = shares.Share(0)

## @brief Share variable for the desired angle for motor 1
#  @details Allows the user to set the reference angle for motor 1
#
yShare = shares.Share(0)

## @brief Share variable for the desired angle for motor 2
#  @details Allows the user to set the reference angle for motor 2
#
YSHARE = shares.Share(0)

## @brief Flag determining whether 'y' or Y has been pressed
#  @details Used for switching between closed loop control determined by location
#           of ball and closed loop control determined by user input
#
yFlag = shares.Share(False)

## @brief Share variable for initiation of closed loop control
#  @details Communicates to other tasks whether user has selected closed 
#           loop control of motor.
#
wFlag = shares.Share(False)

## @brief Share variable for printing the duty cycle 1
#  @details Communicates that the value of duty cycle motor 1 is desired to be printed
#
dFlag = shares.Share(False)

## @brief Share variable for printing the duty cycle 2
#  @details Communicates that the value of duty cycle motor 2 is desired to be printed
#
DFlag = shares.Share(False)

# @brief Share variable for position.
# @details The tuple contains the values for the x,y,z positions of the touch pad.
#
Pos = shares.Share((0,0,0))

# @brief Share variable for abfiltering.
# @details The tuple contains the values for the positions and velocities of the ball.
#
abfShare = shares.Share((0,0,0,0,0))

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

# @brief Object for the BNO055 class of the BNO055 module that instantiates values.
# @details This object pulls in the euler angles and omegas to be used in IMUTask
#
bno_obj = BNO055.BNO055()

# @brief Object for the Touchpad class of the touchpad module.
# @details This object instatiates values for the pins and dimensions of the touchpad
#
touch = touchpad.Touchpad(Pin.cpu.A7, Pin.cpu.A1, Pin.cpu.A6, Pin.cpu.A0, 176, 100)

# @brief Object for the ClosedLoop class of the closedloop5 module.
# @details This object instatiates values for the outer loop control of motor 1
#
CLC_O1 = closedloop5.ClosedLoop(0, 0, 0, yShare, 12, -12)

# @brief Object for the ClosedLoop class of the closedloop5 module.
# @details This object instatiates values for the outer loop control of motor 2
#
CLC_O2 = closedloop5.ClosedLoop(0, 0, 0, yShare, 12, -12)

# @brief Object for the ClosedLoop class of the closedloop5 module.
# @details This object instatiates values for the inner loop control of motor 1
#
CLC_I1 = closedloop5.ClosedLoop(0, 0, 0, yShare, 45, -45)

# @brief Object for the ClosedLoop class of the closedloop5 module.
# @details This object instatiates values for the inner loop control of motor 2
#
CLC_I2 = closedloop5.ClosedLoop(0, 0, 0, yShare, 45, -45)

if __name__ == '__main__':
    
    ## @brief Creates a list of tasks to be computed simultaneously.
    #  @details Contains the tasks that are used to run the User Interface.
    #           The tasks run in a cooperative fashion.       
    #
    taskList = [UTask5.taskUserFCN ('Task User', 50_000, eulAng, gyrVel, duty1, duty2, KpShare, KdShare, KiShare, KpOut, KdOut, KiOut, wFlag, dFlag, DFlag, abfShare, yShare, YSHARE, yFlag),
                #ETask5.updateFunction ('Task Encoder', 10_000, zFlag, encData, ENC1, deltaTime, CLC),
                MTask5.motorFunction ('Task Motor 1', 10_000, motor_1, duty1),
                MTask5.motorFunction ('Task Motor 2', 10_000, motor_2, duty2),
                #STask4.safetyFunction('Task Safety', 10_000, motor_drv, cFlag, eFlag),
                CTask5.loopFunction('Task Motor Control 1', 10_000, CLC_O1, CLC_I1, eulAng, wFlag, KpShare, KdShare, KiShare, KpOut, KdOut, KiOut, duty1, gyrVel, 1, 1, dFlag, DFlag, abfShare, 0, 1, yShare, yFlag),
                CTask5.loopFunction('Task Motor Control 2', 10_000, CLC_O2, CLC_I2, eulAng, wFlag, KpShare, KdShare, KiShare, KpOut, KdOut, KiOut, duty2, gyrVel, 2, 0, dFlag, DFlag, abfShare, 2, 3, YSHARE, yFlag),
#                CTask5.loopFunction('Task Inner Loop 1', 10_000, kFlag, CLC, eulAng, wFlag, KpShare, KdShare, KiShare, yShare, duty1, gyrVel, 1, 1, dFlag),
#                CTask5.loopFunction('Task Inner Loop 2', 10_000, kFlag, CLC, eulAng, wFlag, KpShare, KdShare, KiShare, yShare, duty2, gyrVel, 2, 0, dFlag),

                IMUTask.bnoFunction('Task IMU', 10_000, calStat, bno_obj, eulAng, gyrVel),
                TTask.TouchpadFunction('Task Touchpad', 10_000, Pos, touch, 0.85, 0.005, abfShare)]
    
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