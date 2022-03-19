"""!
@file    LED_Patterns.py
@brief   Script to change LED light pattern for lab01
@details Using pyb and utime, the script changes a specific LED light
         on a nucelo board in 3 different patterns: square qave, sine
         wave, and saw wave.

        @image html led_fsm.png width=600px
        
        See source code here:
        https://bitbucket.org/ndesimon/me405_labs/src/master/Lab%200x01/LED_Patterns.py
            
        See short demonstration video here:
        https://drive.google.com/file/d/1gsICIg6rI42QG8VJxdCG4akqodxdDdyq/view

@author Tyler McCue, Nick De Simone
@date   10/8/2021
"""
import time
import pyb
import utime
import math
#run continuously until user exits

def current_time(time):
    """!
    @brief Returns updated time difference between button push and current time
    @details Uses the utime module to return a running clock that then updates
             the LED patterns
    """   
    return (utime.ticks_diff(utime.ticks_ms(), time))/1000

def square_wave(current_time):
    """!
    @brief runs LED with square wave pattern
    @details Using the pyb module, an LED flashes in a square wave pattern
    @param current_time Accumulated time difference between button push and current time
    """
    return 100*((current_time % 1) < 0.5)

def sine_wave(current_time):
    """!
    @brief runs LED with square wave pattern
    @details Using the pyb module, an LED flashes in a square wave pattern
    """
    return 100*(.5*math.sin(2*math.pi*(current_time % 10)/10) + .5)

def saw_wave(current_time):
    """!
    @brief runs LED with square wave pattern
    @details Using the pyb module, an LED flashes in a square wave pattern
    """
    return 100*(current_time % 1)

def button_pressed(IRQ_src):
    '''!
    @brief Sets button flag variable to true upon user button press
    @param IRQ_src Interrupt request triggered by button push
    '''
    global blue_button_pressed
    blue_button_pressed = 1
    print('Button Pressed!')

if __name__ == '__main__':
    ## Assign Green LED on Nucleo to Pin A5 for PWM usage
    pinA5 = pyb.Pin(pyb.Pin.cpu.A5)
    ## Establish Timer for PWM
    tim2 = pyb.Timer(2, freq = 20000)
    ## Link PWM to Pin A5
    t2ch1 = tim2.channel(1, pyb.Timer.PWM, pin=pinA5)
    
    ## Assign Blue Button on Nucleo to Pin C13 for Button Interrupt
    pinC13 = pyb.Pin (pyb.Pin.cpu.C13)

    ## External interrupt associated with the blue button's callback function
    ButtonInt = pyb.ExtInt(pinC13, mode=pyb.ExtInt.IRQ_FALLING,
                           pull=pyb.Pin.PULL_NONE, callback=button_pressed)

    ## The current state for this iteration of the FSM
    state = 0
    ## The current run loop of the program
    runs = 0
    ## The current state of the button
    blue_button_pressed = 0
    ## If the current state has already run once
    ran = False

    while True:
        try:
            if state==0:
                #run state 0  code
                # "not ran" allows FSM to only pass through state 0 one time
                if not ran:
                    print("Welcome to the LED cycle program")
                    print("Press the blue button to begin")
                    print("Press Ctrl+C to Exit")
                    ran = True
                    state = 1
                    
            elif state==1:
                #run state 1 code
                # Looks for user button press to transition to next state
                if blue_button_pressed == 1:
                    print("Now Showing: Square Wave Pattern")
                    print("Press Blue Button for Next Pattern")
                    state = 2
                    blue_button_pressed = 0
                    start_time = utime.ticks_ms()
                    
            elif state==2:                
                #run state 2 code
                # Update accumulated time for each pass through FSM
                timer = current_time(start_time)
                # Update LED "brightness" according to pattern's equation and current timer
                t2ch1.pulse_width_percent(square_wave(timer))
                # Looks for user button press to transition to next state
                if blue_button_pressed == 1:
                    print("Now Showing: Sine Wave Pattern")
                    print("Press Blue Button for Next Pattern")
                    state = 3
                    blue_button_pressed = 0
                    start_time = utime.ticks_ms()
                    
            elif state==3:
                #run state 3 code
                timer = current_time(start_time)
                t2ch1.pulse_width_percent(sine_wave(timer))
                if blue_button_pressed == 1:
                    print("Now Showing: Saw Wave Pattern")
                    print("Press Blue Button for Next Pattern")
                    state = 4
                    blue_button_pressed = 0
                    start_time = utime.ticks_ms()
                    
            elif state==4:
                #run state 4 code
                timer = current_time(start_time)
                t2ch1.pulse_width_percent(saw_wave(timer))
                if blue_button_pressed == 1:
                    print("Now Showing: Square Wave Pattern")
                    print("Press Blue Button for Next Pattern")
                    state = 2
                    blue_button_pressed = 0
                    start_time = utime.ticks_ms()
            
            # Counts number of passes through entire FSM        
            runs += 1
        
        except KeyboardInterrupt:
            print("Program Ended!!")
            t2ch1.pulse_width_percent(0)
            break
