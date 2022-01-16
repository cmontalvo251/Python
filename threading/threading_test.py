#!/usr/bin/python3

import threading
import time
import keyboard

##GLOBALS
var0 = 0.0
kill = False

def method1():
    global var0,kill
    while kill == False:
        time.sleep(10)
        str1 = "Method1 = " + str(var0)
        print(str1)
    print('Thread 1 Killed')

def method2():
    global var0,kill
    while kill == False:
        time.sleep(0.1)
        str2 = "Method2 = " + str(var0)
        print(str2)
    print('Thread 2 Killed')

def method3():
    global var0,kill
    while kill == False:
        time.sleep(1.0)
        var0+=1
    print('Thread 3 killed')

print('Creating First Thread')
t1 = threading.Thread(target=method1)
t1.start()

print('Creating Second Thread')
t2 = threading.Thread(target=method2)
t2.start()

print('Creating Third Thread')
t3 = threading.Thread(target=method3)
t3.start()

print('Main Loop')
while kill==False:
    time.sleep(0.1)
    if keyboard.is_pressed('q'):
        print('YOU PRESSED Q!!!!!')
        kill=True

print('Killing threads')
while t1.is_alive():
    print('Waiting for t1 to quit',time.time())
    time.sleep(1.0)
t1.join()
while t2.is_alive():
    print('Waiting for t2 to quit',time.time())
    time.sleep(1.0)
t2.join()
while t3.is_alive():
    print('Waiting for t3 to quit',time.time())
    time.sleep(1.0)
t3.join()
print('All threads killed. Ending program')



