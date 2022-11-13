"""
This is the python translation of the code on the M5.
The code is the UIFlow version - this is just a mirror
"""

from m5stack import *
from m5ui import *
from uiflow import *
import urequests
import json

from easyIO import *
import wifiCfg
import time


setScreenColor(0x111111)


message = None



label0 = M5TextBox(7, 225, "label0", lcd.FONT_Default, 0xFFFFFF, rotate=270)
label1 = M5TextBox(109, 225, "label1", lcd.FONT_Default, 0xFFFFFF, rotate=270)



def buttonA_wasPressed():
  global message
  try:
    req = urequests.request(method='GET', url='http://192.168.1.18:8000/button', headers={})
  except:
    label1.setText(str(req.status_code))
  message = json.loads((req.text))
  label0.setText(str(message['messages']))
  M5Led.on()
  wait(0.1)
  M5Led.off()
  pass
btnA.wasPressed(buttonA_wasPressed)


label0.setText('Waiting for WiFi')
label1.setText(str(map_value((axp.getBatVoltage()), 3.7, 4.1, 0, 100)))
wifiCfg.autoConnect(lcdShow=False)
label0.setText('Waiting For Button')
