import RPi.GPIO as GPIO
import time
import math

data_pin1 = 21  # シリアルデータ1
latch_pin1 = 20  # ラッチクロック1
clock_pin1 = 19  # シフトレジスタクロック1

GPIO.setmode(GPIO.BCM)
GPIO.setup(data_pin1,GPIO.OUT)
GPIO.setup(latch_pin1,GPIO.OUT)
GPIO.setup(clock_pin1,GPIO.OUT)
#row 1
#b1 = int('00000000' ,2 )
#row2
#b2 = int('00000000' ,2 )
#row3
#b3 = int('00000000' ,2 )
#you can give a gap, if you want to do nothing for 1 row
gap = int('00000000' ,2 )
#bool
alltrue= int('11111111',2)


#test
class vibePattern:
	
	def __init__(self):
		self.b1= 0
		self.b2= 0
		self.b3 =0
		print('vibe Pattern start')
		
	def sound2vibe (self,num):
		#do re mi.. =  7 6 5 4 ...
		self.b1 = int( format(num & alltrue,'08b'),2 )
		print(self.b1)
		for i in range (8):
			num = num >> 1
		#row2
		self.b2 = int(format(num & alltrue,'08b') ,2 )
		
		print(self.b2)
		for i in range (8):
			num=num >> 1
		#row3
		self.b3 = int(format(num & alltrue,'08b') ,2 )
	
		print(self.b3)

	def set_b_values(self, value):
		if 0 <= value <= 7:
			b1 = 1 << (7 - value)
			self.b1 = int(format(b1 & alltrue,'08b'),2 )
		elif 8 <= value <= 15:
			b2 = 1 << (15 - value)
			self.b2 = int(format(b2 & alltrue,'08b') ,2 )
		elif 16 <= value <= 23:
			b3 = 1 << (23 - value)	
			self.b3 = int(format(b3 & alltrue,'08b') ,2 )
		elif value == -100:
			self.b1 = 0
			self.b2 = 0
			self.b3 = 0

	def vibe(self):
		GPIO.output(latch_pin1, GPIO.LOW)
		#row 3 control
		print(self.b1)
		print(self.b2)
		print(self.b3)
		for i in range (8):
			GPIO.output(clock_pin1,GPIO.LOW)
			GPIO.output(data_pin1,(self.b3 >> i)&1)
			GPIO.output(clock_pin1,GPIO.HIGH)
			#give data and make clock 

		#row 2 control
		for i in range (8):
			GPIO.output(clock_pin1,GPIO.LOW)
			GPIO.output(data_pin1,(self.b2 >> i)&1)
			GPIO.output(clock_pin1,GPIO.HIGH)

		#row 1 control
		for i in range (8):
			GPIO.output(clock_pin1,GPIO.LOW)
			GPIO.output(data_pin1,(self.b1 >> i)&1)
			GPIO.output(clock_pin1,GPIO.HIGH)

		GPIO.output(latch_pin1, GPIO.HIGH)
		#start to vibe at this time actually (human cannot notice though)
		'''
		try:
			while True:
				pass
		except KeyboardInterrupt:
			GPIO.cleanup()
		'''

if __name__ == "__main__":
	test = vibePattern()
	n = 0
	test.set_b_values(n)
	test.vibe()
	time.sleep(5)
	print("a")
	test.set_b_values(-100)
	test.vibe()
	GPIO.cleanup()
