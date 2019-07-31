import webiopi

GPIO = webiopi.GPIO

L1=20
L2=21
LS=26

R1=6
R2=13
RS=12

# -------------------------------------------------- #
# Convenient PWM Function                            #
# -------------------------------------------------- #

# Set the speed of two motors
def set_speed(speed):
    GPIO.output(LS,GPIO.HIGH)
    GPIO.output(LS,GPIO.HIGH)
# -------------------------------------------------- #
# Left Motor Functions                               #
# -------------------------------------------------- #

def left_stop():
    GPIO.output(L1, GPIO.LOW)
    GPIO.output(L2, GPIO.LOW)

def left_forward():
    GPIO.output(L1, GPIO.HIGH)
    GPIO.output(L2, GPIO.LOW)

def left_backward():
    GPIO.output(L1, GPIO.LOW)
    GPIO.output(L2, GPIO.HIGH)

# -------------------------------------------------- #
# Right Motor Functions                              #
# -------------------------------------------------- #
def right_stop():
    GPIO.output(R1, GPIO.LOW)
    GPIO.output(R2, GPIO.LOW)

def right_forward():
    GPIO.output(R1, GPIO.LOW)
    GPIO.output(R2, GPIO.HIGH)

def right_backward():
    GPIO.output(R1, GPIO.HIGH)
    GPIO.output(R2, GPIO.LOW)

# -------------------------------------------------- #
# Macro definition part                              #
# -------------------------------------------------- #
@webiopi.macro
def go_forward():
    left_forward()
    right_forward()

@webiopi.macro
def go_backward():
    left_backward()
    right_backward()

@webiopi.macro
def turn_left():
    left_backward()
    right_forward()

@webiopi.macro
def turn_right():
    left_forward()
    right_backward()

@webiopi.macro
def stop():
    left_stop()
    right_stop()
    
# Called by WebIOPi at script loading
def setup():
    # Setup GPIOs
    GPIO.setFunction(LS, GPIO.OUT)
    GPIO.setFunction(L1, GPIO.OUT)
    GPIO.setFunction(L2, GPIO.OUT)
    
    GPIO.setFunction(RS, GPIO.OUT)
    GPIO.setFunction(R1, GPIO.OUT)
    GPIO.setFunction(R2, GPIO.OUT)
    GPIO.output(LS,GPIO.HIGH)
    GPIO.output(RS,GPIO.HIGH)
    
    GPIO.setFunction(24, GPIO.PWM)
    GPIO.setFunction(25, GPIO.PWM)

    stop()


# Called by WebIOPi at server shutdown
def destroy():
    # Reset GPIO functions
    GPIO.setFunction(LS, GPIO.IN)
    GPIO.setFunction(L1, GPIO.IN)
    GPIO.setFunction(L2, GPIO.IN)
    
    GPIO.setFunction(RS, GPIO.IN)
    GPIO.setFunction(R1, GPIO.IN)
    GPIO.setFunction(R2, GPIO.IN)
    
