global last_time

def servo_left():
    servos.P0.set_angle(150)
    basic.show_leds("""
        # . . . .
        # . . . .
        # . . . .
        # . . . .
        # # # # .
        """)
    if control.millis() - last_time <= 1000:
            last_time = control.millis()
    servos.P0.set_angle(90)
def motor_forward():
    pins.digital_write_pin(DigitalPin.P20, 1)# ENA HIGH
    pins.digital_write_pin(DigitalPin.P3, 1)# IN1 HIGH
    pins.digital_write_pin(DigitalPin.P1, 0)# IN2 LOW
    basic.show_leds("""
        # # # # .
        # . . . .
        # # # . .
        # . . . .
        # . . . .
        """)
def motor_backward():
    pins.digital_write_pin(DigitalPin.P20, 1)
    pins.digital_write_pin(DigitalPin.P3, 0)# IN1 LOW
    pins.digital_write_pin(DigitalPin.P1, 1)# IN2 HIGH
    basic.show_leds("""
        # # # # .
        # . . . #
        # # # # .
        # . . . #
        # # # # .
        """)

def motor_stop():
    pins.digital_write_pin(DigitalPin.P20, 0)
    pins.digital_write_pin(DigitalPin.P3, 0)
    pins.digital_write_pin(DigitalPin.P1, 0)
    basic.show_leds("""
        . # # # #
        # . . . .
        . # # # .
        . . . . #
        # # # # .
        """)
def servo_right():
    servos.P0.set_angle(30)
    basic.show_leds("""
        # # # . .
        # . . # .
        # # # . .
        # . . # .
        # . . # .
        """)
    if control.millis() - last_time <= 1000:
            last_time = control.millis()
    servos.P0.set_angle(90)
message = ""
# Sett opp radio
radio.set_group(67)
servos.P0.set_angle(90)

"""
direction_map = {
    "L": servo_left,
    "R": servo_right,
    "F": motor_forward,
    "B": motor_backward
}
"""
#was going to add "lookup table" functionality instead of if else test in the main loop but couldnt get it to work so focused rather on the self balancing

def on_forever():
    global message

    message = radio.receive_string()
    if message == "R":
        servo_right()
    
    elif message == "L":
        servo_left()

    elif message == "F":
        motor_forward()        

    elif message == "B":
        motor_backward()

    else:
        motor_stop()
basic.forever(on_forever)
