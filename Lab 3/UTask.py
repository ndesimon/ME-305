"""!
@file UTask.py
@brief Creates the UserInterface of the program
@details The User Interface lists all possible quantities and ways that the user
         can interact with the encoder, motor, and DRV8847 modules.
         The state transition diagram for this task is depicted below:
         @image html UTaskSTD3.png width=500px
         
         See source code:
         https://bitbucket.org/bbartl01/mechatronics-labs/src/master/Lab3/UTask.py
   
@author Baxter Bartlett
@author Nick DeSimone
@author Miles Ibarra
@date 02-17-22
"""

from pyb import USB_VCP
from time import ticks_us, ticks_add, ticks_diff
import micropython
import array
import gc

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

## @brief Creates a state called S5_DIGI_IN
#  @details Variable sets state where user inputs are evaluated as to whether
#           they are valid duty cycles
#
S5_DIGI_IN = micropython.const(5)

## @brief Creates a state called S6_TESTING
#  @details Variable sets state where user inputs are collected to be tested and
#           used to find the average velocity in the next state.
#
S6_TESTING = micropython.const(6)

## @brief Creates a state called S7_DETERMINE_V_AVG
#  @details Variable sets state where user inputs are evaluated to find the 
#           average velocity of the data colleced
#
S7_DETERMINE_V_AVG = micropython.const(7)

## @brief Creates a state called S8_PRINT_TEST
#  @details Variable sets state where user inputs are printed. The duty value and
#           average velocity are printed to the user.
#
S8_PRINT_TEST = micropython.const(8)

mPress = micropython.const(1)
MPress = micropython.const(2)
tPress = micropython.const(3)

def taskUserFCN(taskName, period, zFlag, cFlag, eFlag, encData, duty1, duty2):
    
    '''! @brief Creates the user interface.
         @details Creates the many functionalities required.  Motor can be controlled and data
                  can be collected.  User is prompted as to what inputs are valid.
         @param taskName Names the task so that multiple tasks can be run simultaneously.
         @param period Passes in the period at which the code is run.
         @param zFlag A shared parameter that indicates if the 'z' key has been pressed.
         @param cFlag A shared parameter that indicates if the 'c' key has been pressed.
         @param eFlag A shared parameter that indicates if the 'e' key has been pressed.
         @param encData A tuple containing time, position, and delta of the encoder.  
         @param duty1 A shared parameter that passes in the value for the duty cycle of motor 1.
         @param duty2 A shared parameter that passes in the value for the duty cycle of motor 2.
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
    timeArray = array.array('f', maxItems*[0])
    
    gc.collect()
    
    ## @brief creates an array called posArray
    #  @details Array will be used as an array for the position values
    #
    posArray = array.array('f', timeArray)
    
    ## @brief creates a variable called vItems
    #  @details Sets number of velocity samples to take
    #
    vItems = 40
    
    ## @brief creates an array called velArray
    #  @details Array will be used as an array for the velocity values
    #
    velArray = array.array('f', timeArray)
    
    ## @brief creates a variable called vNum
    #  @details Index of velocity list
    #
    vNum = 0
    
    ## @brief creates a variable called testNum
    #  @details Index each time user tests the data
    #
    testNum = 0
    
    ## @brief creates a variable called ItemNum
    #  @details Index of the tested data once user is done testing
    #
    testItemNum = 0
    
    ## @brief creates a variable called numItems
    #  @details Variable will be used for setting the number items in the list
    #
    numItems = 0
    
    ## @brief creates a variable called numPrint
    #  @details Variable will be used for setting the printed items in the list
    #
    numPrint = 0 
    
    # Buffer containing inputted digits
    buf = ''
    
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
                    
                    if charIn in ['z', 'Z']:
                        state = S2_ZERO
                        print('Zeroing encoder...')
                        zFlag.write(True)                
                    
                    elif charIn in ['p', 'P']:
                        ## @brief creates a variable called encPos
                        #  @details Variable will be used for passing in the position value
                        #           from encData
                        #
                        encPos = encData.read()[1]
                        print(f'Encoder Position: {encPos:.2f} rad')                                         
                    
                    elif charIn in ['d', 'D']:
                        ## @brief creates a variable called encDelta
                        #  @details Variable will be used for passing in the delta value
                        #           from encData
                        #
                        encDelta = encData.read()[2]
                        print(f'Encoder Delta: {encDelta:.2f} rad')
                        
                    elif charIn in ['v', 'V']:
                        ## @brief creates a variable called enhgcfg
                        #  @details Variable will be used for passing in the delta value
                        #           from encData
                        #
                        encVel = encData.read()[3]
                        print(f'Encoder Velocity: {encVel:.2f} rad/s')
                    
                    elif charIn in ['g', 'G']:
                        print('Collecting data...')
                        state = S3_COLLECT
                        numItems = 0    
                        numPrint = 0
                        
                    elif charIn in ['c', 'C']:
                        print('Clearing fault...')
                        print('Re-enabling motor')
                        duty1.write(0)
                        duty2.write(0)
                        cFlag.write(True)

                    elif charIn in ['e', 'E']:
                        print('Enabling motors...')
                        duty1.write(0)
                        duty2.write(0)
                        eFlag.write(True)

                    elif charIn == 'm':
                        s = mPress
                        print('Enter Duty Cycle for Motor 1')
                        #state = S5_DUTY1
                        state = S5_DIGI_IN
                        
                    elif charIn == 'M':
                        s = MPress
                        print('Enter Duty Cycle for Motor 2')
                        #state = S6_DUTY2
                        state = S5_DIGI_IN
                        
                    elif charIn in ['t', 'T']:
                        state = S6_TESTING
                        dutyInput = []
                        v_avgList = []
                        testItemNum = 0
                        testNum = 0
                        
                    else: 
                        print('Invalid character entered. Please try again.')
                        
            elif state == S2_ZERO:
                
                if not zFlag.read():
                    print('Encoder Zeroed')
                    state = S1_CMD
                    
            elif state == S3_COLLECT:        
                
                if numItems < maxItems:
                    timeArray[numItems],posArray[numItems],deltaDummy,velArray[numItems] = encData.read()
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
                    print(f'{((timeArray[numPrint]-timeArray[0])/1000):.2f}, {(posArray[numPrint]):.2f}, {(velArray[numPrint]):.2f}')
                    numPrint += 1
                elif numPrint == numItems:
                    state = S1_CMD
            
            elif state == S5_DIGI_IN:
                if ser.any():
                    char = ser.read(1).decode()
                    if char.isdigit():
                        buf += char
                        ser.write(char)
                    elif char == '-':
                        if len(buf)==0:
                            buf += char
                            ser.write(char)
                        else:
                            pass
                    elif char == '.':
                        if '.' in buf:
                            pass
                        else:
                            buf += char
                            ser.write(char)
                    elif char in {'\b','\x08','\x7F'}:
                        if len(buf)==0:
                            pass
                        else:
                            buf = buf[0:-1]
                            ser.write(char)
                    elif char in {'s','S'}:
                        duty1.write(0)
                        state = S8_PRINT_TEST
                    elif char in {'\r','\n'}:
                        if len(buf)==0:
                            pass
                        else:
                            duty = int(buf)
                            if duty > 100:
                                duty = 100
                                print('Duty cannot be above 100%.  Setting duty to 100%')
                            elif duty < -100:
                                duty = -100
                                print('Duty cannot be below -100%.  Setting duty to -100%')
                            # If setting motor 1 duty   
                            if s == mPress:
#                                print('writing duty1 cycle')
#                                print('before writing d1')
#                                print(duty1.read())                                
                                duty1.write(duty)
                                print('')
#                                print('after writing d1')
#                                print(duty1.read())                                    
                                buf = ''
                                s = 0
                                state = S1_CMD
                                
                            # if setting motor 2 duty
                            elif s == MPress:
#                                print('writing duty2 cycle')
#                                print('before writing d2')
#                                print(duty2.read())                                
                                duty2.write(duty)
                                print('')
                                buf = ''
                                s = 0
                                state = S1_CMD
                                
                            elif s == tPress:
                                duty1.write(duty)
                                dutyInput.append(duty)
                                buf = ''
                                state = S7_DETERMINE_V_AVG
                                vNum = 0
                                vSum = 0
                                
            elif state == S6_TESTING:
                print('Enter a duty cycle for motor 1')
                s = tPress
                state = S5_DIGI_IN
                
            elif state == S7_DETERMINE_V_AVG:
                if vNum < vItems:
                    vSum += encData.read()[3]
                    vNum += 1
                else:
                    v_avg = vSum/vNum
                    print('')
                    print(f' At {duty}%, the average velocity is {v_avg} rad/s')
                    v_avgList.append(v_avg)
                    testNum += 1
                    state = S6_TESTING
                    
            elif state == S8_PRINT_TEST:
                if testItemNum < testNum:
                    print(f'{(dutyInput[testItemNum]):.2f}, {(v_avgList[testItemNum]):.2f}')
                    testItemNum +=1
                else:
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
    print('| 1. "z or Z": Reset Encoder 1 position to 0                |')
    print('| 2. "p or P": Get current Encoder 1 position               |')
    print('| 3. "d or D": Get current Encoder 1 delta                  |')
    print('| 4. "v or V": Get current velocity of Encoder 1            |')
    print('| 5. "g or G": Collect Encoder 1 data for 30 seconds        |')
    print('| 6. "s or S": End Encoder 1 data collection prematurely    |')
    print('|                                                           |')
    print('| Motor Commands:                                           |')
    print('| 1. "m": Prompt user to enter a duty cycle for Motor 1     |')
    print('| 2. "M": Prompt user to enter a duty cycle for Motor 2     |')
    print('| 3. "c" or "C" : Clear fault conditions                    |')
    print('| 4. "t or T": Enter testing interface of motor 1           |')
    print('| NOTE: Duty cycle values must be from -100 to +100         |')
    print('|                                                           |')
    print('|    (Data will show on screen at the end of collection)    |')
    print('+-----------------------------------------------------------+')
