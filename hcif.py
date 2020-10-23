#!/usr/bin/env python

# hcif.py
# 2020-03-31 (Day 15 of CoViD19-Lockdown in Austria)
# Public Domain
# Based on _433.py from abyz.me.uk/rpi/pigpio/examples.html (http://abyz.me.uk/rpi/pigpio/code/_433_py.zip)


"""
This module provides the receiver class to use with heating 
controllers from Technische Alternative RT GmbH.
The rx class decodes the data line signal from the heating controller (HC)
Only compatible to following devices (By 2020-03-31)

UVR64
HZR65

"""
import time
import pigpio
import logging

logging.basicConfig(
   format="%(asctime)s - %(levelname)s - %(message)s", 
   level = logging.ERROR
)
class rx():
   """
   A class to read data transmitted by HC.
   """


   # Constants

   # Byte types for mapping
   # Device type
   HC_DEF_MAP_BYTE_TYPE_DEVICE = 0
   # Temperature
   HC_DEF_MAP_BYTE_TYPE_TEMP = 1
   # Outputs
   HC_DEF_MAP_BYTE_TYPE_OUT = 2

   # High/Low Byte for mapping of word sized values
   # Neither
   HC_DEF_MAP_BYTE_HILO_NONE = -1
   # Low byte
   HC_DEF_MAP_BYTE_HILO_LOW = 0
   # High byte
   HC_DEF_MAP_BYTE_HILO_HIGH = 1



   HC_DEF = {
      
      # Definition of the different heating controllers
      # Each item consists of the following attributes:
      
      # key            datatype             description
      # ------------------------------------------------------------------------------------------------
      # device type    string                Type of the heating controller
      # clock period   float                 Clock period of the heating controller in µs
      # byte count     int                   Count of bytes transmitted
      # byte mapping   tuple of dict         Mapping of each byte consisting of:
      #    name        string                Name of the value stored in this byte
      #    type        int                   Which kind of value is it (0: devicetype, 1: temperature, 2: output)
      #    hilo        int                   If type == 1: High (1) or low (0) byte?; else -1
      #    bit mapping tuple of int          If type == 2: Mapping of each output to a byte; else empty
      #    scale       float                 Scale of the byte (value = byte * scale)
      32 : {
         "device type" : "UVR64", 
         "clock_period" : 20000,
         "byte count" : 14,
         "byte mapping" : (
            {
               "name" : "devicetype",
               "type" : HC_DEF_MAP_BYTE_TYPE_DEVICE,
               "hilo" : HC_DEF_MAP_BYTE_HILO_NONE,
               "bit mapping" : (),
               "scale" : 1
            },
            {
               "name" : "temp1",
               "type" : HC_DEF_MAP_BYTE_TYPE_TEMP,
               "hilo" : HC_DEF_MAP_BYTE_HILO_LOW,
               "bit mapping" : (),
               "scale" : 0.1
            },
            {
               "name" : "temp1",
               "type" : HC_DEF_MAP_BYTE_TYPE_TEMP,
               "hilo" : HC_DEF_MAP_BYTE_HILO_HIGH,
               "bit mapping" : (),
               "scale" : 0.1
            },
            {
               "name" : "temp2",
               "type" : HC_DEF_MAP_BYTE_TYPE_TEMP,
               "hilo" : HC_DEF_MAP_BYTE_HILO_LOW,
               "bit mapping" : (),
               "scale" : 0.1
            },
            {
               "name" : "temp2",
               "type" : HC_DEF_MAP_BYTE_TYPE_TEMP,
               "hilo" : HC_DEF_MAP_BYTE_HILO_HIGH,
               "bit mapping" : (),
               "scale" : 0.1
            },
            {
               "name" : "temp3",
               "type" : HC_DEF_MAP_BYTE_TYPE_TEMP,
               "hilo" : HC_DEF_MAP_BYTE_HILO_LOW,
               "bit mapping" : (),
               "scale" : 0.1
            },
            {
               "name" : "temp3",
               "type" : HC_DEF_MAP_BYTE_TYPE_TEMP,
               "hilo" : HC_DEF_MAP_BYTE_HILO_HIGH,
               "bit mapping" : (),
               "scale" : 0.1
            },
            {
               "name" : "temp4",
               "type" : HC_DEF_MAP_BYTE_TYPE_TEMP,
               "hilo" : HC_DEF_MAP_BYTE_HILO_LOW,
               "bit mapping" : (),
               "scale" : 0.1
            },
            {
               "name" : "temp4",
               "type" : HC_DEF_MAP_BYTE_TYPE_TEMP,
               "hilo" : HC_DEF_MAP_BYTE_HILO_HIGH,
               "bit mapping" : (),
               "scale" : 0.1
            },
            {
               "name" : "temp5",
               "type" : HC_DEF_MAP_BYTE_TYPE_TEMP,
               "hilo" : HC_DEF_MAP_BYTE_HILO_LOW,
               "bit mapping" : (),
               "scale" : 0.1
            },
            {
               "name" : "temp5",
               "type" : HC_DEF_MAP_BYTE_TYPE_TEMP,
               "hilo" : HC_DEF_MAP_BYTE_HILO_HIGH,
               "bit mapping" : (),
               "scale" : 0.1
            },
            {
               "name" : "temp6",
               "type" : HC_DEF_MAP_BYTE_TYPE_TEMP,
               "hilo" : HC_DEF_MAP_BYTE_HILO_LOW,
               "bit mapping" : (),
               "scale" : 0.1
            },
            {
               "name" : "temp6",
               "type" : HC_DEF_MAP_BYTE_TYPE_TEMP,
               "hilo" : HC_DEF_MAP_BYTE_HILO_HIGH,
               "bit mapping" : (),
               "scale" : 0.1
            },
            {
               "name" : "output",
               "type" : HC_DEF_MAP_BYTE_TYPE_OUT,
               "hilo" : HC_DEF_MAP_BYTE_HILO_NONE,
               "bit mapping" : (
                  0,
                  0,
                  0,
                  0,
                  1,
                  2,
                  3,
                  4
               ),
               "scale" : 1
            }
         )
      },
      96 : {
         "device type" : "HZR65", 
         "clock_period" : 20000,
         "byte count" : 14,
         "byte mapping" : (
            {
               "name" : "devicetype",
               "type" : HC_DEF_MAP_BYTE_TYPE_DEVICE,
               "hilo" : HC_DEF_MAP_BYTE_HILO_NONE,
               "bit mapping" : (),
               "scale" : 1
            },
            {
               "name" : "temp1",
               "type" : HC_DEF_MAP_BYTE_TYPE_TEMP,
               "hilo" : HC_DEF_MAP_BYTE_HILO_LOW,
               "bit mapping" : (),
               "scale" : 0.1
            },
            {
               "name" : "temp1",
               "type" : HC_DEF_MAP_BYTE_TYPE_TEMP,
               "hilo" : HC_DEF_MAP_BYTE_HILO_HIGH,
               "bit mapping" : (),
               "scale" : 0.1
            },
            {
               "name" : "temp2",
               "type" : HC_DEF_MAP_BYTE_TYPE_TEMP,
               "hilo" : HC_DEF_MAP_BYTE_HILO_LOW,
               "bit mapping" : (),
               "scale" : 0.1
            },
            {
               "name" : "temp2",
               "type" : HC_DEF_MAP_BYTE_TYPE_TEMP,
               "hilo" : HC_DEF_MAP_BYTE_HILO_HIGH,
               "bit mapping" : (),
               "scale" : 0.1
            },
            {
               "name" : "temp3",
               "type" : HC_DEF_MAP_BYTE_TYPE_TEMP,
               "hilo" : HC_DEF_MAP_BYTE_HILO_LOW,
               "bit mapping" : (),
               "scale" : 0.1
            },
            {
               "name" : "temp3",
               "type" : HC_DEF_MAP_BYTE_TYPE_TEMP,
               "hilo" : HC_DEF_MAP_BYTE_HILO_HIGH,
               "bit mapping" : (),
               "scale" : 0.1
            },
            {
               "name" : "temp4",
               "type" : HC_DEF_MAP_BYTE_TYPE_TEMP,
               "hilo" : HC_DEF_MAP_BYTE_HILO_LOW,
               "bit mapping" : (),
               "scale" : 0.1
            },
            {
               "name" : "temp4",
               "type" : HC_DEF_MAP_BYTE_TYPE_TEMP,
               "hilo" : HC_DEF_MAP_BYTE_HILO_HIGH,
               "bit mapping" : (),
               "scale" : 0.1
            },
            {
               "name" : "temp5",
               "type" : HC_DEF_MAP_BYTE_TYPE_TEMP,
               "hilo" : HC_DEF_MAP_BYTE_HILO_LOW,
               "bit mapping" : (),
               "scale" : 0.1
            },
            {
               "name" : "temp5",
               "type" : HC_DEF_MAP_BYTE_TYPE_TEMP,
               "hilo" : HC_DEF_MAP_BYTE_HILO_HIGH,
               "bit mapping" : (),
               "scale" : 0.1
            },
            {
               "name" : "temp6",
               "type" : HC_DEF_MAP_BYTE_TYPE_TEMP,
               "hilo" : HC_DEF_MAP_BYTE_HILO_LOW,
               "bit mapping" : (),
               "scale" : 0.1
            },
            {
               "name" : "temp6",
               "type" : HC_DEF_MAP_BYTE_TYPE_TEMP,
               "hilo" : HC_DEF_MAP_BYTE_HILO_HIGH,
               "bit mapping" : (),
               "scale" : 0.1
            },
            {
               "name" : "output",
               "type" : HC_DEF_MAP_BYTE_TYPE_OUT,
               "hilo" : HC_DEF_MAP_BYTE_HILO_NONE,
               "bit mapping" : (
                  0,
                  0,
                  0,
                  1,
                  2,
                  3,
                  4,
                  5
               ),
               "scale" : 1
            }
         )
      }
   }
      
   def __init__(self, pi, gpio, controller, callback=None):
      """
      Instantiate with the Pi and the GPIO connected to the wireless
      receiver.

      If specified the callback will be called whenever a new code
      is received.

      """
      logging.debug("Initializing controller " + str(controller) + "...")

      self.pi = pi
      self.gpio = gpio
      self.cb = callback
      self.controller = controller

      self._risingCnt = 0
      self._bitcnt = 0
      self._bytes = []
      self._synced = 0

      self._data = {}
      self._devicedef = {}



      self._bytecnt = 0

      pi.set_mode(gpio, pigpio.INPUT)

      self._lastEdgeTimestamp = pi.get_current_tick()
      self._lastBitTimestamp = pi.get_current_tick()
      self._cb = pi.callback(gpio, pigpio.EITHER_EDGE, self._cbf)

      logging.debug("Controller " + str(self.controller) + " initialized")

   def _pulseLenght(self, pulseLen):
      """
      Determines if given pulse is a short or long pulse
      Returns: 1 for long pulse (With 50Hz clock: ~20ms)
               0 for short pulse (~10ms)
               -1 for invalid pulse (Outside of tolerance window)
      """
      if 9000 < pulseLen < 11000:
         # Short pulse
         logging.debug("Controller " + str(self.controller) + " sent a short pulse (" + str(pulseLen) + " ms)")
         return 0
      elif 18000 < pulseLen < 22000:
         # Long pulse
         logging.debug("Controller " + str(self.controller) + " sent a long pulse (" + str(pulseLen) + " ms)")
         return 1
      else:
         logging.info("Controller " + str(self.controller) + " sent a invalid pulse (" + str(pulseLen) + " ms)")
         return -1

   def _cbf(self, g, l, t):
      """
      Accumulates the code from pairs of short/long pulses.
      The code end is assumed when an edge greater than 5 ms
      is detected.
      """

      _pulseLen =  self._pulseLenght(pigpio.tickDiff(self._lastEdgeTimestamp, t))
      self._lastEdgeTimestamp = t

      # Count rising edges
      if _pulseLen == 0:
         self._risingCnt += l
      else:
         self._risingCnt = 0
      
      logging.debug("Controller " + str(self.controller) + ": " + str(self._risingCnt) + " rising edges detected")

      if self._risingCnt >= 16:
         logging.info("Controller " + str(self.controller) + ": SYNC sequence detected")
         logging.debug("Controller " + str(self.controller) + ": " + str(len(self._bytes)) + " Bytes of data were received before")
         logging.debug("Controller " + str(self.controller) + ": " "Data contained: " + str(self._bytes))

         self._lastBitTimestamp = t

         self._data = {}
         
         if (len(self._bytes) > 0) and (self._bytes[0] in self.HC_DEF):
            # devicetype is in the first byte
            _devicedef = self.HC_DEF[self._bytes[0]]
            if (len(_devicedef) <> len(self._bytes)):
               # Invalid count of bytes received
               self._risingCnt = 0
               self._synced = False
               logging.warning("Controller " + str(self.controller) + ": Received " + str(len(self._bytes)) + "instead of " + len(_devicedef) + " bytes")
            else:
               for i, b in enumerate(self._bytes):
                  _bytemapping = _devicedef["byte mapping"][i]
                  b = b * _bytemapping["scale"]
                  if _bytemapping["type"] == self.HC_DEF_MAP_BYTE_TYPE_OUT:
                     # Outputs, get single bits of each one
                     bitMapping = _bytemapping["bit mapping"]
                     for i, out in enumerate(bitMapping):
                        if out > 0:
                           self._data[_bytemapping["name"] + str(out)] = (b & (1 << i)) > 0

                  elif _bytemapping["type"] == self.HC_DEF_MAP_BYTE_TYPE_DEVICE:
                     # device type
                     self._data[_bytemapping["name"]] = _devicedef["device type"]

                  elif _bytemapping["hilo"] == self.HC_DEF_MAP_BYTE_HILO_NONE:
                     # just a single byte
                     self._data[_bytemapping["name"]] = b

                  elif _bytemapping["hilo"] == self.HC_DEF_MAP_BYTE_HILO_HIGH:
                     # just a single byte
                     if _bytemapping["name"] in self._data:
                        self._data[_bytemapping["name"]] += b * 256
                     else:
                        self._data[_bytemapping["name"]] = b * 256

                  elif _bytemapping["hilo"] == self.HC_DEF_MAP_BYTE_HILO_LOW:
                     # just a single byte
                     if _bytemapping["name"] in self._data:
                        self._data[_bytemapping["name"]] += b
                     else:
                        self._data[_bytemapping["name"]] = b


            self.cb(self.controller, self._data)

         self._bytecnt = 0
         self._synced = True

         # Reset bytes
         self._bytes = []
         self._bitcnt = 0

      if (not self._synced):
         logging.debug("Controller " + str(self.controller) + " lost sync")

      if self._synced:
         if self._pulseLenght(pigpio.tickDiff(self._lastBitTimestamp, t)) == 1:
            self._lastBitTimestamp = t
            self._bitcnt += 1

            if self._bitcnt == 1:
               # First bit is the start bit, has to be 1
               if l != 1:
                  self._synced = False
                  logging.warning("Controller " + str(self.controller) + ": Invalid start bit")
                  return
               
               # Start new Byte
               self._bytes.append(0)

            elif self._bitcnt == 10:
               # 10th bit is the stop bit, has to be 0
               # Byte is complete
               self._bitcnt = 0
               self._bytecnt += 1

               if l != 0:
                  self._synced = False
                  logging.warning("Controller " + str(self.controller) + ": Invalid stop bit")
                  return
               
               logging.debug("Controller " + str(self.controller) + " Byte complete. Value: " + str(self._bytes[-1]))
               

            else:
               # Actual bit
               self._bytes[len(self._bytes) - 1] +=  (1 - l) * (1 << (self._bitcnt - 2))

      
   def cancel(self):
      """
      Cancels the receiver.
      """
      if self._cb is not None:
         self._cb.cancel()
         self._cb = None

# Test implementation
if __name__ == "__main__":

   import sys
   import time
   import pigpio
   import hcif

   RX=4

   # define optional callback for received codes.

   def rx_callback(data):
      print(data)

   pi = pigpio.pi() # Connect to local Pi.
   rx=hcif.rx(pi, gpio=RX, callback=rx_callback, controller=1)
   time.sleep(10)
   rx.cancel() # Cancel the receiver.
   pi.stop() # Disconnect from local Pi.


