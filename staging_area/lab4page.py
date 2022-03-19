'''! @page lab4page.py Lab 4: Closed-Loop Speed Control
    @tableofcontents
    Closed-loop speed control of DC motors.
    
    @section sec_intro4 Introduction
    Lab 4 introduces task and driver files to accomodate proportional
    and integral speed control of DC motors. The closed-loop controller 
    reads from the motors' quadrature encoders for error feedback, as well 
    as accepts user-input controller gains Kp and Ki to compute motor 
    actuation signals based on the error in motor velocity versus the user-
    input velocity setpoint. Please see @ref sec_files4 for descriptions of 
    our project files.
    
    Note the following block diagram for observation of our closed-loop
    controller:
    @image html block_diagram.png width=700px    
    
    @section sec_res4 Results
    The Lab 4 firmware is able to conduct user-defined velocity step response 
    tests on the DC motor, which allow for observation of the controller's
    performance in relation to the user defined controller gains and velocity
    setpoint. Please see <b>Figures 1-3</b> for three step response 
    tests, each conducted with a velocity setpoint of 100 [rad/s] and 
    variable Kp/Ki
    controller gains. Note subsequent evaluations of their controller 
    performance, including steady-state error and settling time.
    
    <CENTER>
    @image html Lab4Data1.png width=500px
    <b>Figure 1:</b> The first step-response test was conducted with a Kp of
    0.25 [%*s/rad] and Ki of 20 [Hz]. Note the acceptable steady-state error of
    -0.80 [rad/s] and lack of overshoot, but the relatively slow
    settling time of 0.404 [sec].
    
    @image html Lab4Data2.png width=500px    
    <b>Figure 2:</b> The second step-response test was conducted with a Kp of
    0.50 [%*s/rad] and Ki of 20 [Hz]. Note the steady-state error and settling
    time have both decreased, as compared to <b>Figure 1</b>, to -0.59 [rad/s]
    and 0.26 [sec], respectively. However, the increased Kp value produced
    undesirable overshoot of both the motor's angular velocity and actuation
    signal, which should be mitigated through further tuning of the controller 
    gains.        
    
    @image html Lab4Data3.png width=500px
    <b>Figure 3:</b> The third step-response test was conducted with a Kp of
    0.25 [%*s/rad] and Ki of 50 [Hz]. Note the settling time has decreased
    further to 0.129 [sec], although the steady-state error returns to around
    0.78 [rad/s]. However, oscillation is minimized, which we have chosen to
    optimize over settling time. 
    </CENTER>
    
    @section sec_files4 Project Files
    
    @subsection sub_main4 Main File
    The main file instantiates our task- and class-files as objects to be run
    asynchronously. Note the task diagram below for information regarding file 
    communication and run frequency. See @ref main.py for more information. 
    @image html taskDiagram4.png width=600px
    
    @subsection sub_utask4 User Task
    The user interface is written as a generator function that prints to a 
    terminal emulator. It is able to read a user's keyboard presses as encoder,
    motor driver,
    and controller commands, such as printing the encoder's position in ticks 
    or accepting user-input controller gain and velocity setpoint values, over 
    the USB virtual comm port. 
    See @ref UTask.py for more information and the figure below for the User
    Task's state transition diagram.
    @image html UTaskSTD4.png width=600px
    
    @subsection sub_ctask4 Controller Task
    The controller task communicates controller gain values, Kp and Ki, 
    and motor velocity setpoints to our closed-loop driver, 
    @ref closedloop.py. This task is also responsible for sending duty cycles 
    to the motor task, which enables motor actuation according to the 
    actuation signal computed in the closed-loop driver. 
    See @ref CTask.py for more information and the figure below for the 
    Controller Task's state transition diagram.
    @image html CTAskSTD4.png width=500px

    @subsection sub_mtask4 Motor Task
    The motor task sends duty cycles, which are determined as the actuation
    signal of the closed-loop controller, to their respective motors,
    either Motor 1 or Motor 2. 
    See @ref MTask.py for more information and the figure below 
    for the Motor Task's state transition diagram.
    @image html MTaskSTD3.png width=500px

    @subsection sub_stask4 Safety Task
    The safety task enables and disables the motors according to the user's
    keyboard presses, or at the occurence of faults 
    triggered by the motor driver chip, the DRV8847.
    See @ref STask.py for more information and the figure below 
    for the Safety Task's state transition diagram.
    @image html STaskSTD3.png width=500px
    
    @subsection sub_etask4 Encoder Task
    The encoder task uses a generator function to update a shared tuple, 
    encData, that stores time [ms], position [ticks], and position changes
    [ticks/sec]. See @ref ETask.py for more information and the figure below 
    for the Encoder Task's state transition diagram.
    @image html ETaskSTD3.png width=500px

    @subsection sub_clc4 Closed-Loop Control Driver
    The closed-loop driver is a class file that computes actuation signals 
    according to user-defined controller gains, Kp and Ki, and desired motor
    velocity setpoints. The controller is able to
    perform proportional and/or integral closed-loop control.
    See @ref closedloop.py for more information.

    @subsection sub_mot4 Motor Driver
    The motor driver is a class file that instantiates timer and timer 
    channel objects for the designated motor's PWM channels, which are 
    configured as inverted PWM channels. The driver also has a method to set
    motor duty cycles as a pulse width percent, whose value is determined by
    the user's entered duty cycle.
    See @ref motor.py for more information.
    
    @subsection sub_drv4 DRY8847 Driver
    The DRV8847 class file handles control of our physical motor driver, the
    DRV8847. Its associated methods include enabling and disabling the driver's
    enable pin, clearing motor faults triggered by the driver's fault pin,
    or specifying motor pin, timer, and timer channel values, all of which 
    are called either in @ref main.py or in the safety task, @ref STask.py.
    See @ref DRV8847.py for more information.
    
    @subsection sub_enc4 Encoder Driver
    The encoder driver is a class file that instantiates timer and timer 
    channel objects and has various methods for reading data from the encoder.
    See @ref encoder.py for more information.
    
    @subsection sub_sha4 Shares Class
    The shares class file allows variables to be created, read from, and 
    written to multiple files.
    See @ref shares.py for more information.

'''