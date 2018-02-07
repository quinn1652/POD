import os, sys, time, datetime as datetime
import requests
import threading

import RPi.GPIO as GPIO # from pi zero light driver code

#from tsl2561 import TSL2561 as getLightSensor
import tsl2591
import Adafruit_MCP9808.MCP9808 as tempLib

# potentially break exceptions into specific errors (disconnects, odd values, w/e)
class LightSensorException(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

class TempSensorException(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

# intended for use with an Adafruit TSL2561 breakout board
class LightSensor():
    def __init__(self):
        #self.sensor = getLightSensor(debug=1)
        self.sensor = tsl2591.Tsl2591()
        if (self.sensor is None):
          raise LightSensorException(0); #change return val to the sensors default i2c address

    def getReading(self):
      #lux = self.sensor.lux()
      full, ir = self.sensor.get_full_luminosity()
      lux = self.sensor.calculate_lux(full, ir)
      if lux is not None:
        return lux
      else:
        raise LightSensorException(0)

    def printReading(self, lightFile):
      lux = self.getReading()
      print 'L{' + str(lux) + ',' +  time.strftime("%Y-%m-%d-%H:%M:%S") + '}'
      lightFile.write(str(lux) + "\n")

#intended for use with an Adafruit MCP9808 breakout board
class TempSensor():
    def __init__(self):
        self.sensor = tempLib.MCP9808()
        self.sensor.begin()
    def getReading(self):
        return self.sensor.readTempC()
    def printReading(self, tempFile):
      #print '{0:0.3F} , {0:0.3F}'(self.sensor.readTempC(), time.clock())
      print 'T{' + str(self.getReading()) + ',' + time.strftime("%Y-%m-%d-%H:%M:%S") + '}'
      tempFile.write(str(self.getReading()) + "\n")

class Lights():
    def __init__(self, expEnd, maxBright, onTime, offTime):
        try:
            self.frequencyOn = onTime
            self.frequencyOff = offTime
            self.pPercent = maxBright
            self.fade = 0
            self.endTime = expEnd
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(12, GPIO.OUT)
            #need pPercent power code
            self.lightPin = GPIO.PWM(12, 100) #channel 12, 100Hz
        except:
            print "Unexpected error in Lights init: ", sys.exc_info()[0]
            sys.exit(0)
            
    def run(self, thread):
        try:
            self.lightPin.start(1)
            if (self.fade == 0): #no fading, just hard off and on
            	#loop until we hit endTime
                print "hello??"
                while time.time() < self.endTime and thread.stopped() == False:
                    #light on
                    if self.frequencyOn > 0:
                      self.lightPin.ChangeDutyCycle(self.pPercent)
                      time.sleep(self.frequencyOn)
                    #light off
                    if self.frequencyOff > 0:
                      self.lightPin.ChangeDutyCycle(0)
                      time.sleep(self.frequencyOff)
        except:
            print "Unexpected error in Lights run() (likely pwm error): ", sys.exc_info()[0]
            sys.exit(0)

class WaterPump():
    def __init__(self, onTime):
        try:
            self.timeOn = onTime
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(11, GPIO.OUT)
            #need pPercent power code
            self.pumpPin = GPIO.PWM(11, 100) #channel 11, 100Hz
        except:
            print "Unexpected error in Pump init: ", sys.exc_info()[0]
            sys.exit(0)
            
    def run(self):
        try:
            self.pumpPin.start(1)
            #pump on
            print("on")
            self.pumpPin.ChangeDutyCycle(100)
            time.sleep(self.timeOn)
            #pump off
            print("off")
            self.pumpPin.ChangeDutyCycle(0)
                
        except:
            print "Unexpected error in Pump run() (likely pwm error): ", sys.exc_info()[0]
            sys.exit(0)

threadsStarted = False

def main():
    experimentEndLine = 6
    
    while os.path.isfile("id.txt") is False:
        #contact server for id
        try:
            r = requests.get('http://192.168.1.100/getId.php')
            idFile = open("id.txt", "w")
            idFile.write(r.text)
            idFile.close()
            time.sleep(5)
        except:
            print("can't connect for id")
            time.sleep(5)
    
    idFile = open("id.txt", "r")
    id = int(idFile.readline())
    name = str(id)
    expName = ""
    expDur = 0
    expPhotos = 0
    expWater = 0.0
    expStart = 0.0
    expEnd = 0.0
    lightOnTime = 0.0
    lightOffTime = 0.0
    lightBrightness = 0.0
    threads = []

    #get string representation of id so we can find ourselves in config
    if id < 10:
        name = "00" + name
    elif id < 100:
        name = "0" + name
    
    while True:
        time.sleep(5)
        config = getConfig(str(id), threads)
        print(config)

        #parse out experiment variables
        configfile = open("config.txt", "r")
        expName = configfile.readline()
        expDur = int(configfile.readline())
        expPhotos = int(configfile.readline())
        expWater = float(configfile.readline())
        expStart = float(configfile.readline())
        expEnd = float(configfile.readline())
        print(expEnd)

        foundConfig = False
        
        for line in configfile:
            split = line.split(',')
            if split[0] == ("POD " + name):
                #this is the config for this pod
                foundConfig = True
                lightOnTime = float(split[1])
                lightOffTime = float(split[2])
                lightBrightness = float(split[3])
                
        configfile.close()
        print(str(lightOnTime) + " " + str(lightOffTime) + " " + str(lightBrightness))

        if time.time() > expEnd:
            #experiment is over
            endExperiment(threads)
            threadsStarted = False
            
        elif foundConfig == True:
            #spawn threads for each thing
            #some timer for sending back data to main computer
            #check if exp is over
            lightSensor = None
            tempSensor = None
            pump = None
            global threadsStarted
            if threadsStarted == False:
                try:
                    lightSensor = LightSensor()
                    tempSensor = TempSensor()
                except:
                    print("Sensors not connected")

                try:
                    lights = Lights(expEnd, 5, lightOnTime, lightOffTime)
                except:
                    print("oh nooooo")

                try:
                    pump = WaterPump(expWater)
                except:
                    print("Pump not connected")
                    
                threads.append(Thread_test(runSensors,lightSensor, tempSensor, expEnd, id))
                threads.append(Thread_test(runLights, lights))
                threads.append(Thread_test(runWaterPump, pump, expEnd))
                threadsStarted = True
            
class Thread_test(threading.Thread):
    def __init__(self, function, *args):
        self._stop_event = threading.Event()
        self._function = function
        self._args = args + (self,)
        threading.Thread.__init__(self)
        self.start()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        self._function(*self._args)            

def runLights(lights, thread):
    lights.run(thread)

def runWaterPump(pump, endTime, thread):
    givenWater = False
    if pump is not None:        
        while time.time() < endTime and thread.stopped() == False:
            if (datetime.datetime.today().hour == 20 and givenWater == False):
                try:
                    print("running water")
                    pump.run()
                    givenWater = True
                except:
                    givenWater = False
            elif (datetime.datetime.today().hour != 20):
                givenWater = False
            time.sleep(60)
                         

def runSensors(lightSensor, tempSensor, endTime, podId, thread):
    while time.time() < endTime and thread.stopped() == False:
        if lightSensor is None:
            try:
                lightSensor = LightSensor()
            except:
                print("Light Sensor not connected")

        if tempSensor is None:
            try:
                temSensor = TempSensor()
            except:
                print("Temp Sensor not connected")
                
        lightFile = open("light.txt", "a+")
        tempFile = open("temp.txt", "a+")
            
        if lightSensor is not None:
            lightSensor.printReading(lightFile)
        else:
            lightFile.write("-1\n")

        if tempSensor is not None:
            tempSensor.printReading(tempFile)
        else:
            tempFile.write("-1\n")

        lightFile.close()
        tempFile.close()

        #send data to host
	host = 'http://192.168.1.100/reportLight.php'
	lightFile = open("light.txt", "r")
	payload = str(lightFile.read())
	data = {'value':payload, 'id': podId}
	try:
		print("trying to connect")
		r = requests.post(host, data)
	except:
		print("not connecting")
	lightFile.close()

	host = 'http://192.168.1.100/reportTemp.php'
	tempFile = open("temp.txt", "r")
	payload = str(tempFile.read())
	data = {'value':payload, 'id':podId}
	try:
            r = requests.post(host, data)
        except:
            print("not connecting")
            
        time.sleep(5)

def endExperiment(threads):
    for thread in threads:
        thread.stop()
        thread.join()

    try:
      os.remove("light.txt")
    except:
      print("no light file")
    try:
      os.remove("temp.txt")
    except:
      print("no temp file")
    try:
      os.remove("config.txt")
    except:
      print("no config")
    global threadsStarted
    threadsStarted = False

def getConfig(name,threads):
    host = 'http://192.168.1.100/addPod.php'
    #while os.path.isfile("config.txt") is False:
    while True:
        data= {'name':name}
        try:
            r = requests.post(host, data)
            if (r.text == 'no config'):
                if os.path.isfile("config.txt") == True:
                    os.remove("config.txt")
                    endExperiment(threads)
                
                print("no config")

            else:
                configFile = open("config.txt", "w")
                configFile.write(r.text)
                configFile.close()
                print("config")
                return True
            time.sleep(5)
            
        except:
            print("can't connect")

    return False
    
if __name__ == "__main__":
    main()
