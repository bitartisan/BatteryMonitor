#!/usr/bin/env python3

import sys
import notify2
from time import sleep
from pydub import AudioSegment
from pydub.playback import play

class BatteryMonitor:
    
    battery_path = str()
    sound_path   = str()
    capacity     = int()
    status       = str()
    
    def __init__(self, params):
        try:
            self.battery_path = params['battery_path']
            self.sound_path   = params['sound_path']
            
            metrics       = self.getBatteryMetric()
            self.capacity = metrics['capacity']
            self.status   = metrics['status'].strip()

            while self.capacity > int(10):
                if self.capacity <= int(15) and self.status == str('Discharging'):
                    self.playWarningSound()
                    self.showNotification()
                    
                metrics = self.getBatteryMetric()
                self.capacity = metrics['capacity']
                self.status   = metrics['status'].strip()

                sleep(120)
                
            self.playWarningSound()
            self.showNotification('Battery critically low, computer will be sent to hibernation.')
        except Exception as e:
            print(str(e))
            self.writeFile('Error: ' + str(e) + '\n')
            
    def getBatteryMetric(self):
        metric = {}
        metric['status']    = str(open(self.battery_path + "/status", "r").read())
        metric['capacity']  = int(open(self.battery_path + "/capacity", "r").read())

        return metric

    def playWarningSound(self, file_path=""):
        
        file = self.sound_path
        if file_path:
            file = file_path
            
        play(AudioSegment.from_wav(file))

    def showNotification(self, msg=""):
        
        if not msg:
            msg = "Low battery " + str(self.capacity) + "%, computer shutting down soon!"
            
        notify2.init('Battery Alert')
        notify2.Notification("Battery Alert", msg).show()
        
    def writeFile(self, msg=""):
        f = open("./log", "w")
        f.write(msg)
        
params = {
    'battery_path': '/sys/class/power_supply/BAT0',
    'sound_path'  : '/usr/share/sounds/linuxmint-logout.wav'
}

BatteryMonitor(params)