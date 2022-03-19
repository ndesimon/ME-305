"""!
@file UTask5.py
@brief Creates the UserInterface of the program
@details The User Interface lists all possible ways in which the user can interact 
         with the balancing platform.  
         
         See source code:
         https://bitbucket.org/bbartl01/mechatronics-labs/src/master/Lab3/UTask.py
   
@author Baxter Bartlett
@author Nick DeSimone
@author Miles Ibarra
@date 03-18-22
"""

from pyb import USB_VCP, UART, repl_uart
from time import ticks_us, ticks_ms, ticks_add, ticks_diff
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

## @brief Creates a state called S2_COLLECT
#  @details Variable will be the state 3 for collecting data
#
S2_COLLECT = micropython.const(2)

## @brief Creates a state called S3_PRINT_DATA
#  @details Variable will be the state 4 for printing data.
#
S3_PRINT_DATA = micropython.const(3)

## @brief Creates a state called S4_DIGI_IN
#  @details Variable sets state where user inputs are evaluated as to whether
#           they are valid duty cycles
#
S4_DIGI_IN = micropython.const(4)

## @brief Variable that indicates whether 'y' has been pressed.
#  @details Used to determine that user has entered a setpoint in State 5.
#           Allows State 5 to be used for multiple things.  
#
#yPress = micropython.const(4)

## @brief Variable that indicates whether 'k' has been pressed.
#  @details Used to determine that user has entered a Kp for inner loop.  
#
kPress = micropython.const(5)

## @brief Variable that indicates whether 'k' has been pressed.
#  @details Used to determine that user has entered a Kd for inner loop.
#
kdPress = micropython.const(6)

## @brief Variable that indicates whether 'k' has been pressed.
#  @details Used to determine that user has entered a Ki for inner loop. 
#
kiPress = micropython.const(7)

## @brief Variable that indicates whether 'K' has been pressed.
#  @details Used to determine that user has entered a Kp for outer loop. 
#
KPRESS = micropython.const(8)

## @brief Variable that indicates whether 'K' has been pressed.
#  @details Used to determine that user has entered a Kd for outer loop. 
#
KDPRESS = micropython.const(9)

## @brief Variable that indicates whether 'K' has been pressed.
#  @details Used to determine that user has entered a Ki for outer loop. 
#
KIPRESS = micropython.const(10)

## @brief Variable that indicates whether 'y' has been pressed.
#  @details Used to determine that user has entered an angle for motor 1. 
#
yPress = micropython.const(11)

## @brief Variable that indicates whether 'Y' has been pressed.
#  @details Used to determine that user has entered an angle for motor 2. 
#
YPRESS = micropython.const(12)

def taskUserFCN(taskName, period, eulAng, gyrVel, duty1, duty2, KpShare, KdShare, KiShare, KpOut, KdOut, KiOut, wFlag, dFlag, DFlag, abfShare, yShare, YSHARE, yFlag):
    
    '''! @brief Creates the user interface.
         @details Creates the many functionalities required.  Motor can be controlled and data
                  can be collected.  User is prompted as to what inputs are valid.
         @param taskName Names the task so that multiple tasks can be run simultaneously.
         @param period Passes in the period at which the code is run.
         @param eulAng A tuple containing Euler angles head, pitch, and roll.
         @param gyrVel A tuple containing angular velocity about X,Y, and Z.
         @param duty1 A shared parameter that passes in the value for the duty cycle of motor 1.
         @param duty2 A shared parameter that passes in the value for the duty cycle of motor 2.
         @param Kpshare A shared parameter that passes in the value for the gain of Kp.
         @param KdShare A shared parameter that indicates the gain value Kd for the inner loop.
         @param Kishare A shared parameter that passes in the value for the gain of Ki.
         @param KpOut A shared parameter that indicates the gain value Kp for the outer loop.
         @param KdOut A shared parameter that indicates the gain value Kd for the outer loop.
         @param KiOut A shared parameter that indicates the gain value Ki for the outer loop.
         @param wFlag A shared parameter that indicates if the closed loop control keys have been pressed.
         @param dFlag A shared parameter that indicates if the value for duty cycle of motor 1 is wanted.
         @param DFlag A shared parameter that indicates if the value for duty cycle of motor 2 is wanted.
         @param abfshare A shared parameter that indicates the position and velocities of the ball for filtering.
         @param yShare A shared parameter that passes in the value set motor angle 1.
         @param YSHARE A shared parameter that passes in the value set motor angle 2.
         @param yFlag A shared parameter that indicates if the set motor angle control keys have been pressed.
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
    
    uart = UART(2, 115200)
    repl_uart(None)
    uart.write('Hello computer\r\n')
    
    ## @brief creates a variable called maxItems
    #  @details Variable will be used for setting the max items in the list
    #
    
    maxItems = 301
    
    ## @brief creates a variable called timeArray
    #  @details Array will be used as an array for the time values
    #
    timeArray = array.array('f', maxItems*[0])
    
    gc.collect()
    
    #Arrays used for the CSV data collection
    xArray = array.array('f', timeArray)
    vxArray = array.array('f', timeArray)
    gc.collect()
    yArray = array.array('f', vxArray)
    vyArray = array.array('f', vxArray)
    thxArray = array.array('f', vxArray)
    gc.collect()
    thyArray = array.array('f', thxArray)
    omxArray = array.array('f', thxArray)
    omyArray = array.array('f', thxArray)
    
    gc.collect()
    
    
    ## @brief creates a variable called numItems
    #  @details Variable will be used for setting the number items in the list
    #
    numItems = 0
    
    ## @brief creates a variable called numPrint
    #  @details Variable will be used for setting the printed items in the list
    #
    numPrint = 0 
    
    ## @brief creates the buffer used store inputted characters
    #  @details This buffer stores all user inputted characters and converts them
    #           to integers once the user hits "Enter".
    buf = ''
    
    filestring = ''
    
    nFile = 0
    
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
                    
                    if charIn in ['h', 'H']:
                        printHelp()              
                    
                    elif charIn in ['p', 'P']:
                        ## @brief Prints Euler angles
                        #
                        head, roll, pitch = eulAng.read()
                        print(f'Heading: {head:.2f} [deg], Roll: {roll:.2f} [deg], Pitch: {pitch:.2f} [deg]')
                                        
                    
                    elif charIn == 'd':
                        dFlag.write(True)
                        
                    elif charIn == 'D':
                        DFlag.write(True)
                        
                    elif charIn in ['v', 'V']:
                        gyr_x,gyr_y,gyr_z = gyrVel.read()
                        print(f'Ang Vel X,Y,Z: {gyr_x:.2f} [rad/s], {gyr_y:.2f} [rad/s], {gyr_z:.2f} [rad/s]')
                    
                    elif charIn in ['c', 'C']:
                        print('Collecting data...')
                        state = S2_COLLECT
                        numItems = 0    
                        numPrint = 0
                        
                    elif charIn in ['w', 'W']:
                        if wFlag.read():
                            print('Closed-Loop Control Disabled')
                            wFlag.write(False)
                        else:
                            print('Closed-Loop Control Enabled')
                            wFlag.write(True)

                    elif charIn == 'k':
                        s = kPress
                        print('Enter Inner Loop Kp Gain Value')
                        state = S4_DIGI_IN
                        
                    elif charIn == 'K':
                        s = KPRESS
                        print('Enter Outer Loop Kp Gain Value')
                        state = S4_DIGI_IN
                        
                    elif charIn == 'y':
                        if not yFlag.read():
                            yFlag.write(True)
                        s = yPress
                        print('Enter desired angle for Motor 1.  ')
                        print('Note that angles outside the angle saturation limits are not permitted')
                        state = S4_DIGI_IN
                        
                    elif charIn == 'Y':
                        if not yFlag.read():
                            yFlag.write(True)
                        s = YPRESS
                        print('Enter desired angle for Motor 2.  ')
                        print('Note that angles outside the angle saturation limits are not permitted')
                        state = S4_DIGI_IN
                        
                    elif charIn in ['q', 'Q']:
                        if yFlag.read():
                            yFlag.write(False)
                            print('Ending direct angle control for both motors')
                        else:
                            print('Angle control has not been enabled to begin with')
                        
                    else: 
                        print('Invalid character entered. Please try again.  Press "h" to review the available inputs.')
                    
            elif state == S2_COLLECT:        
                if numItems < maxItems:
                    timeArray[numItems] = ticks_ms()
                    xArray[numItems], vxArray[numItems], yArray[numItems], vyArray[numItems], zDummy = abfShare.read()
                    thzDummy, thyArray[numItems], thxArray[numItems] = eulAng.read()
                    omxArray[numItems], omyArray[numItems], omzDummy = gyrVel.read()
#                    xArray[numItems], vxArray[numItems], yArray[numItems], vyDummy, zDummy = abfShare.read()
                    numItems += 1
                    if ser.any():
                        charIn = ser.read(1).decode()
                        if charIn == 's':
                            state = S3_PRINT_DATA
                            print('Ending Data Collection Early')
                    if numItems == maxItems:
                        state = S3_PRINT_DATA
                        
            elif state == S3_PRINT_DATA:
                with open('Data.csv', 'a+') as f:
                    if numPrint < numItems:
                        aC = round((timeArray[numPrint]-timeArray[0])/1000, 2)
                        bC = -round(xArray[numPrint], 2)
                        cC = -round(vxArray[numPrint], 2)
                        dC = round(yArray[numPrint], 2)
                        eC = round(vyArray[numPrint], 2)
                        fC = round(thxArray[numPrint], 2)
                        gC = round(omxArray[numPrint], 2)
                        hC = round(thyArray[numPrint], 2)
                        iC = round(omyArray[numPrint], 2)
                        data = [aC, bC, cC, dC, eC, fC, gC, hC, iC]
                        for x in data:
                            filestring += str(x)
                            filestring += ','
                            nFile += 1
                        if nFile == 9:
                            print(filestring)
                            f.write(filestring)
                            f.write('\n')
                            numPrint += 1
                            filestring = ''
                            nFile = 0
                    elif numPrint == numItems:
                        state = S1_CMD
            
            elif state == S4_DIGI_IN:
                if ser.any():
                    char = ser.read(1).decode()
                    if char.isdigit():
                        buf += char
                        ser.write(char)
                        uart.write(str(char)+ '\n')
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
                    elif char in {'\r','\n'}:
                        ser.write('\r\n')
                        if len(buf)==0:
                            pass
                        elif s == kPress:
                            Kp = float(buf)
                            KpShare.write(Kp)
                            buf = ''
                            print('Enter Inner Loop Kd Gain Value')
                            s = kdPress
                            
                        elif s == kdPress:
                            Kd = float(buf)
                            KdShare.write(Kd)
                            buf = ''
                            print('Enter Ki Gain Value')
                            s = kiPress
                                
                        elif s == kiPress:
                            Ki = float(buf)
                            KiShare.write(Ki)
                            buf = ''
                            s = 0
                            state = S1_CMD
                                
                        elif s == KPRESS:
                            KpO = float(buf)
                            KpOut.write(KpO)
                            buf = ''
                            print('Enter Outer Loop Kd Gain Value')
                            s = KDPRESS
                            
                        elif s == KDPRESS:
                            KdO = float(buf)
                            KdOut.write(KdO)
                            buf = ''
                            print('Enter Outer Loop Ki Gain Value')
                            s = KIPRESS
                            
                        elif s == KIPRESS:
                            KiO = float(buf)
                            KiOut.write(KiO)
                            #kINNER.write(Ki)[2]
                            #kINNER.write(Kp, Kd, Ki)
                            buf = ''
                            s = 0
                            state = S1_CMD
                            
                        elif s == yPress:
                            y = float(buf)
                            buf = '' 
                            s = 0                                                      
                            state = S1_CMD
                            yShare.write(y)
                            print('Press "k" if you have not yet entered inner loop gain values')
                            
                        elif s == YPRESS:
                            Y = float(buf)
                            buf = '' 
                            s = 0                                                      
                            state = S1_CMD
                            YSHARE.write(Y)
                            print('Press "k" if you have not yet entered inner loop gain values')
                    
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
    print('| Data Collection Commands:                                 |')
    print('| 1. "p or P": Print Euler Angles                           |')
    print('| 2. "d": Get current duty cycle supplied to motor 1        |')
    print('| 3. "D": Get current duty cycle supplied to motor 2        |')
    print('| 4. "v" or "V": Print Angular Velocities                   |')
    print('| 5. "c" or "C": Collect platform data for 15 seconds       |')
    print('| 6. "s" or "S": End platform data collection prematurely   |')
    print('|                                                           |')
    print('| Closed-Loop Commands:                                     |')
    print('| 1. "w": Enable/disable closed-loop control for Motor 1    |')
    print('| 2. "k": Enter inner closed loop gain values (Kp & Kd)     |')
    print('| 3. "K": Enter outer closed loop gain values (Kp, Kd, & Ki)|')
    print('| 4. "y": Directly control the angle of Motor 1             |')
    print('| 5. "Y": Directly control the angle of Motor 2             |')
    print('| 6. "q" or "Q": Stop directly controlling both motor angles|')
    print('|                                                           |')
    print('|      NOTES:                                               |')
    print('|      - Press "h" at any time to view this UserUI          |')
    print('|      - Data will show on screen at the end of collection  |')
    print('+-----------------------------------------------------------+')
