import RPi.GPIO as GPIO
from shiftr_74HC595.shiftr_74HC595 import ShiftRegister
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

data_pin1 = 21  # シリアルデータ1
latch_pin1 = 20  # ラッチクロック1
clock_pin1 = 19  # シフトレジスタクロック1


shift_register1 = ShiftRegister(data_pin1, latch_pin1, clock_pin1)
#shift_register2 = ShiftRegister(data_pin1, LO, clock_pin1)
#shift_register3 = ShiftRegister(data_pin1, latch_pin1, clock_pin1)

try:
    while True:
        shift_register1.setOutput(0, GPIO.LOW)
        shift_register1.latch()

        sleep(0.05)
        #for i in range(12):
        '''
            if i < 8:
                shift_register1.setOutput(i, GPIO.HIGH)
            else:
                shift_register2.setOutput(i - 8, GPIO.HIGH)
            '''
            
        '''
        for i in range(12):
            if i < 8:
                shift_register1.setOutput(i, GPIO.LOW)
            else:
                shift_register2.setOutput(i - 8, GPIO.LOW)

            shift_register1.latch()
            shift_register2.latch()
            sleep(0.05)
           '''

except KeyboardInterrupt:
    shift_register1.setOutputs([GPIO.LOW] * 24)
    shift_register1.latch()
    print("Ctrl-C - quit")

GPIO.cleanup()
