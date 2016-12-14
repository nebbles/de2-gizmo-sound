# Test file descriptions

## Contents

+ [motortest.py](#motortestpy)

### motortest.py

Allows user to set the duty cycle of the motor PWM signal. This can test the motor operates at different speeds.

### mstest0.py

Returns the state of the microswitch and will also return an RPM (virtual) for the rate of trigger events.

### mstest1.py

Combines the use of the motor and microswitch. Once a duty cycle is inputted the motor will run and the RPM will be calculated and returned on every trigger event.

### pinsetup.py

This is a dummy program which does nothing on running but allows for a standardised header to every written program.

### rpmtest1.py

Runs the motor automonously using the trigger events to calculate the RPM and assign a new PWM to reach a target of 75 RPM.

### solenoidtest3.py

Contains two modes: file, debug

+ File - runs 'solenoidtest3.txt' file which plays through different combinations of solenoids hit at a speed defined by the user.
+ Debug - waits for user to input a customised combination of the solenoid hitters and will play that combination once.

### synctest1.py

*This is proof of concept for the threading design.*  
Runs with no hardware, this script simulates and environment with a brush stroke happening in intermittent periods. The solenoid thread then attempts to keep in time with the brush, out of phase by one beat.

### synctest2.py

Running experiments on timing with threads.
