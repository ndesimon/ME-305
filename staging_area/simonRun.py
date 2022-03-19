''' @file           simonRun.py
    @brief          Runs the "simonSays.py" class
    @details        Runs the simonSays class to play an LED Nucleo game.
    @author         Nick De Simone
    @date           4/9/21
    @copyright      License Info Here
'''

# import time
from simonSays import simonSays



# Main program / test program begin
#   This code only runs if the script is executed as main by pressing play
#   but does not run if the script is imported as a a module
if __name__ == "__main__":
    # Program initialization goes here
    game1 = simonSays()
    
    while True:
        try:
            game1.run()
            
            # print('T2:')
            # task2.run()
            
            # Slow down execution of FSM so we can see output in console
            # time.sleep(0.2)
            
        except KeyboardInterrupt:
            # This except block catches "Ctrl-C" from the keyboard to end the
            # while(True) loop when desired
            print('Ctrl-c has been pressed')
            break

    # Program de-initialization goes  here
