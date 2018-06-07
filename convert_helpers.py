#Temp reading code for baseplate temperature contoller for Nishant - relys on specific values.
#Author: Murali

from labjack import ljm
import numpy as np

handle = ljm.openS("T7", "USB", "ANY")

R1 = 9977 #Value of other resistor. May need to change if changing resistor.

a = 3.3570420e-3
b = 2.5214848e-4
c = 3.3743283e-6
d = -6.4957311e-8

def get_temp():
    """Returns temperature in Degrees Celsius"""
    #Calculates thermistor resistance
    vain0 = ljm.eReadName(handle, "AIN0") #Voltage divider voltage
    vain1 = ljm.eReadName(handle, "AIN1") #Total positive to negative voltage
    resistance = float(vain0/(vain1-vain0))*R1 #Thermistor resistance calculation
    #Code for thermistor temperature calculation. Constants above and below as well as equation from https://www.thorlabs.com/_sd.cfm?fileName=4813-S01.pdf&partNumber=TH10K
    logarith = np.log(resistance/10000.0) #Logarithm required
    T = 1.0/(a + b * logarith + c * (logarith ** 2) + d * (logarith ** 3)) #Temperature calulcation
    return (T - 273.15)

A = -1.6443767e1
B = 6.1080608e3
C = -4.4141671e5
D = 2.4159818e7

def set_temp(temp):
    """Returns voltage as a function of temperature in Degrees Celsius"""
    #Code for thermistor resistance calculation. Equation available: https://www.thorlabs.com/_sd.cfm?fileName=4813-S01.pdf&partNumber=TH10K
    tempC = temp + 273.15
    Rth = (10000.0)*np.exp(A + B/tempC + C/(tempC ** 2) + D/(tempC ** 3)) #Thermistor resistance
    #Voltage calculation
    V = ljm.eReadName(handle, "AIN1") * (Rth / (Rth+R1)) 
    return V
