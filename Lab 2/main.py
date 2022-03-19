"""!
@file main.py
@brief Runs all the tasks.  
@details This file runs all the tasks and classes necessary to run the user interface.  
         Task Diagram is depicted below:
         @image html taskDiagram2.png width=500px
         
         Find State Transition Diagram for the User Task in @ref lab2_UTask.py .  
         Find State Transition Diagram for the Encoder Task in @ref lab2_ETask.py .  
         
         See source code:
         https://bitbucket.org/bbartl01/mechatronics-labs/src/master/Lab2/main.py
         
@author Baxter Bartlett
@author Nick DeSimone
@author Miles Ibarra
@date 02-03-22
"""
import lab2_ETask
import lab2_UTask
import shares

## @brief Character flag to change variable value.
#  @details This variable is used in conjunction with the shares class to enable 
#           the two tasks to communicate when to change states.  
#
zFlag = shares.Share(False)

## @brief Creates a tuple
#  @details Creates a tuple containing time, position, and delta, all obtained
#           from the Encoder Task
#
encData = shares.Share((0,0,0))


if __name__ == '__main__':
    
    ## @brief Creates a list of tasks to be computed simultaneously.
    #  @details Contains the two tasks that are used to run the User Interface.
    #           The two tasks run simultaneously.       
    #
    taskList = [lab2_UTask.taskUserFCN ('Task User', 10_000, zFlag, encData),
                lab2_ETask.updateFunction ('Task Encoder', 10_000, zFlag, encData)]
    
    while True:
        try:
            for task in taskList:
                next (task)
        
        except KeyboardInterrupt:
            break
    print('Program Terminating')