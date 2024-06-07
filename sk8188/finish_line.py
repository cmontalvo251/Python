#!/usr/bin/python3
from datetime import datetime
import os
import sys
#import keyboard  # using module keyboard

##GET CURRENT DATE
while True:
	rider_number = input('Rider number? = ')
	print('Rider = ',rider_number,' crossed at = ',datetime.now())