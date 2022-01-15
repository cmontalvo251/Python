#!/usr/bin/python


import threading
import time

def method1():
    ctr =0
    while 1:
        time.sleep(0.1)
        ctr+=1
        str1 = "Method1 = " + str(ctr)
        print str1

def method2():
    ctr =0
    while 1:
        time.sleep(0.1)
        ctr+=1
        str2 = "Method2 = " + str(ctr)
        print str2

def method3():
    ctr =0
    while 1:
        time.sleep(0.1)
        ctr+=1
        str3 = "Method3 = " + str(ctr)
        print str3

t1_stop = threading.Event()
t1 = threading.Thread(target=method1)
t1.start()

t2_stop = threading.Event()
t2 = threading.Thread(target=method2)
t2.start()

t3_stop = threading.Event()
t3 = threading.Thread(target=method3)
t3.start()


