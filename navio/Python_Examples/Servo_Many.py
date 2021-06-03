import sys
import time

import navio.pwm
import navio.util

navio.util.check_apm()

PWM_OUTPUT = [0,1]
SERVO_MIN = 1.250 #ms
SERVO_MAX = 1.750 #ms

pwm_channels = []

with navio.pwm.PWM(PWM_OUTPUT[0]) as pwm1:
    pwm1.set_period(50)
    pwm1.enable()

with navio.pwm.PWM(PWM_OUTPUT[1]) as pwm2:
    pwm2.set_period(50)
    pwm2.enable()
                        
while (True):
    pwm1.set_duty_cycle(SERVO_MIN)
    time.sleep(1)
    pwm1.set_duty_cycle(SERVO_MAX)
    time.sleep(1)
    pwm2.set_duty_cycle(SERVO_MIN)
    time.sleep(1)
    pwm2.set_duty_cycle(SERVO_MAX)
    time.sleep(1)

