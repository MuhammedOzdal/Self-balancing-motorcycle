radio.on()
radio.set_group(67)

mode = 0 
lastState = "STOP"  

basic.show_string("S")


pins.set_pull(DigitalPin.P13, PinPullMode.PULL_UP) 
pins.set_pull(DigitalPin.P14, PinPullMode.PULL_UP)
pins.set_pull(DigitalPin.P15, PinPullMode.PULL_UP)
pins.set_pull(DigitalPin.P16, PinPullMode.PULL_UP)

def vis_mode(symbol: str):
    basic.show_string(symbol)
    #basic.clear_screen()

def buttons():
    global lastState
    pressed = False

    if input.button_is_pressed(Button.A):
        radio.send_string("F")
        basic.show_leds("""
            . . # . .
            . # # # .
            # # # # #
            . . # . .
            . . # . .
        """)
        pressed = True
        lastState = "FORWARD"

    elif input.button_is_pressed(Button.B):
        radio.send_string("R")
        basic.show_leds("""
            . . # . .
            . . # # .
            # # # # #
            . . # # .
            . . # . .
        """)
        pressed = True
        lastState = "RIGHT"

    elif pins.digital_read_pin(DigitalPin.P13) == 0:
        radio.send_string("L")
        basic.show_leds("""
            . . # . .
            . # # . .
            # # # # #
            . # # . .
            . . # . .
        """)
        pressed = True
        lastState = "LEFT"

    elif pins.digital_read_pin(DigitalPin.P14) == 0: 
        radio.send_string("B")
        basic.show_leds("""
            . . # . .
            . . # . .
            # # # # #
            . # # # .
            . . # . .
        """)
        pressed = True
        lastState = "BACKWARDS"

    if not pressed and lastState != "STOP":
        radio.send_string("S")
        radio.send_string("S")
        basic.show_leds("""
            . . . . .
            . . . . .
            # # # # #
            . . . . .
            . . . . .
        """)
        lastState = "STOP"

def joystick():
    global lastState
    X = pins.analog_read_pin(AnalogPin.P1)
    Y = pins.analog_read_pin(AnalogPin.P2)

    pressed = False

    if Y < 300: 
        radio.send_string("B")
        basic.show_leds("""
            . . # . .
            . . # . .
            # # # # #
            . # # # .
            . . # . .
        """)
        pressed = True
        lastState = "BACKWARDS"

    elif Y > 700: 
        radio.send_string("F")
        basic.show_leds("""
            . . # . .
            . # # # .
            # # # # #
            . . # . .
            . . # . .
        """)
        pressed = True
        lastState = "FORWARD"

    elif X < 300: 
        radio.send_string("L")
        basic.show_leds("""
            . . # . .
            . # # . .
            # # # # #
            . # # . .
            . . # . .
        """)
        pressed = True
        lastState = "LEFT"

    elif X > 700:
        radio.send_string("R")
        basic.show_leds("""
            . . # . .
            . . # # .
            # # # # #
            . . # # .
            . . # . .
        """)
        pressed = True
        lastState = "RIGHT"

    if not pressed and lastState != "STOP":
        radio.send_string("S")
        basic.show_leds("""
            . . . . .
            . . . . .
            # # # # #
            . . . . .
            . . . . .
        """)
        lastState = "STOP"

def power_tilt(value: int):

# positiv value from 0 to 100%, where the power is 1023
    value = abs(value)
    force = value * 100 // 1023

    # Min
    if force < 10:
        force = 10

    # Max
    if force > 100:
        force = 100

    return force


def tilt():
    xx = input.acceleration(Dimension.X)
    yy = input.acceleration(Dimension.Y)

    if yy < -300: 
        radio.send_string("F" + str(power_tilt(yy)))
        basic.show_leds("""
            . . # . .
            . # # # .
            # # # # #
            . . # . .
            . . # . .
        """)
    elif yy > 300: 
        radio.send_string("B" + str(power_tilt(yy)))
        basic.show_leds("""
            . . # . .
            . . # . .
            # # # # #
            . # # # .
            . . # . .
        """)
    elif xx < -300: 
        radio.send_string("L" + str(power_tilt(xx)))
        basic.show_leds("""
            . . # . .
            . # # . .
            # # # # #
            . # # . .
            . . # . .
        """)
    elif xx > 300: 
        radio.send_string("R" + str(power_tilt(xx)))
        basic.show_leds("""
            . . # . .
            . . # # .
            # # # # #
            . . # # .
            . . # . .
        """)
    else: 
        radio.send_string("S")
        basic.show_leds("""
            . . . . .
            . . . . .
            # # # # #
            . . . . .
            . . . . .
        """)

def on_forever():
    global mode
    L1 = pins.digital_read_pin(DigitalPin.P15) == 0 
    R1 = pins.digital_read_pin(DigitalPin.P16) == 0 

    if L1 and R1:
        mode = 0
        vis_mode("S")

    elif L1 and not R1 and mode != 1:
        mode = 1
        vis_mode("J")

    elif R1 and not L1 and mode != 2:
        mode = 2
        vis_mode("T")

    if mode == 0:
        buttons()
    elif mode == 1:
        joystick()
    elif mode == 2:
        tilt()

    basic.pause(10)

basic.forever(on_forever)
