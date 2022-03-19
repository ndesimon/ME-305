'''@file HW_2.py
@brief   Simulates an elevator between two floors
@details Implements finite state machine, shown below, to simulate the 
         behavior of an elevator moving between two floors
         
         @image html elevator_fsm.png
            
         See source code here: 
             https://bitbucket.org/ndesimon/me405_labs/src/master/HW%202/
         
@author Nick De Simone
@date   1/25/2021
@copyright License Info Here
'''



import time
import random

# Function Definitions
def motor_cmd(cmd):
    '''@brief Commands the motor to move or stop
       @param cmd The command to give the motor
    '''
    if cmd=='0':
        print('Motor stop')
    elif cmd=='1':
        print('Motor up')
    elif cmd=='2':
        print('Motor down')
        
def button_1():
    '''@brief Randomly calls elevator to first floor
    '''
    return random.choice([True, False]) # randomly returns T or F
def button_2():
    '''@brief Randomly calls elevator to second floor
    '''
    return random.choice([True, False]) # randomly returns T or F
def first():
    '''@brief Randomly sets elevator at first floor
    '''
    return random.choice([True, False]) # randomly returns T or F
def second():
    '''@brief Randomly sets elevator at second floor
    '''
    return random.choice([True, False]) # randomly returns T or F




# Main program / test program begin
#  This code only runs if the script is executed as main by pressing play
#  but does not run if the script is imported as a module 

if __name__ == "__main__":
    # Program initialization goes here
    print ('Initiate')
    state = 0 # Initial state is the init state
    
    while True:
        try:
            # main program code goes here
            if state==0:
                # run state 0 (moving down) code
                print('S0: Car Moving Down')
                motor_cmd('2') # Command motor to move car down
                # if we are on first floor, stop the motor and transition to S2
                if first():
                    motor_cmd('0')
                    state = 1 # Updating state for next iteration
            
            elif state==1:
                # run state 1 (stopped at first floor) code
                print('S1: Car Stopped at Floor 1')
                # if button 2 is pressed, start motor and transition to S2
                if button_2():
                    motor_cmd('1')
                    state = 2
                elif button_1():
                    pass

            elif state==2:
                # run state 2 (moving up) code
                print('S2: Car Moving Up')
                motor_cmd('1')
                # if we are on second floor, stop motor and transition to S3
                if second():
                    motor_cmd('0')
                    state = 3
                    
             
            elif state==3:
                # run state 3 (stopped at second floor) code
                print('S3: Car Stopped at Floor 2')
                # if at the right, stop motor and transition to S4
                # if button 1 is pressed, transition to S0
                if button_1():
                    state = 0
                elif button_2():
                    pass
                    

            
            else:
                pass
                # code to run if state number is invalid
                # program should ideally never reach here
            
            # Slow down execution of FSM so we can see output in console
            time.sleep(0.2)
            
        except KeyboardInterrupt:
            # This except block catches "Ctrl+C" from the keyboard to end the
            #  while(True) loop when desired
            print('Ctrl-C has been pressed')
            break
        
    # Program de-initialization goes here
    print ('System Off')
    

