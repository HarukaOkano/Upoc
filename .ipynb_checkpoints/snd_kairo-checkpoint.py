from socket import *
import RPi.GPIO as GPIO
import time
import math
from gpiozero import MCP3208

Vref = 5

def analog_read(channel):
    pot = MCP3208(channel)
    volt = pot.value * Vref
    return volt
GPIO.setmode(GPIO.BCM)
SENSOR_PIN = 0
VALUE_1 = 170
POSITION_1 = 20.0
VALUE_2 = 440
POSITION_2 = 50.0

MELODY_LENGTH = 200  # Length of the sound in milliseconds
BUZZER_PIN = 17  # GPIO pin number to connect the buzzer
A_0 = 262  # Frequency of note "do" in Hz (the base frequency)
K = 0.08
R = pow(2, K)  # Each note frequency increment ratio

def map_value(input_value, input_min, input_max, output_min, output_max, constrain=False):
    output_value = (input_value - input_min) * (output_max - output_min) / (input_max - input_min) + output_min
    if constrain:
        output_value = max(min(output_value, output_max), output_min)
    return output_value

def setup():
    GPIO.setup(BUZZER_PIN, GPIO.OUT)

def loop():
    while True:
        i_value = analog_read(0) 
        #print(i_value)
        d_position = map_value(i_value, VALUE_1, VALUE_2, POSITION_1, POSITION_2, False)
        print(d_position)
        if i_value <= 0.5:
            GPIO.output(BUZZER_PIN, GPIO.LOW)  # Turn off the buzzer
        else:
            GPIO.output(BUZZER_PIN, GPIO.HIGH) # Turn on the buzzer
            time.sleep(MELODY_LENGTH / 1000.0)
            GPIO.output(BUZZER_PIN, GPIO.LOW)  # Turn off the buzzer

        time.sleep(0.01)  # Small delay between readings

def poscal():
    i_value = analog_read(0)
    d_position = map_value(i_value, VALUE_1, VALUE_2, POSITION_1, POSITION_2, False)
    print(d_position)

def test():
    print("a")

if __name__ == "__main__":
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        GPIO.cleanup()
