'''
@file           UI_Encoder_Task.property.py
@brief          User Interface on Putty Terminal
@details        Uses micro python VCP module to accept user inputs
                one character at a time. These user inputs command action
                by either the motors or encoders.
@author         Tyler McCue, Nick De Simone, Charlie Refvem (Reference)
@date           Oct 9, 2021
'''

import pyb
import utime


class UI():
    '''
    @brief      UI class that allows encoder to take user inputs
    @details    Uses micro python VCP module to accept user inputs
                for encoder

    '''

    def __init__(self, period):
        '''
        @brief          Constructor for UI driver
        @param period   Period of time at which user task runs, in sec
        '''
        ## Set input period equal to the frequency at which the user task will
        # run
        self.user_freq = period
        # Convert user task period from sec to microsec
        self.user_freq = int(self.user_freq*1E6)
        
        ## Assign VP communication for specified encoder
        # Allows for reading and writing of data over the USB connecting user 
        #   & Nucleo
        self.coms = pyb.USB_VCP()
        
        ## Initiate input variable associated with user key presses
        self.input = '0'
        
        ## Initiate state variable sent to encoder task
        self.state = 0
        
        ## Initiate gather flag, which enables the 30 sec data collection code
        self.gather = False
        
        ## Next_Time determines the time at which the user task will look for
        #  user inputs
        self.next_time = utime.ticks_add(utime.ticks_us(), self.user_freq)
        
        ## Initiate data list, which is filled with 30 sec of position and 
        #  delta values when a "g" is pressed
        self.data = []
        
        ## Initiate run variable that allows for 30 seconds of data collection
        self.run = -self.user_freq/1E6
        
        # Welcome instructions printed to Putty terminal on start-up
        print('+-----------------------------------------------------------+')
        print('|                  Welcome to EncoderUI                     |')
        print('|                                                           |')
        print('| Encoder Commands:                                         |')
        print('| 1. "z": Reset Encoder 1 position to 0                     |')
        print('| 2. "p": Get current Encoder 1 position                    |')
        print('| 3. "d": Get current Encoder 1 delta                       |')
        print('| 4. "g": Collect Encoder 1 data for 30 seconds             |')
        print('| 5. "s": End Encoder 1 data collection prematurely         |')
        print('|    (Data will show on screen at the end of collection)    |')
        print('| NOTE: For Encoder 2, press the capitalized version of the |')
        print('| above commands                                            |')
        print('|                                                           |')
        print('| Motor Commands:                                           |')
        print('| 1. "m": Prompt user to enter a duty cycle for Motor 1     |')
        print('| 2. "M": Prompt user to enter a duty cycle for Motor 2     |')
        print('| 3. "c" OR "C" : Clear fault conditions                    |')
        print('| NOTE: Duty cycle values must be from -100 to +100         |')
        print('|                                                           |')
        print('+-----------------------------------------------------------+')       

    def getInput(self, update_data, motor):
        '''
        @brief              Reads user inputs and writes encoder/motor commands
        @param update_data  Refers to numbered encoder object passed in by main
        @param motor        Refers to numbered motor object passed in by main 

        '''
        if (utime.ticks_diff(utime.ticks_us(), self.next_time) > 0):
            self.next_time = utime.ticks_add(self.next_time, self.user_freq)
            self.state = 0
            if self.coms.any() and motor == motor1:                
                # Read one character of user key press
                self.input = self.coms.read(1)                
                
                # Encoder/Motor 1 key presses and associated commands
                if self.input.decode() == 'z':
                    print('Setting Position to 0')
                    self.state = 1
                if self.input.decode() == 'p':
                    print('Getting Position: ', update_data.current[0])
                    print('')
                if self.input.decode() == 'd':
                    print('Getting Delta: ', update_data.current[1])
                    print('')
                if self.input.decode() == 'g':
                    print('Collecting data for 30 seconds')
                    self.gather = True
                if self.input.decode() == 's':
                    print('Ending data collection')
                    self.gather = False
                if self.input.decode() == 'm':
                    print('Please enter a duty cycle between -100 to 100')
                    input_duty = int(input('Duty Cycle: '))
                    motor.set_duty(input_duty)
                if self.input.decode() == 'c':
                    print('Clearing motor fault')
                    self.motor.clear_fault                
                
            if self.coms.any() and motor == motor2:                   
                # Read one character of user key press
                self.input = self.coms.read(1)                
                
                # Encoder/Motor 2 key presses and associated commands
                if self.input.decode() == 'Z':
                    print('Setting Position to 0')
                    self.state = 1
                if self.input.decode() == 'P':
                    print('Getting Position: ', update_data.current[0])
                    print('')
                if self.input.decode() == 'D':
                    print('Getting Delta: ', update_data.current[1])
                    print('')
                if self.input.decode() == 'M':
                    print('Please enter a duty cycle between -100 to 100')
                    input_duty = int(input('Duty Cycle: '))
                    motor.set_duty(input_duty)
                if self.input.decode() == 'G':
                    print('Collecting data for 30 seconds')
                    self.gather = True
                if self.input.decode() == 'S':
                    print('Ending data collection')
                    self.gather = False
                if self.input.decode() == 'C':
                    print('Clearing motor fault')
                    self.motor.clear_fault 
            
            # Evaluating for gather = True allows for the "s" exception, which 
            # will end data collection prematurely
            if self.gather and (self.run < 30.0/(self.user_freq/1E6)):
                self.data += [[update_data.current[0], (update_data.current[2])/1E6]]
                self.run += 1

            else:
                # Print the zeroeth and first index of each list in the data
                #   list, one line at a time
                for i in range(len(self.data)):
                    print(self.data[i][0],',', self.data[i][1])
                self.data = []
