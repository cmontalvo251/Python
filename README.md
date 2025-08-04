This repo contains alot of things in it like apps made in qt as well as some io and plotting utilities.

If you're in my controls or instrumentation class then there is a folder with all the codes I create in the classroom

I've also copied into here my Earth Sciences codes that I wrote back in 2016. Here's the readme of those....

Here we have code needed to process iMet sensor data and pitot probe
data using the FASTPitot sensor.

The data sets from April 20th, 2016 are from the Municipal Park.

iMet Sensor Data - 20160420-141621-00037232.csv
http://fastlabtutorials.blogspot.com/2016/03/imet-xq-quick-start-and-data-processing.html

Pitot Sensor Data - MUNICIPAL_PARK.TXT
http://fastlabtutorials.blogspot.com/2016/03/pitot-tube-wiring-diagram-and-data.html

This Pitot Sensor file only has 1 data stream and no GPS data. I am working on doing another flight test with GPS data and just 0's for the 3 other data streams so that you can at least develop the code for it. I'll let you know when that is done. My plan (assuming the baby doesn't come) is to finish the GPS code over the weekend and perform a flight test with all the sensors and final data format on Monday. Wishful thinking but it would be nice.

Iris+ Sensor Data - Iris_4_20.log
I don't have any documentation on this file but I can point you to a wiki which will hopefully help.
http://ardupilot.org/copter/docs/introduction.html

iMet Plots

-Pressure vs. Altitude
-Temperature vs. Altitude
-Humidity vs. Altitude

Pitot Sensor Plots

-Windspeed vs. Time for all 4 data streams
-Windspeed vs. Altitude for all 4 data streams

Iris+ Plots

-Altitude vs. Time
-Vx,Vy,Vz (m/s) vs. Time
-Roll,Pitch,Yaw (deg) vs. Time

Combinatory Plots for Check

-LAT vs. LON vs. Alt for all 3 data streams
-Altitude vs. Time for all 3 data streams


COMPLETED TASK
1.) Plot iMet soundings but split it into two soundings. You had two soundings so plot each sounding by itself and then compare each sounding. Plot apprentice data as well by splitting that. 
2.) Plot FAST pitot data from soundings  - use pitot.py
3.) Plot raw Anemometer data - use anemometer.py
5.) Combine iMet Soundings with FASTpitot soundings with Anemometer
data and send over to Systke - this is experiment 1 for UAV sampling
of winds - use ploteverything.py and then test with wrapper.py - gonna
need to edit code to plot double iMet data using ploteverything.py -
not sure how I will do that but we'll figure it out 
4.) Plot Quad data from soundings

TASK TO COMPLETE

Data Streams for MAAWM

1.) Create a module in MAAWM that handles all of this kind of data
1.5) plot quad data from MAAWM flight
2.) Add iMet streams to MAAWM module keeping in mind that one was on the aircraft - probably just need to make a vehicle module with a list of sensors and their respective files. Yea that will work. 
3.) Add FASTpitot data to MAAWM module and make sure you can read it in just fine
4.) Add anemometer data to MAAWM module
5.) Add FASTMeta - you'll have to create a new module for this so I suggest creating this module inside of MMACS to plot all of this data and go ahead and compare it to brandon's plots because something wierd is going on.
6.) Now combine all data streams and plot the following.
-LAT vs time
-LON vs time
-LAT/LON for all things
-ALT vs TIME for all things
-LAT/LON/ALT
-LAT/LON/EAST-WEST Wind - Note that FASTpitot only got North
-LAT/LON/NORTH-SOUTH wind - Note that Apprentice will need to use GPS heading and combine with magnetometer and substract GPS speed
-LAT/LON/TOTAL - for now this will only have anemometer, once we have the 4Pitot on two quads we can add that. Not sure what to do about apprentice. We won't get total wind unless we mount a 3pitot sensor on the aircraft.

DESCRIPTION OF FLIGHT TEST EXPERIMENT

FASTpitot sensor on Quad pointing north - Located in
GeoSampling/FASTPitot b/c that's where FASTpitot data goes - There
were two files GPSLOG10.TXT is the soundings and GPSLOG11.TXT was the
MAAWM flight test

iMet on Quad - Located in GeoSampling/iMet b/c that's where iMet data goes
iMet on Apprentice - Located in GeoSampling/iMet b/c that's where iMet data goes
Anemometer Data which just sat on the ground the whole data - Located in GeoSampling/Anemometer b/c that's where Anemometer data goes
Ground Station Data - Sat on the ground and grabbed control inputs - located in FASTPilot/fastwing/Flight_Tests b/c this data is from the fast meta sensor 
FASTMeta Data - Was in the apprentice and grabbed 6DOF and pitot data - located in FASTPilot/fastwing/Flight_Tests b/c this data was from the fast sensor

In order to download mesonet tower data you must visit this site
http://chiliweb.southalabama.edu/archived_data.php

Typically I've been downloading

Year 
Month
Day of Month
Hour 
Minute
Lat
Lon
Elevation
Wind Dir 2m
Wind Dir 10m
Wind Speed 2m
Wind Speed 10m

To Do List

See LateX for outline of paper

1. Learn and be more proficient in FORTRAN and Python as well 
3. Create CAD drawing of the case for the project 
6.) Perform a flight test solely by yourself (except for PIC) where you operate the sensors take the data and process the data. This is extremely important for you to move forward.
14.) Make Lisa write a tutorial on post processing code.

July 29th, 2016

Tasks completed

2. Create Fritzing diagram for new assembled project 
Using Arduino UNO and GPS Shield

July 20th, 2016

8.) Try digital pitot probe - Done
9.) Try 4 pitot sensors with a GPS shield - you can just use a bread board to test this.

The above steps worked so there is no need to get a breakout board or a MEGA.
10.) If that doesn't work go buy an SD breakout and GPS breakout. If you do that you'll probably need to go get a MEGA though.
11.) Go buy a MEGA if need be.

July 14th, 2016

FrSky pitot probe needs a receiver to parse proprietary data. Unless we want to buy a $30 receiver I suggest we move on to digital pitot probes. Good news is that hobby king is back in stock so Virginia got the go ahead to buy 4. I just purchased 2 more for the meta aircraft project.

http://www.getfpv.com/frsky-x6r-16ch-receiver-sbus-smart-port.html?utm_source=google_shopping&m=simple&gdffi=747627bc7e464db68e5f529d971aacf3&gdfms=EBCA004CF25B439390407C619ECDDD88&gclid=CjwKEAjw8Jy8BRCE0pOC9qzRhkMSJABC1pvJ-D11VNkM6fFeAWlcDUcWaUZid6t7VAvmaRJ3-hTaLRoCgOPw_wcB

July 1st , 2016

Purchase a FrSky pitot sensor. Just waiting for it to be delivered. 

June 30th, 2016

Successful flight test completed. Added some line items above. 3,4,5,6 and 12 and 13

June 27th, 2016

So unfortunate news. The pitot probes are no where to be found now. They are either out of stock or from a sketchy seller. Nemo found one from FrySky but unfortunately we're not sure if that uses some sort of proprietary format.

June 12th, 2016

Finished testing 1 pitot sensor. Need to now purchase all 4 pitot sensors. Note that Drew could not get the GPS shield to work on the MEGA so I may just want to get an UNO. Then again number 9 says test everything with bread boards so we have time.

Monday May 30th, 2016

-Sent MOU to Bill and Sytske so we're all set there.
-Nemo is actively working on getting up to speed with all of the different sensors. iMet pitot quad. He has made a circuit diagram (attached)

Wednesday May 25th, 2016

-Just got the MOU in the mail. Need to send to Sytske and upload to Drive
-Nghia just made a fritzing diagram. Need to get him on board with pitot sensor and do pinned assignments above.

Monday May 16th, 2016

-Working on sending Wesley stuff (FINISHED!!!!)
-Approved the MOU online. Waiting for legal to take care of it.

Wednesday May 11th, 2016

-Just submitted the online form for the MOU.
-Got the AMA document

Tuesday May 10th, 2016

-Need to fill out online form for MOU
-Once done you need to send AMA insurance document and FAA document
-Need to get AMA insurance document
-Toss all iMet, Pitot and Iris+ files into drive but make sure to get pitot probe wired up with GPS
-Send Wesley link to blog about Qt designer 
-Next flight test take video and make a youtube video.

Tuesday May 3rd, 2016

Need to call Bill Melton to check on status. Need to find his phone number from avasystem

April 27th, 2016

Still no word from Bill Melton. Will probably call him on Friday
Insurance Document apparently is from AMA so I'll need to get that insurance document somehow and forward to Bill as well as the FAA document.

April 25th, 2016

Make a few phone calls
Now Calling Jonny Harper
Didn't pick up

Calling Bill Melton Currently
Approving MOU this morning in an hour and will sign the document this week and send it back asap
Insurance Document - Can we get this? - Ask kristin and send her MOU
FAA Document - Send that back

April 20th, 2016

1.) Need to as Jake about NOTAM.
2.) Successful flight test. 
2.8) Just need to make a few phone calls

April 19th, 2016

1.) I read the FAA document - need to ask Jake about NOTAM. Apparently we can fly whereever we want provided it is within 5 NM of a controlled airport or 2NM from an uncontrolled airport.
2.) Shooting for Wednesday afternoon
2.5) Compiled the document into 1.75. That's pretty good going from 7 pages.
2.8) MOU is in process. Need to make a few phone calls.
Don't do 3 or 4. Sytske found it. I just emailed Jake so 2.8 is done.

April 12th, 2016

1.) Read FAA Document
2.) Try and fly either at the school or the municipal park maybe tuesday based on weather (Fly up to 100 m)
Can potentially fly here 
https://www.google.com/maps/place/Dawes+Intermediate+School/@30.6168121,-88.2908962,17z/data=!3m1!4b1!4m2!3m1!1s0x889bb0d72fc8311f:0xd3814c3e9866a2d8
Or maybe just Municipal park when you have time one day and you do it quickly.
2.5) Compile the document into 1.5 page rather than 7 pages put in the new data from the launch
2.8) Email jake about getting the MOU
3.) Look for N-Number Registration of Systke
4.) Monday - Call FAA and ask for update via serial number and Name on form (Look in Drive for N-Number Documents)

March 22nd, 2016

Pre-Spring Break Meeting

0.) Repeat experiment in windtunnel
1.5) Wiring diagram
1.) AA Battery power
2.) Button
3.) Extension for Pitot probe
4.) Carbon fiber rod in DBF lab
5.) Cardboard box for quad - paint it black
5.5) Make sure iMet still works
6.) Perform experiment
7.) Write up results

February 2nd, 2016

Drone Committee Meeting
-Flying around tower using quad

January 26th, 2016

1.) Calibrate Sensor 
2.) Make sure code is correct and is writing arduino
3.) Wrap foam around it and put on quad for full flight test
4.) Write up of results and description of sensor build procedure

Meeting with Lynne

Questions for Sytske
-NSF iCORPS - Perhaps intend to work on this
-Lean Launch
-Transfer to Practice

January 19th, 2016

Ok so I uploaded the N-number documents for my aircraft and updated the flight operations map.

Still need to get Sytske to fill out her stuff.

--------------------------------------------

Once you get the N-number paperwork fill everything out and then submit it to the address found in COA_USA/N-number_registration (Drive). You need to attach two documents. The first is the 8050-1 form and the second is the bill of sale form that needs to be notarized.

At the same time you need to upload the N-number registration forms into the Other category in the Systems Description

Then update the flight operations map and RECOMMIT the document.

-------------------------------------------

Dec 13th, 2015

COA has been submitted. I sent a letter to Thea Dickerman about the request for getting N numbers

1.) Flight Operations Map - Take a look at team Eagle
2.) Airworthiness - We are going to make sure it's safe to fly by following the correct guidelines from 3DR and other things - Need to get VPR to approve of this - I think this is Lynne Chronnister - Just say you'll follow 3DRobotics checklist  - Need to send to them and have Lynne sign it.
3.) Visual observer - 100 feet away - just use voice communication - Lost communication - there will be no lost communication which is fine but you need to have that in there. Not using any comm tours since all airports close by are uncontrolled. Observers are within voice range so there is no need for lost comms procedure. 
4.) Generate attachment with no TSO components.
5.) For PIC match the images that you sent and then make sure observers are trained on part 91. Make sure to match Dave's paper
6.) VPR from UAH said no!
7.) Email Mark Jordan once you get AG letter.


Maybe get people to save data using the NMEA protocol
Pic
http://www.microchip.com/wwwproducts/Devices.aspx?product=PIC12F1571
NMEA Library
http://nmea.sourceforge.net/
Wikipedia Article
https://en.wikipedia.org/wiki/NMEA_0183
NMEA 0183 Wiring
https://www.google.com/webhp?sourceid=chrome-instant&ion=1&espv=2&ie=UTF-8#q=NMEA+0183+wiring

MicroSD Card 16 GB - $12
http://www.newegg.com/Product/Product.aspx?Item=9SIA4P02C05481&cm_re=micro_SD-_-9SIA4P02C05481-_-Product
Ineesi 8GB
http://www.newegg.com/Product/Product.aspx?Item=9SIA9173AY2756&cm_re=micro_SD-_-9SIA9173AY2756-_-Product


Lowrance Mark-4
http://www.lowrance.com/en-US/Products/Fishfinder-Chartplotter/Mark4-en-us.aspx
Lowrance Mark-4 PDF
http://www.lowrance.com/Root/Lowrance-Documents/US/MARK-ELITE_SONAR-COMBO_OM_EN_988-10161-001_w.pdf

For flight planning I would recommend purchasing this quad to help people learn. Maybe Christmas?

http://www.horizonhobby.com/products/nano-qx-bnf-with-safe-technology-BLH7680

Email Zeke and cc Kristin
Make sure to get the Attorney General letter - 2.5 months ago


===================SST SENSOR TALK WITH COAST GUARD==============

Using NOAA Sensor Buoy - 42012 is off the coast of Dauphin Island
Supposedly the Side Skin Sonar Hummingbird sensor works like the SST
An idea for the SST structure is to just tie a rope to the side of the boat
Another idea is to just have a float in the water like a boogie board
Shrimping boats go at 5 knots (3 knots is 200 ft resolution)
Another idea is to have the rig be spring loaded so that when you travel full speed it just bounces and then when you travel slow you can take good data

====================Phone Call with Dave - 10/27/2015======================

Start filling out data
use spreadsheet as template
description of vehicles
attachments for vehicles
prepare documents
picture of vehicle
basic information about controller
lat lons for site
Send Dave filled out spreadsheet
Send Attachments
Dave has to upload those to FAA site - he will submit the COA
Dave will print out all documents
Submit something about airworthiness over vehicle - VP research may not want to take responsibility of aircraft
Needs to be some letter in there that says we will do airworthiness - We will take a look at this

====================================================================

Supplies for build
Tape Measure - In launch room
Hacksaw - in DBF room
Drill - in Launch room 
Hammer - Launch
Respirator
Gloves
Wrench set - In lab
Bring extra things from office to size some things
Get some foam for press fit
Find a way to insert a 1.5+3/16 = 1.6875" the pipe we have now is ID 1.593" and OD 1.9"

Need to respond to last email but more Importantly I need to build SST Sensor.

Items to address
-Ask her about attending CubeSat meeting at 1pm on Monday SH room 3????
-Get quad copter and wind sensor from Dave
-Get quad copter from EAS
-Missing Screws
-Get COA submitted with Dave Arterburn
-SST sensor - need to get the equipment - need to build it as well
-Legal Meeting from below

Conversation with Legal/Police/Risk Management - 10/5/2015
Kristin,Zeke,Bill
-Ask Jake about ATC at regional airport - Zeke and Bill
-AMA license required but licensed pilot only below 200 ft
-Buddy system test for training
-Email all documents from any COAs to Police Dept

Conversation with NOAA - 9/29/2015 - John Walker
-NGI - can we help? - collaboration? - NGI = North Gulf Institute, Perhaps get a phone call with them
-Cost share with NOAA??
-NSF interested in collaboration
-Look ahead for a group call
-Working with Dave Arterburn to submit COA - Emailed him this morning about two sites
-Oklahoma State University - Tornadic Activity
-UAH - Dave - Kevin Knaupp
-Weather Service Operations and Universities
-Looking at weather in own backyard
-No real competition
-Jacksonville, FL - Sea Breeze research as well
-Should be alot of collaboration in the future

---------Email to all Faculty Members-------------

-Nathan Murray from University of Mississippi suggested I contact Ratan Jha - Director of Raspet Flight Research Lab since Miss State was just awarded a Center of Excellence in UAVs from the FAA
-Calvin Walker was then contacted on behalf of Rtan Jha and said he can call me
-Dave Arterburn from UAH contacted me and offered sponsorship

---------Email with Dave Arterburn----------------

Bio: Director of Rotorcraft Systems Engineering and Simulation Center

-Offered to sponsor us
-Currently en route to Paris until June 22nd - will contact me next Monday
-Asked if there was funding to support our involvement

---------Phone Call with Mike Mendez (845-551-7701)-------------

Bio: AREAI Flight Test Expert - Written numerous COAs for FAA

Notes:

-Need a COA for each boundary defined. Only 1 aircraft allowed per boundary
-Need N-numbers for each aircraft and must be registered with FAA. Could get aircraft leased (see Hobby Town / Bill Hutto)
-COA itself usually takes 2-3 months (it could 1-2 months just for paperwork) for approval unless they have questions
-Because of our first time it is usually a good idea to get sponsorship (see UAH and Bill Hutto)

-----------Phone Call with Hobbytown----------------

Bio: Rob - 100+ hrs of flight time. Flys at Irvington, AL airfield

-Fly at Irvington, AL with no license unless vehicle is autonomous
-Might be able to lease vehicles from Hobbytown - This way we can get aircraft registered with FAA without actually purchasing the aircraft. He said we will figure something out.
-Jim Pinion offers a UAV safety class however he wants to take class with Auburn (see Bill Hutto/Auburn)

------------------Jim Pinion (251-583-9933)----------------------

Bio: Home Inspector - Uses Quadcopters to take photos of roof

-Teaches a quadcopter school
-Auburn is first school to be approved by FAA
-Apparently Rodney from Alabama is the admin contact
-Typically FAA rules state that 500 ft is max altitude no matter what

Turns out Rodney ?? is actually 

Rodney Robertson, Executive Director of the AU Huntsville Office

Joe Hanna was cced in addition to Rodney and he emailed me back. 

-------------------Joe Hanna------------------

Bio: Regions Bank Professor and Associate Dean

-Auburn's Harbert College of  Business offers two different aviation degree programs
-The Director of the Auburn Aviation Center is Dr. Bill Hutto - "he was instrumental in Auburn's ability to obtain a FAA COA for UAVs"

--------------------Bill Hutto --------------------

Bio: Airport and Aviation Center Directoy

-Typically Public COAs (PCOA) are limited to research on aircraft platform itself rather than obtaining data - If this is true how do other institutions do it?
-FAA released a memo stating the difference between applied research and pure research
-Auburn applied for a 333 commercial exemption to perform research and offer classes
-Suggested I contact Mark Jordan from FAA

------------------Calvin Walker (662-325-9614)------------------

Bio: Senior Flight Test Engineer Mississippi State

-Application for COA is easy but leading up to it is tough
-Operator must be a licensed pilot with a class 2 medical license from the FAA
-Observer needs a class 2 medical license and they have to have taken the written class
-Need 1 pilot per aircraft so we would need 3 pilots every single time we fly
-I thought about being a pilot but you need 40 hrs of full scale flight time ($200 /hr = ~$8000)
-What we do need is a letter from the Attorney General stating that we are part of the state of alabama and a public entity. Probably need to get Bill Guess and Lynne Chronister involved in this one.
-Sometimes a 333 exemption is good for the university but you can only fly up to 200 ft but at least you don't need licensed pilot everytime
-Need to get in contact with Mark Jordan from FAA to get website access to fill out registration form
https://ioeaaa.faa.gov/oeaaa/Welcome.jsp
