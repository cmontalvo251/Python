#include <iostream>
#include <stdlib.h>
#include <boost/thread.hpp> 

using namespace std;
using namespace boost;

///Functions
void runloop1();
void runloop2();
void cross_sleep(double);

///Globals
double var1 = 10;
double var2 = 10;
double var0 = 10;
boost::mutex printmutex;

int main(int argc,char** argv) {

  printf("Kicking off loop1 \n");
  boost::thread loop1(runloop1);

  printf("Kicking off loop2 \n");
  boost::thread loop2(runloop2);

  //Infinite Main Loop
  while (1) {
    printmutex.lock();
    //printf("Main Loop var0 = %lf \n",var0);
    var0++;
    printmutex.unlock();
    cross_sleep(1);
  }
}

//Infinite loop 1
void runloop1() {
  while (1) {
    printmutex.lock();
    printf("This is loop 1 var0 = %lf \n",var0);
    printmutex.unlock();
    var1++;
    cross_sleep(10);
  }
}

//infinite loop 2
void runloop2() {
  while (1) {
    printmutex.lock();
    printf("This is loop 2 var0 = %lf \n",var0);
    printmutex.unlock();
    var2++;
    cross_sleep(0.1);
  }
}

void cross_sleep(double length) {
  #ifdef _WIN32
  Sleep(length*1000);
  #else
  usleep(length*1000000);
  #endif
}

