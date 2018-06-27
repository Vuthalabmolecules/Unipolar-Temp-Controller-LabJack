#From dual_unipolar_temp_controller by Shreyas for Arduino found in Google Drive under code/calcium_control/dual_uuniploar_temp_controller
#Translated to python for Labjack by Murali

from labjack import ljm
import time as time
from convert_helpers import *

handle = ljm.openS("T7", "USB", "ANY")

N_ACCUM = 100
ZEROV = 2.5 #Verify that this is actually the zeropoint 
GATE_VOLT_MIN = 1.5
GATE_VOLT_MAX = 2.7
enable = True
enable2 = True

logger_gate_voltage = ZEROV
params_set_temp = ZEROV


#Parameters
SET = set_temp(25.5) #PUT YOUR TEMP HERE!  
SET2 = set_temp(25.5) #PUT YOUR TEMP HERE!  

params_prop_gain = 2.5
params_pi_pole = 0.5
params_pd_pole = 1

params_prop_gain2 = 2.5
params_pi_pole2 = 0.5
params_pd_pole2 = 1

logger_accum = 0.0
accum_small = 0.0
prop_term = 0.0
error_signal_instant = 0.0
n_accum = 0
alpha_avg = 1.0/N_ACCUM
curr_time = time.time()
error_signal = 0.0
derivative_term = 0.0

while (True):
    prev_time = curr_time
    curr_time = time.time()
    dt = curr_time - prev_time

    error_signal_prev = error_signal_instant
    error_signal_instant = ljm.eReadName(handle, "AIN0") - SET
    error_signal = (error_signal_instant * alpha_avg) + (error_signal * (1.0 - alpha_avg))

    error_signal_prev2 = error_signal_instant2
    error_signal_instant2 = ljm.eReadName(handle, "AIN0") - SET
    error_signal2 = (error_signal_instant2 * alpha_avg) + (error_signal2 * (1.0 - alpha_avg))


    if (enable):
        accum_small += error_signal_instant * dt
        n_accum += 1
        if (n_accum > N_ACCUM):
            n_accum = 0
            logger_accum += accum_small*params_prop_gain*params_pi_pole
            accum_small = 0.0

        prop_term = 0.99*prop_term + 0.01*(error_signal_instant*params_prop_gain)
        der_term = (error_signal_instant - error_signal_prev)/dt/params_pd_pole
        derivative_term = 0.995*derivative_term + 0.005*(der_term*params_prop_gain)

        gv = logger_accum + prop_term

        if (gv > GATE_VOLT_MAX):
            gv = GATE_VOLT_MAX
            logger_accum = gv

        if (gv < GATE_VOLT_MIN):
            gv = GATE_VOLT_MIN
            logger_accum = gv
        logger_gate_volt = gv
    else:
        logger_gate_volt = GATE_VOLT_MIN
        logger_accum = 0.0
    
    ljm.eWriteName(handle, "DAC0", logger_gate_volt)



    if (enable2):
        accum_small2 += error_signal_instant * dt
        n_accum2 += 1
        if (n_accum2 > N_ACCUM):
            n_accum2 = 0
            logger_accum2 += accum_small2*params_prop_gain2*params_pi_pole2
            accum_small2 = 0.0

        prop_term = 0.99*prop_term2 + 0.01*(error_signal_instant2*params_prop_gain2)
        der_term2 = (error_signal_instant2 - error_signal_prev2)/dt/params_pd_pole2
        derivative_term2 = 0.995*derivative_term2 + 0.005*(der_term2*params_prop_gain2)

        gv = logger_accum2 + prop_term2

        if (gv > GATE_VOLT_MAX):
            gv = GATE_VOLT_MAX
            logger_accum2 = gv

        if (gv < GATE_VOLT_MIN):
            gv = GATE_VOLT_MIN
            logger_accum2 = gv
        logger_gate_volt2 = gv
    else:
        logger_gate_volt2 = GATE_VOLT_MIN
        logger_accum2 = 0.0
    
    ljm.eWriteName(handle, "DAC0", logger_gate_volt2)
    #print "OUT: %10.4f                 INSTANT_ERROR: %10.4f                TEMPERATURE: %10.4f" % (round(logger_gate_volt, 4), round(error_signal_instant, 4), round(get_temp(), 4))
