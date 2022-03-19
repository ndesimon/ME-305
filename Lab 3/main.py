"""!
@file main.py
@brief Runs all the tasks.  
@details This file runs all the tasks and classes necessary to run the user interface.  
         Task Diagram is depicted below:
         @image html taskDiagram3.png width=500px
         
         Find State Transition Diagram for the User Task in @ref UTask.py .  
         Find State Transition Diagram for the Encoder Task in @ref ETask.py .
         Find State Transition Diagram for the Motor Task in @ref MTask.py .
         Find State Transition Diagram for the Safety Task Task in @ref STask.py .
         
         See source code:
         https://bitbucket.org/bbartl01/mechatronics-labs/src/master/Lab2/main.py
         
@author Baxter Bartlett
@author Nick DeSimone
@author Miles Ibarra
@date 02-17-22
"""
import ETask
import UTask
import encoder
import MTask
import STask
import shares
import DRV8847
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
#  @details Creates a tuple containing time, position, delta, and velocity, all obtained
#           from the Encoder Task
#
encData = shares.Share((0,0,0,0))

## @brief creates a variable called ENC1
#  @details Pushes forward the ENC1 variable from the encoder module
#
ENC1 = encoder.Encoder(Pin.cpu.B6, Pin.cpu.B7, 4)

# @brief Object for the DRV8847 module.
# @details This object pulls in the timer and pins defined in the DRV8847 module 
#          and DRV8847 class
#
motor_drv = DRV8847.DRV8847(3, Pin(Pin.cpu.A15, mode=Pin.OUT_PP), Pin(Pin.cpu.B2, mode=Pin.OUT_PP)) # Object of DRV8847 class

# @brief Object for the motor method of the DRV8847 class that instantiates the pins and channels.
# @details This object pulls in the pins and channels defined in the motor method 
#          to communicate with DRV8847
#
motor_1 = motor_drv.motor(Pin.cpu.B4, Pin.cpu.B5, 1, 2)# Calling motor method in DRV8847 to comm with motor.py

# @brief Object for the motor method of the DRV8847 class that instantiates the pins and channels.
# @details This object pulls in the pins and channels defined in the motor method 
#          to communicate with DRV8847
#
motor_2 = motor_drv.motor(Pin.cpu.B0, Pin.cpu.B1, 3, 4)

# Enable the motors
motor_drv.enable()

if __name__ == '__main__':
    
    ## @brief Creates a list of tasks to be computed simultaneously.
    #  @details Contains the two tasks that are used to run the User Interface.
    #           The two tasks run simultaneously.       
    #
    taskList = [UTask.taskUserFCN ('Task User', 10_000, zFlag, cFlag, eFlag, encData, duty1, duty2),
                ETask.updateFunction ('Task Encoder', 10_000, zFlag, encData, ENC1),
                MTask.motorFunction ('Task Motor 1', 10_000, motor_1, duty1),
                MTask.motorFunction ('Task Motor 2', 10_000, motor_2, duty2),
                STask.safetyFunction('Task Safety', 10_000, motor_drv, cFlag, eFlag)]
    
    while True:
        try:
            for task in taskList:
                next(task)
        except KeyboardInterrupt:
            motor_drv.disable() 
            break
    print('Stopping Motor')