Here are my notes on getting bluetooth to work

First I downloaded Android Studio on my computer
(I'm using this tutorial)
https://developer.android.com/training/basics/firstapp/creating-project

The first time this booted up took forever

On the Raspberry Pi side (testing on computer first)
I downloaded pybluez by running these two commands

$ sudo apt install bluetooth libbluetooth-dev

$ pip3 install pybluez

Make sure you install that libbluetooth-dev or it will throw an error

I'm using this tutorial for Python Bluetooth
https://geektechstuff.com/2020/06/01/python-and-bluetooth-part-1-scanning-for-devices-and-services-python/

I ran the scan.py script in this folder and sometimes I found one device and other times I wouldn't find any

Device:
Device Name: moto g play (2021)
Device MAC Address: C0:6B:55:71:52:7A
Device Class: 5898764

Creating a virtual object didn't work real well
cannot add library /home/carlos/Android/Sdk/emulator/qemu/linux-x86_64/lib64/vulkan/libvulkan.so: failed 
2022-05-18 22:58:43,145 [ 402644]  ERROR -       Emulator: Pixel 2 API 30 - Failed to create Vulkan instance.

But a physical object via wireless worked but not with a hard line.





