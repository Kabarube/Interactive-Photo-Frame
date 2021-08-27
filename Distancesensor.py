import RPi.GPIO as GPIO
from time import sleep
from time import time

# Global pin variables
PIN_LED = 33
PIN_TRIGGER = 7
PIN_ECHO = 11
PWMFREQ = 75


# Function for setting up output and input pins
def sensorsetup():
    # GPIO Setup procedure
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    # Distance sensor setup
    GPIO.setup(PIN_TRIGGER, GPIO.OUT)
    GPIO.setup(PIN_ECHO, GPIO.IN)
    # Led dimmer setup
    GPIO.setup(PIN_LED, GPIO.OUT)
    # Turn on led array
    global dimmer
    dimmer = GPIO.PWM(PIN_LED, PWMFREQ)
    dimmer.start(1)
    # Waiting for sensor to stabalize
    GPIO.output(PIN_TRIGGER, GPIO.LOW)

    print("Sensoren stabiliserer seg")
    sleep(2)

# Function for measuring the actual distance.
# Returns distance in centimeter
def measuredistance():

    # Calling sensor to calculate distance
    GPIO.output(PIN_TRIGGER, GPIO.HIGH)
    sleep(0.00001)
    GPIO.output(PIN_TRIGGER, GPIO.LOW)

    while GPIO.input(PIN_ECHO) == 0:
        pulse_start_time = time()
    while GPIO.input(PIN_ECHO) == 1:
        pulse_end_time = time()

    # Distance calculation
    pulse_duration = pulse_end_time - pulse_start_time
    distance = round(pulse_duration * 17150, 0)

    # #print("Distance: ", distance, "cm") --maybe remove
    sleep(0.075)

    return distance

# Function for changing brightness of LED array
def dimmingled(repdistance):

    # Change brightness based on distance value
    if repdistance < 100:
        dimmer.ChangeDutyCycle(100 - repdistance)
    else:
        dimmer.ChangeDutyCycle(0)
    sleep(0.01)


# Initialize sensors
def main():
    try:
        sensorsetup()

        avgdistance = []

        while True:

            avgdistance.append(measuredistance())
            if len(avgdistance) >= 5:
                avgdistance.pop(0)

            print(avgdistance)
            dimmingled(round(sum(avgdistance) / len(avgdistance)))

    except KeyboardInterrupt:
        print("\nBye bye")

    finally:
        GPIO.cleanup()
        print("\nCleanup done")
        dimmer.stop()


main()
