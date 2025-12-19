# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       hfx                                                          #
# 	Created:      12/18/2025                                                   #
# 	Description:  V5 project with concurrent motor control                     #
#                                                                              #
# ---------------------------------------------------------------------------- #

from vex import *
from threading import Thread

# Initialize brain and controller
brain = Brain()
controller_1 = Controller(PRIMARY)

# Global state variables
battery_percent = 0
battery_voltage = 0
left_button_pressed = False
right_button_pressed = False

# ============================================================================ #
#                          MONITORING FUNCTIONS                               #
# ============================================================================ #

def monitor_battery():
    """Continuously update and display battery information."""
    global battery_percent, battery_voltage
    
    while True:
        battery_percent = brain.battery.capacity()
        battery_voltage = brain.battery.voltage(VoltageUnits.VOLT)
        
        # Format battery display string
        battery_display = f"{battery_percent}% | {battery_voltage}V"
        
        # Display on brain screen
        brain.screen.clear_row(1)
        brain.screen.set_cursor(1, 1)
        brain.screen.print(battery_display)
        
        # Display on controller screen
        controller_1.screen.clear_row(1)
        controller_1.screen.set_cursor(1, 1)
        controller_1.screen.print(battery_display)
        
        # Console output
        print(battery_display)
        
        wait(1, SECONDS)

# ============================================================================ #
#                        BUTTON CALLBACK FUNCTIONS                            #
# ============================================================================ #

def on_right_button_pressed():
    """Handle R1 button press - spin motor forward."""
    global right_button_pressed
    
    while controller_1.buttonR1.pressing():
        right_button_pressed = True
        wait(5, MSEC)
    
    right_button_pressed = False

def on_left_button_pressed():
    """Handle L1 button press - spin motor forward."""
    global left_button_pressed
    
    while controller_1.buttonL1.pressing():
        left_button_pressed = True
        wait(5, MSEC)
    
    left_button_pressed = False

# ============================================================================ #
#                        MOTOR CONTROL FUNCTIONS                              #
# ============================================================================ #

def control_motor():
    """Continuously control motor based on button states."""
    global left_button_pressed, right_button_pressed
    
    while True:
        # If either button is pressed, spin the motor
        if left_button_pressed or right_button_pressed:
            MOTORORTA.spin(FORWARD, 10, VOLT)
        else:
            MOTORORTA.stop()
        
        wait(5, MSEC)

# ============================================================================ #
#                        AUTONOMOUS & DRIVER CONTROL                          #
# ============================================================================ #

def autonomous():
    """Autonomous mode code."""
    brain.screen.clear_screen()
    brain.screen.print("Autonomous Mode")
    # Place autonomous code here

def user_control():
    """Driver control mode - runs the main control loop."""
    brain.screen.clear_screen()
    brain.screen.print("Driver Control Active")
    
    while True:
        wait(20, MSEC)

# ============================================================================ #
#                            MAIN PROGRAM START                               #
# ============================================================================ #

if __name__ == "__main__":
    # Clear initial screen
    brain.screen.clear_screen()
    brain.screen.print("Initializing...")
    
    # Register button event handlers
    controller_1.buttonR1.pressed(on_right_button_pressed)
    controller_1.buttonL1.pressed(on_left_button_pressed)
    
    # Wait to ensure events register
    wait(15, MSEC)
    
    # Start background threads
    battery_thread = Thread(monitor_battery)
    motor_thread = Thread(control_motor)
    
    battery_thread.start()
    motor_thread.start()
    
    # Create and start competition instance
    comp = Competition(user_control, autonomous)