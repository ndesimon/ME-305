"""!
@file lab2_UTask.py
@brief Creates the UserInterface of the program
@details The User Interface lists all possible quantities and ways that the user
         can interact with the encoder.
         The state transition diagram for this task is depicted below:
         @image html UTaskSTD.png width=500px
         
         See source code:
         https://bitbucket.org/bbartl01/mechatronics-labs/src/master/Lab2/lab2_UTask.py
   
@author Baxter Bartlett
@author Nick DeSimone
@author Miles Ibarra
@date 02-03-22
"""

from pyb import USB_VCP
from time import ticks_us, ticks_add, ticks_diff
import micropython
import array

## @brief Creates a state called S0_INIT
#  @details Variable will be the state 0 for starting the program
#
S0_INIT = micropython.const(0)

## @brief Creates a state called S1_CMD
#  @details Variable will be the state 1 for updating the program
#
S1_CMD = micropython.const (1)

## @brief Creates a state called S2_ZERO
#  @details Variable will be the state 2 for zeroing the program
#
S2_ZERO = micropython.const(2)

## @brief Creates a state called S3_COLLECT
#  @details Variable will be the state 3 for collecting data
#
S3_COLLECT = micropython.const(3)

## @brief Creates a state called S4_PRINT_DATA
#  @details Variable will be the state 4 for printing data.
#
S4_PRINT_DATA = micropython.const(4)

def taskUserFCN(taskName, period, zFlag, encData):
    
    '''! @brief Creates the user interface.
         @details This function creates the inputs that gets the code to run accordingly.
         @param taskName Names the task so that multiple tasks can be run simultaneously.
         @param period Passes in the period at which the code is run.
         @param zFlag A shared parameter that indicates if the 'z' key has been pressed.
         @param encData A tuple containing time, position, and delta of the encoder.  
    '''
    
    ## @brief creates a variable called state
    #  @details Variable will be used for setting the states
    #
    state = S0_INIT
    
    ## @brief creates a variable called start_time
    #  @details Variable will be used for setting the time to micro seconds
    #
    start_time = ticks_us()
    
    
    ## @brief creates a variable called next_time
    #  @details Variable will be used for adding the start_time to the period
    #
    next_time = ticks_add(start_time, period)
    
    ## @brief creates a variable called ser
    #  @details Variable will be used for recognzing the keyboard input
    #
    ser = USB_VCP()
    
    ## @brief creates a variable called maxItems
    #  @details Variable will be used for setting the max items in the list
    #
    maxItems = 3001
    
    ## @brief creates a variable called timeArray
    #  @details Array will be used as an array for the time values
    #
    timeArray = array.array('l', maxItems*[0])
    
    ## @brief creates an array called posArray
    #  @details Array will be used as an array for the position values
    #
    posArray = array.array('l', maxItems*[0])
    
    ## @brief creates a variable called numItems
    #  @details Variable will be used for setting the number items in the list
    #
    numItems = 0
    
    ## @brief creates a variable called numPrint
    #  @details Variable will be used for setting the printed items in the list
    #
    numPrint = 0 
    
    while True:
        
        ## @brief creates a variable called current_time
        #  @details Variable will be used for setting the time to micro seconds within the while loop
        #
        current_time = ticks_us()
        
        if ticks_diff(current_time, next_time) >= 0:
 
            if state == S0_INIT:
                printHelp()
                state = S1_CMD
                
            elif state == S1_CMD:
                if ser.any():
                    ## @brief creates a variable called char_In
                    #  @details Variable will be used for reading the character inputted by the 
                    #           keyboard
                    #
                    charIn = ser.read(1).decode()
                    
                    if charIn == 'z':
                        state = S2_ZERO
                        print('Zeroing encoder...')
                        zFlag.write(True)                
                    elif charIn == 'p':
                        ## @brief creates a variable called encPos
                        #  @details Variable will be used for passing in the position value
                        #           from encData
                        #
                        encPos = encData.read()[1]
                        print(f'Encoder Position: {encPos}')                                         
                    elif charIn == 'd':
                        ## @brief creates a variable called encDelta
                        #  @details Variable will be used for passing in the delta value
                        #           from encData
                        #
                        encDelta = encData.read()[2]
                        print(f'Encoder Delta: {encDelta}')                       
                    elif charIn == 'g':
                        print('Collecting data...')
                        state = S3_COLLECT
                        numItems = 0    
                        numPrint = 0

                    else: 
                        print('Invalid character entered. Please try again.')
                        
            elif state == S2_ZERO:
                if not zFlag.read():
                    print('Encoder Zeroed')
                    state = S1_CMD
                    
            elif state == S3_COLLECT:        
                
                if numItems < maxItems:
                    timeArray[numItems],posArray[numItems],deltaDummy = encData.read()
                    numItems += 1              
                    if ser.any():
                        charIn = ser.read(1).decode()
                        if charIn == 's':
                            state = S4_PRINT_DATA
                            print('Ending Data Collection Early')
                    if numItems == maxItems:
                        state = S4_PRINT_DATA
                        
            elif state == S4_PRINT_DATA:
                if numPrint < numItems:
                    print(f'{((timeArray[numPrint]-timeArray[0])/1000):.2f}, {(posArray[numPrint]):.2f}')
                    numPrint += 1
                elif numPrint == numItems:
                    state = S1_CMD
                    
                
                
            else:
                raise ValueError(f'Invalid State in {taskName}')
            
            next_time = ticks_add(next_time, period)
            
            yield state
                
        else:
            yield None

def printHelp():
    
    '''! @brief Creates the User Interface Display
         @details Creates a stylsh display with all possible ways for user to
                  interact with the encoder.
    '''
    # Welcome instructions printed to Putty terminal on start-up
    print('+-----------------------------------------------------------+')
    print('|                  Welcome to UserUI                        |')
    print('|                                                           |')
    print('| Encoder Commands:                                         |')
    print('| 1. "z": Reset Encoder 1 position to 0                     |')
    print('| 2. "p": Get current Encoder 1 position                    |')
    print('| 3. "d": Get current Encoder 1 delta                       |')
    print('| 4. "g": Collect Encoder 1 data for 30 seconds             |')
    print('| 5. "s": End Encoder 1 data collection prematurely         |')
    print('|                                                           |')
    print('|    (Data will show on screen at the end of collection)    |')
    print('|                                                           |')
    print('+-----------------------------------------------------------+')
