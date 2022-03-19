'''@file fibonacci.py
   @brief  This file calculates a Fibonacci number at a specific index.
   @details Uses a function to compute the Fibonacci number at an index 
            specified by the user
            
            See source code here: 
                https://bitbucket.org/ndesimon/me405_labs/src/master/Lab%201/
   @author Nick De Simone
   @author Charlie Refvem (Bottom-Up Fib Function)
   @date   1/14/2021
'''


def fib (idx):
    '''@brief Computes Fibonacci number at a specific index.
       @param  idx  An integer specifying the index of the desired 
                    Fibonacci number    
       @return The associated F number at the specified index
    '''
    if idx == 0:
        return 0
    elif idx == 1:
        return 1
    else :
        if idx > 1:
            fn_minus_two = 0
            fn_minus_one = 1
            
            for n in range (2,idx+1):
                fn = fn_minus_two + fn_minus_one
                
                fn_minus_two = fn_minus_one
                fn_minus_one = fn
        return (fn)

if __name__ == '__main__':
    print('Welcome to the Fibonacci Number Generator')
    
    while True:
        try:
            
            # Ask user for the index of their desired Fibonacci number 
            idx = input("Please enter the index of your desired Fibonacci"
                        " number: ")
            
            # Check whether user input is a positive whole number
            if idx.isdigit():
                idx = int(idx)
           
            # If the user input is not a digit integer, prompt user 
            # for another input
            else : 
                idx = input("Please enter an integer. An integer is any"
                            " whole number 1,2,3,etc: ")
                idx = int(idx)
                
            # Return the user their desired Fibonacci number
            print ('Fibonacci number at ' 
                   'index {:} is {:}.'.format(idx,fib(idx)))
        except KeyboardInterrupt:
            print ('Thank you for using the Fibonacci Number Generator!')
            break
