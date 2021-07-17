PROGRAM Parachute
IMPLICIT NONE

integer openflag
integer NOSTATE
real*8 n, i
real*8 z,t,dt
real*8 STATE(12),STATEDOT(12),NEWSTATE(12)

n = 50000
t = 0.0
dt = 0.01
STATE(1) = -500.0 !z
STATE(2) = -30.0  !zdot 
openflag = 0
NOSTATE = 2

open(unit=93,file ='ParachuteResults_FORTRAN.txt',iostat=openflag)

do i = 1,n

   write(93,*), t,STATE(1:NOSTATE),STATEDOT(1:NOSTATE)

   write(*,*) 'Simulation ', i/n*100,' % Complete'

   if (STATE(1) .gt. 0) then
      EXIT
   end if

   call Derivatives(STATEDOT, STATE)

   NEWSTATE = STATE + dt*STATEDOT
  
   STATE = NEWSTATE

   t = t + dt


end do

END PROGRAM Parachute

Subroutine Derivatives(statedot,state)
real*8 statedot(12),state(12)
real*8 z,zdot,zdbldot
integer,parameter :: m = 80 !mass of skydiver
real,parameter :: g = 9.81 !gravity     
real,parameter :: rho = 1.28 !density of air
real, parameter :: A = 0.7 !Cross-Sectional Area of parachute        	
real,parameter :: cd = 1.0 !Drag coefficient 

z = state(1)
zdot = state(2)
zdbldot = g - (0.5*rho*(zdot**2)*A*cd)/m

statedot(1) = zdot
statedot(2) = zdbldot

end Subroutine Derivatives
