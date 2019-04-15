from m5stack import *
from m5ui import *
from m5_pin import *
from hardware import sh200q

clear_bg(0x000000)


pin = M5_Pin()
imu = sh200q.Sh200q()
image2 = M5Img(0, 41, "res/Laserblk2.jpg", True)
label1 = M5TextBox(2, 3, "Laser Bed", lcd.FONT_Default,0xffffff, rotate=0)
label2 = M5TextBox(0, 13, "Controller", lcd.FONT_Default,0xffffff, rotate=0)
height = M5TextBox(23, 129, "0", lcd.FONT_DejaVu18,0xffffff, rotate=0)
multiplier_label = M5TextBox(49, 146, "x", lcd.FONT_DefaultSmall,0xFFFFFF, rotate=0)
multiplier = M5TextBox(57, 146, "1", lcd.FONT_Default,0xFFFFFF, rotate=0)

import math

multipliercnt = None
threshold = None
j = None
lowthreshold = None
dir_pin = None
pul_pin = None
pulse_int = None
ispulse = None

def thresholdmet():
  global multipliercnt, threshold, j, lowthreshold, dir_pin, pul_pin, pulse_int, ispulse
  M5LED.on()
  pin.digitalWrite(dir_pin, 0)
  pulse()

def lowthresholdmet():
  global multipliercnt, threshold, j, lowthreshold, dir_pin, pul_pin, pulse_int, ispulse
  M5LED.on()
  pin.digitalWrite(dir_pin, 1)
  pulse()

def thresholdunmet():
  global multipliercnt, threshold, j, lowthreshold, dir_pin, pul_pin, pulse_int, ispulse
  M5LED.off()
  p26.deinit()

def upRange(start, stop, step):
  while start <= stop:
    yield start
    start += abs(step)

def downRange(start, stop, step):
  while start >= stop:
    yield start
    start -= abs(step)

def pulse():
  global multipliercnt, threshold, j, lowthreshold, dir_pin, pul_pin, pulse_int, ispulse
  for j in (0 <= float(multipliercnt)) and upRange(0, float(multipliercnt), 1) or downRange(0, float(multipliercnt), 1):
    #pin.digitalWrite(pul_pin, 0)
    #pin.digitalWrite(pul_pin, 1)
    p26.init(int(round(abs(imu.ypr[2]))) * 50)


def buttonB_pressed():
  global multipliercnt, threshold, lowthreshold, dir_pin, pul_pin, pulse_int, ispulse, pin
  multipliercnt = 1
  multiplier.setText(str(multipliercnt))
  pass
buttonB.wasPressed(callback=buttonB_pressed)
threshold = 30
lowthreshold = -30
dir_pin = 33
pul_pin = 32
pulse_int = 350
ispulse = 0
multipliercnt = 1
pin.digitalWrite(dir_pin, 0)
pin.digitalWrite(pul_pin, 0)

p26 = machine.PWM(pul_pin, freq=5000, duty=50)

while True:
  if (imu.ypr[2]) > threshold:
    thresholdmet()
  else:
    if (imu.ypr[2]) < lowthreshold:
      lowthresholdmet()
    else:
      thresholdunmet()
  height.setText(str(math.ceil(imu.ypr[2])))
  if buttonA.wasPressed():
    if multipliercnt < 127:
      multipliercnt = multipliercnt * 2
      multiplier.setText(str(multipliercnt))
      print(multipliercnt)
    else:
      multipliercnt = 1
      multiplier.setText(str(multipliercnt))
  wait(0.001)

