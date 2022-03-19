'''! @page lab1page.py Lab 1: LED Light Show
    @tableofcontents
    Blink the Nucleo L476 LED in three patterns.
    
    @section sec_intro2 Introduction
    Lab 1 served as an introduction to writing Python scripts to be run on a 
    microcontroller. Our team wrote a finite state machine program that is
    able to be run on a Nucleo L476 MCU. The goal of the program is to display
    three LED pulse patterns on the Nucleo's native LED, located on pin PA5. 
    By clicking the Nucleo's blue user button, the user is able to cycle 
    through the following three LED patterns: (1) square wave
    (2) sine wave and (3) sawtooth wave.
    Please see @ref sec_files1 for descriptions about our project file.
    
    @section sec_vid1 Demonstration Video
    See short demonstration video of the LED patterns here: \n 
    https://drive.google.com/file/d/1gsICIg6rI42QG8VJxdCG4akqodxdDdyq/view
    \n   
    
    @section sec_files1 Project Files
    
    @subsection sub_led1 LED Patterns
    Our Lab 1 script, LED_Patterns.py, changes the LD2 LED light of the 
    Nucleo L476 according to the following three waveforms:
    (1) square (2) sine and (3) sawtooth. The user is able to press the
    blue user button on the Nucleo in order to cycle through those three
    LED patterns.
    See @ref LED_Patterns.py for more information.

'''