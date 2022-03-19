'''@file LED_waves.py
@brief   Cycles through LED pulse patterns
@details Implements finite state machine, shown below, and Nucleo blue user 
         button to cycle through LED pulse patterns
         
         @image html led_fsm.png
            
         See source code here: 
             https://bitbucket.org/ndesimon/me405_labs/src/master/Lab%202/
             
         See short demonstration video here:
             https://drive.google.com/file/d/1gsICIg6rI42QG8VJxdCG4akqodxdDdyq/view?usp=sharing
            
             
@author Nick De Simone
@date   2/4/2021
@copyright License Info Here
'''

import utime
import pyb
import math

global state

# Function definitions go here

# Define a callback function that will run when the button is pressed
def onButtonPressFCN(IRQ_src):
    '''@brief Commands Nucleo upon button push
       @param IRQ_src Associated with button interrupt 
    '''
    ## Flag Variable
    global buttonPushed
    buttonPushed = True
    print('Show the lights!')

#Define flag variable
buttonPushed = False
    
def squareWave(time_diff):
    '''@brief Runs square wave LED pattern
       @param time_diff Difference between current time and latest button push
    '''
    # run square PWM on pin A5
    global duty
    duty = 100*(time_diff%1<=0.5) # time in seconds
    t2ch1.pulse_width_percent(duty)
def sineWave(time_diff):
    '''@brief Runs sine wave LED pattern
       @param time_diff Difference between current time and latest button push
    '''
    #run sine PWM on pin A5
    global duty
    duty = 50*math.sin(((math.pi)/10)*time_diff)+50
    t2ch1.pulse_width_percent(duty)
def sawWave(time_diff):
    '''@brief Runs saw wave LED pattern
       @param time_diff Difference between current time and latest button push
    '''
    #run saw PWM on pin A5
    global duty
    duty = 100*(time_diff%1) # time in seconds
    t2ch1.pulse_width_percent(duty)




# Main program / test program begin
#  This code only runs if the script is executed as main by pressing play
#  but does not run if the script is imported as a module 

if __name__ == "__main__":
    # Program initialization goes here
    print ('Welcome to the LED Light Show. Initiating...')
    print ('Push Blue Button to Start Show')
    print ('Press Ctrl+C to Exit')
    
    ## Assign Pin C13 to board
    pinC13 = pyb.Pin (pyb.Pin.cpu.C13)
    ## Assign Pin A5 to board
    pinA5 = pyb.Pin (pyb.Pin.cpu.A5)
    
    ## Timer for PWM
    tim2 = pyb.Timer(2, freq = 20000)
    ## Pulse Width Modulation
    t2ch1 = tim2.channel(1, pyb.Timer.PWM, pin=pinA5)
    
    # Associate the callback function with the pin by setting up an external 
    # interrupt.    
    ## External interrupt associated with button callback function
    ButtonInt = pyb.ExtInt(pinC13, mode=pyb.ExtInt.IRQ_FALLING,
                           pull=pyb.Pin.PULL_NONE, callback=onButtonPressFCN)
    
    ## The current state of the finite state machine
    state = 0 
    
    ## Stores time at which button is pushed for square wave
    time_one = 0
    
    ## Stores time at which button is pushed for sine wave
    time_two = 0
    
    ## Stores time at which button is pushed for saw wave
    time_three = 0
    
    ## Defines duty cycle for the desired waveform
    duty = 0
    
    ## Calculates difference between current time and latest button push
    time_diff = 0
    
    while True:
        try:
            # main program code goes here
            if state==0:
                # Run state 0 (init) code
                
                # Turn the LED off
                t2ch1.pulse_width_percent(0)
                
                # If user pushes button, run square wave
                if buttonPushed:
                    state = 1            # Updating state for next iteration
                    buttonPushed = False # Reset flag variable
                    time_one = utime.ticks_ms() # Record time of button push
                    print('Showing Square Wave Pattern')
                    print('Push button to see next pattern')
            
            elif state==1:
                # run state 1 (square wave) code
                
                # calculate time difference in seconds
                time_diff = (utime.ticks_diff(utime.ticks_ms(),time_one))/1000
                
                # call square wave function which applies each duty cycle
                #  iteration as a pulse width percent to the LED
                squareWave(time_diff)
                
                # if user pushes button again, run sine wave
                if buttonPushed:   
                    state = 2
                    buttonPushed = False
                    time_two = utime.ticks_ms()
                    print('Showing Sine Wave Pattern')
                    print('Push button to see next pattern')
                         
            elif state==2:
                # run state 2 (sine wave) code
                time_diff = (utime.ticks_diff(utime.ticks_ms(),time_two))/1000
                sineWave(time_diff)
                
                # if user pushes button again, run sine wave
                if buttonPushed:   
                    state = 3
                    buttonPushed = False
                    time_three = utime.ticks_ms() 
                    print('Showing Saw Wave Pattern')
                    print('Push button to restart pattern sequence')
             
            elif state==3:
                # run state 3 (saw wave) code
                time_diff=(utime.ticks_diff(utime.ticks_ms(),time_three))/1000
                sawWave(time_diff)

                # if user pushes button again, run sine wave
                if buttonPushed:   
                    state = 1
                    buttonPushed = False
                    time_one = utime.ticks_ms()
                    print('Showing Square Wave Pattern')
                    print('Push button to see next pattern')
            
            else:
                pass
                # code to run if state number is invalid
                # program should ideally never reach here
            
        except KeyboardInterrupt:
            # This except block catches "Ctrl+C" from the keyboard to end the
            #  while(True) loop when desired
            print('Ctrl-C has been pressed')
            t2ch1.pulse_width_percent(0) 
            break
        
    # Program de-initialization goes here
    print ('Light Show Terminated')
    
    

