""" 
@file    simonSays.py
@brief   Displays Morse patterns on Nucleo LED and asks user to repeat them
@details Implements a FSM, shown below, to create an interactive game for a
         user. The game entails blinking of a Nucleo LED in morse code patterns,
         whereupon the user is asked to repeat said pattern using the Nucleo's
         blue button.

         @image html simon_fsm.png
                  
         See source code here: 
             https://bitbucket.org/ndesimon/me405_labs/src/master/Lab%203/
             
         See short demonstration video here:
             https://drive.google.com/file/d/1Z7y6_3cOUfyDuwKpqxwhg9-7uB3f_5j9/view?usp=sharing

@author         Nick De Simone
@date           4/9/21
@copyright      License Info Here
"""
#import random
import utime
from morseCode import createPhrase
from morseCode import convertPhraseToMorse
import pyb

# Welcome Statement
print('Welcome to the "Simon Says" Nucleo Board Game \n')
print('Press "r" and hit enter to hear game rules \n')

## Waits for user to declare readiness for game start
ready = input()
# Display rules if user is ready
while ready != '' and ready != 'r':
    print('Input was invalid\n')
    print('Press "r" and hit enter to hear game rules \n')
    ready = input()

if ready == 'r':
    
    print('\n Rules: \n')
    print('1. Watch the LED on the Nucleo Controller; It will blink in Morse code \n')
    print('2. Repeat the Morse pattern using the Blue User Button \n')
    print('3. There will be three rounds of increasing complexity \n')
    print('4. Successfully complete all three rounds to beat the game! \n')
    print('Press Ctrl+C at any time to exit the game \n')
    print('Lets Go! \n')


# Initialize LED for PWM
## Assign Pin C13 to board
pinC13 = pyb.Pin (pyb.Pin.cpu.C13) #read HI on push; LO on release
## Assign Pin A5 to board
pinA5 = pyb.Pin (pyb.Pin.cpu.A5)
## Timer for PWM
tim2 = pyb.Timer(2, freq = 20000)
## Pulse Width Modulation
t2ch1 = tim2.channel(1, pyb.Timer.PWM, pin=pinA5)

## Establish game play level
level = 0



class simonSays:
    
    # Static variables are defined outside of methods
    
    ## Init state sets state to starts game and displays rules if user is ready
    S0_INIT          = 0
    ## State 1 generates random phrase and converts it to Morse/PWM Time 
    S1_CREATE_PHRASE = 1
    ## State 2 blinks the Morse sequence on the Nucleo LED     
    S2_SHOW_SEQ      = 2
    ## State 3 evaluates a user's attempt at copying the given Morse sequence     
    S3_USER_TRIAL    = 3
    ## State 4 declares the user successful and updates the game play level     
    S4_SUCCESS       = 4
    ## State 5 waits for the user to push button to continue     
    S5_STANDBY       = 5
    ## State 6 occurs if user fails in copying the LED sequence
    S6_FAIL          = 6
    
    def __init__(self, morse_unit = 1000, error_allow = 1000, 
                 DBG_flag=False):
        '''
        @brief              Initializes parameters/variables of the game
        @param error_allow  Time in [ms] of allowed error between user's input 
                            and the actual morse sequence
        @param morse_unit   Amount of time in [ms] for one base unit used to 
                            create morse characters

        @return none        

        '''
        # This not your state 0
        
        ## The current state of the finite state machine
        self.state = 0
        
        ## Level of Game Play
        self.level = level
        
        ## Flag to indicate button has been pushed or released
        self.buttonPushed = 0
        
        ## Flag to specify if debug messages print
        self.DBG_flag = DBG_flag
        
        ## Standard unit to be used for timing of morse characters
        self.morse_unit = morse_unit
        
        ## The allowed time difference between the actual morse sequence and 
        #  the user's button presses in microseconds
        self.error_allow = error_allow
        
        ## Assign external Button Interrupt
        self.ButtonInt = pyb.ExtInt(pinC13, mode=pyb.ExtInt.IRQ_RISING_FALLING,
                       pull=pyb.Pin.PULL_NONE, callback=self.onButtonPressFCN)


    def run(self):
        '''
        @brief Runs game FSM
        
        '''
        
        # MAIN PROGRAM CODE
        ## State 0: Initializing
        if self.state==self.S0_INIT:
            # run state 0 (init) code
            ## Serves as variable to establish next state in FSM
            self.newState = self.S1_CREATE_PHRASE   # Updating state for next iteration
            # Start game on level one
            print('GENERATING GAME... \n')
            self.level = 1
            self.standby()
        
        ## State 1: Creating Random Character/Phrase    
        elif self.state==self.S1_CREATE_PHRASE:
            
            # Run state 1 (morse code phrase creation)
            self.buttonPushed = False
            
            # Create list of randomly selected characters
            ## Randomly generated character or list of characters
            self.randPhrase = createPhrase(self.level)
            if self.DBG_flag:
                print(self.randPhrase)
            
            # Create empty list to be filled with the morse equivalents of the 
            #   random phrase
            ## List filled with morse equivalents of the randPhrase
            self.morsePhrase = []
            for n in self.randPhrase:
                self.morsePhrase.append(convertPhraseToMorse(n))
                if self.DBG_flag:
                    print(self.morsePhrase)
            
            # Convert Morse Phrase into time equivalents
            self.convertMorseToTime()
            if self.DBG_flag:
                print(self.timePhrase)
            
            # Transition to S2 (SHOW SEQUENCE)
            print ('Your current task is {} with a corresponding Morse sequence of {}. \n'.format(self.randPhrase, self.morsePhrase))
            print ('Get ready to watch the LED Morse Sequence \n')
            self.getReady()
            self.newState=self.S2_SHOW_SEQ
            self.transitionTo(self.newState)


        ## State 2: Show LED Morse Sequence    
        elif self.state==self.S2_SHOW_SEQ:
            
            # run state 2 (show sequence) code
            self.buttonPushed = False
            print('Now Showing the LED Morse Sequence \n')
            self.lights() # Run PWM function with the timePhrase
            self.getReady()
            self.newState=self.S3_USER_TRIAL
            self.transitionTo(self.newState)
        
        ## State 3: User Matches LED Morse Sequence
        elif self.state==self.S3_USER_TRIAL:
            
            # run state 3 (user trial) code
            print('Now it is your turn... \n')
            print('Push the blue button in the same sequence as was just shown \n')
            self.getReady()
            self.checkUser()
            # checkUser should return a new state once the user's list matches
            #   the length of the timePhrase. It will then be either success
            #       or failure
            self.standby()
        
        ## State 4: User Successfully Matches Sequence
        elif self.state==self.S4_SUCCESS:
            # run state 4 (single round success) code
            # Declare winner
            # Ask if would like to proceed to next round (if not, exit)
            # Update level and send to S1
            self.level += 1
            if self.level <= 3:
                print ('Congratulations! You successfully matched the sequence. \nGet ready for the next round \n')
                self.getReady()
                self.newState=self.S1_CREATE_PHRASE
            elif self.level > 3:
                # State 7: Print statement serves as State 7: Total Win
                print ('Congratulations! You successfully completed all three rounds. \nYou may repeat the game or exit. \n')
                self.newState=self.S0_INIT
            self.transitionTo(self.newState)

        ## State 5: Standby          
        elif self.state==self.S5_STANDBY:
            if self.buttonPushed:
                self.buttonPushed = False
                self.transitionTo(self.newState)

        ## State 6: User Fails to Match Sequence                
        elif self.state==self.S6_FAIL:
            print('You lost :( \n')
            print('Get ready to try again or press Ctrl+C to exit \n')
            self.level = 1
            self.newState = self.S1_CREATE_PHRASE
            self.getReady()
            self.transitionTo(self.newState)
               
                

        else:
            pass
            # code to run if state number is invalid
            # program should ideally never reach here
    
    def transitionTo(self, newState):
        '''
        @brief Transitions to the next specified state in the FSM

        '''
        if self.DBG_flag:
            print(str(self.state) + "->" + str(newState) + '\n')    
        self.state = self.newState
        self.buttonPushed=False # reset flag

    
    def standby(self):
        '''
        @brief Sends user to a standby state where they must button push to continue

        '''
        print('Press Blue Button to Continue \n')
        self.buttonPushed = 0
        self.state = self.S5_STANDBY
            
    
    def convertMorseToTime(self):
        '''
        @brief Converts Morse Code to Times for PWM

        '''
        ## List containing Morse sequences converted into units of time
        self.timePhrase = []
        for i in range(self.level):
            for n in self.morsePhrase[i]:
                # Assign timing of a standard dot
                if n == '.': 
                    self.timePhrase.append(self.morse_unit)
                    # add a unit space after each character
                    self.timePhrase.append(self.morse_unit)
                # Assign timing of a standard dash
                elif n == '-':    
                    self.timePhrase.append(self.morse_unit*3)
                    # add a unit space after each character
                    self.timePhrase.append(self.morse_unit)

    def getReady(self):
        '''
        @brief Gives three ready statements as a buffer before proceeding in the game

        '''
        start_time = utime.ticks_ms()
        cdn = 3 # countdown number
        while cdn >= 0:
            round_time = utime.ticks_ms()
            if ((utime.ticks_diff(round_time,start_time)) > 1000):
                if cdn == 3:
                    print('Get ready \n')
                elif cdn == 2:
                    print('Get set \n')
                elif cdn == 1:
                    print('Go \n')
                elif cdn == 0:
                    print(' \n')
                start_time = utime.ticks_ms()
                cdn -= 1
                
    def lights(self):
        '''
        @brief Displays morse sequence on the LED of Pin C13
        '''
        i=0
        init_time = utime.ticks_ms()
        while i<(len(self.timePhrase)):
            curr_time = utime.ticks_ms()
            if (utime.ticks_diff(curr_time,init_time)) < self.timePhrase[i]:
                if (i % 2): # if its an odd index
                    t2ch1.pulse_width_percent(0) # turn led off
                else: #if even index
                    t2ch1.pulse_width_percent(100) # turn led on

                if self.DBG_flag:
                    print(i)
                    print(self.timePhrase[i])
                    print(utime.ticks_diff(curr_time,init_time))
            elif (utime.ticks_diff(curr_time,init_time)) >= self.timePhrase[i]:
                i += 1 # add 1 to index to update PWM to next item in time list
                init_time = utime.ticks_ms() # reset init time so it is able to go 0->timePhrase
                if i == 12:
                    print('Light show done. Get ready to copy the sequence \n')
                    
    def checkUser(self):
        '''
        @brief Checks user's button pushes and compares them to the given seq

        '''               
        init_time = utime.ticks_ms()
        trial = [] # time list to be compared to total length of Morse sequence
        while len(trial) <= len(self.timePhrase):
            curr_time = utime.ticks_ms()
            time_diff = utime.ticks_diff(curr_time,init_time)

            if self.buttonPushed:
                trial.append(time_diff)
                if self.DBG_flag:
                    print(trial)
                    print("len trial: ",  len(trial))
                    print("len timPhr: ", len(self.timePhrase))
                if (len(trial)%2): #if odd length value, turn LED on
                    t2ch1.pulse_width_percent(100)
                else: # if even length value, turn LED off
                    t2ch1.pulse_width_percent(0)
                for x in range(1, len(trial)):
                    theor = self.timePhrase[x-1]
                    actual = trial[x] - trial[x-1]
                    if self.DBG_flag:
                        print("theor: ", theor)
                        print("actual: ", actual)
                        print("theor - actual: ", abs(theor-actual))
                    if abs(theor - actual) > self.error_allow:
                        self.newState = self.S6_FAIL
                        return
                    else:
                        pass
                self.buttonPushed = 0
                if len(trial) == len(self.timePhrase):
                    self.newState = self.S4_SUCCESS
                    return
                
        
         

    # Define a callback function that will run when the button is pressed
    def onButtonPressFCN(self, IRQ_src):
        '''@brief Commands Nucleo upon button push
           @param IRQ_src Associated with button interrupt 
        '''
        ## Flag Variable
        self.buttonPushed = True



