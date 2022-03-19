'''! @page lab3page.py Lab 3: DC Motor Control
    @tableofcontents
    DC motor driving using PWM.
    
    @section sec_intro3 Introduction
    Lab 3 achieves independent control of two DC motors by applying PWM 
    signals to their associated timer channels. The motors are enabled via the
    DRV8847 motor driver from Texas Instruments, which is also able to disable
    the motors by triggering fault conditions. Thus, Lab 3 implements task and
    driver files that are able to handle the motor and each of the two DC 
    motors independently. A user interface task is also included to interpret 
    user keyboard presses as motor and/or motor driver commands, such as 
    setting the motor duty cycles (in pulse width percent), enabling and 
    disabling the motor driver, and clearing motor fault conditions.
    Please see @ref sec_files3 for descriptions of our project files.
    
    @section sec_res3 Results
    The Lab 3 firmware offers two opportunities for data collection; the user
    may choose (1) to record encoder position over time or (2) to compute the
    average velocity, in [rad/s], of Motor 1 according to input duty cycles in 
    [% PWM]. See <b>Figures 1-2</b> for observation of experimental results
    for each of these cases.
    
    <CENTER>
    @image html Lab3Data1.png width=500px
    <b>Figure 1:</b> Encoder position, converted to [rad] from encoder ticks, 
    over time in [sec].
    
    @image html Lab3Data2.png width=500px    
    <b>Figure 2:</b> Average motor speeds, in [rad/s], for input duty cycles
    ranging from -100 to 100 [% PWM], in 10 [% PWM] increments. Note the slight
    non-linear relationship between the actual motor speed and duty cycle
    (especially between -20 to 20 [% PWM]), as 
    compared to the theoretically linear trend between the two. This error is
    indicative of physical nonlinearities in the motors, like voltage losses
    or motor stiction.
    </CENTER>
    
    @section sec_files3 Project Files
    
    @subsection sub_main3 Main File
    The main file instantiates our task- and class-files as objects to be run
    asynchronously. Note the task diagram below for information regarding file 
    communication and run frequency. See @ref main.py for more information.
    @image html taskDiagram3.png width=600px

    @subsection sub_utask3 User Task
    The user interface is written as a generator function that prints to a 
    terminal emulator. It is able to read a user's keyboard presses as encoder
    and motor commands, such as collecting the encoder's position over time or 
    accepting user-input motor PWM duty cycles, over the USB virtual comm port. 
    See @ref UTask.py for more information and the figure below for the User
    Task's state transition diagram.
    @image html UTaskSTD3.png width=600px

    @subsection sub_mtask3 Motor Task
    The motor task sends user-determined duty cycles to their respective 
    motors, either Motor 1 or Motor 2. 
    See @ref MTask.py for more information and the figure below 
    for the Motor Task's state transition diagram.
    @image html MTaskSTD3.png width=500px

    @subsection sub_stask3 Safety Task
    The safety task enables and disables the motors according to the user's
    keyboard presses, or at the occurence of faults, which are 
    triggered by the motor driver, the DRV8847.
    See @ref STask.py for more information and the figure below 
    for the Safety Task's state transition diagram.
    @image html STaskSTD3.png width=500px
    
    @subsection sub_etask3 Encoder Task
    The encoder task uses a generator function to update a shared tuple, 
    encData, that stores time [ms], position [ticks], and position changes
    [ticks/sec]. See @ref ETask.py for more information and the figure below 
    for the Encoder Task's state transition diagram.
    @image html ETaskSTD3.png width=500px

    @subsection sub_mot3 Motor Driver
    The motor driver is a class file that instantiates timer and timer 
    channel objects for the designated motor's PWM channels, which are 
    configured as inverted PWM channels. The driver also has a method to set
    motor duty cycles as a pulse width percent, whose value is determined by
    the user's entered duty cycle.
    See @ref motor.py for more information.
    
    @subsection sub_drv3 DRY8847 Driver
    The DRV8847 class file handles control of our physical motor driver, the
    DRV8847. Its associated methods include enabling and disabling the driver's
    enable pin, clearing motor faults triggered by the driver's fault pin,
    or specifying motor pin, timer, and timer channel values, all of which 
    are called either in @ref main.py or in the safety task, @ref STask.py.
    See @ref DRV8847.py for more information.
    
    @subsection sub_enc3 Encoder Driver
    The encoder driver is a class file that instantiates timer and timer 
    channel objects and has various methods for reading data from the encoder.
    See @ref encoder.py for more information.
    
    @subsection sub_sha3 Shares Class
    The shares class file allows variables to be created, read from, and 
    written to multiple files.
    See @ref shares.py for more information.
    
'''