!!!FORTRAN CODE TO COMPUTE A KEPLERIAN ORBIT

PROGRAM kerbin_orbit
IMPLICIT NONE
real*8 Rkerbin,nu(100)
real*8 alt_AGL,rp,ra,axis,ecc,W,wp,inc,PI,zrf(100)
real*8 xpf(100),yqf(100),xif(100),yjf(100),zkf(100)
real*8 TPI(3,3),xyzi(3),xyz0(3),velf(100),p,r(100)
real*8 vxf(100),vyf(100),vel_circular
real*16 G,Mkerbin,muKerbin
integer i,openflag

PI = 3.141592654

write(*,*) 'Running Fortran Code' 

!##Kerbin Parameters
G = 6.6742*(10**(-11)) !#%%Gravitational constant
Mkerbin = 5.2915158*(10**22) !#
!Unfortunately this does not work so we have to compute it 
!A different way
muKerbin = 6.6742*5.2915158*(10**11)
Rkerbin = 600000. !#meters

!##True Anamoly
call linspace(nu,0.0D0,2.0D0*PI)

!##Semi Major Axis of an 80 km parking orbit
alt_AGL = 80000.
rp = Rkerbin + alt_AGL
ra = Rkerbin + 12000000.
axis = (ra+rp)/2.
!##Eccentricity
ecc = (ra - rp)/(ra+rp)
write(*,*) ecc
!##inclination
inc = 56.0*PI/180.0 !##Drew's random satellite he wants a just slightly over polar retrograde orbit
!###Longitude of the Ascending Node
W = 45*PI/180.0
!#Argument of the periaps
wp = 0.

!###Phat and Qhat
p = axis*(1-ecc**2)
r = p/(1+ecc*cos(nu))
xpf = r*cos(nu)
yqf = r*sin(nu)
zrf = 0*xpf

!###Rotate to Kerbin Centered Inertial Frame (KCI)
TPI(1,1) = cos(W)*cos(wp)-sin(W)*sin(wp)*cos(inc)
TPI(1,2) = -cos(W)*sin(wp)-sin(W)*cos(wp)*cos(inc)
TPI(1,3) = sin(W)*sin(inc)
TPI(2,1) = sin(W)*cos(wp)+cos(W)*sin(wp)*cos(inc)
TPI(2,2) = -sin(W)*sin(wp)+cos(W)*cos(wp)*cos(inc)
TPI(2,3) = -cos(W)*sin(inc)
TPI(3,1) = sin(wp)*sin(inc)
TPI(3,2) = cos(wp)*sin(inc)
TPI(3,3) = cos(inc)

xif = 0*xpf
yjf = 0*yqf
zkf = 0*zrf

do i=1,100
  xyz0(1) = xpf(i)
  xyz0(2) = yqf(i)
  xyz0(3) = zrf(i) 
  xyzi = matmul(TPI,xyz0)
  xif(i) = xyzi(1)
  yjf(i) = xyzi(2)
  zkf(i) = xyzi(3)
end do

!###Now let's Compute Velocity
vel_circular = sqrt(muKerbin/p)
write(*,*) 'muKerbin:',muKerbin
write(*,*) 'parameter:',p
write(*,*) 'Velocity Circuilar:',vel_circular
vxf = vel_circular*(-sin(nu))
vyf = vel_circular*(ecc+cos(nu))
velf = sqrt(vxf**2 + vyf**2)

!!Output contents to file
open(unit=93,file ='Output_File.txt',iostat=openflag)
!xpf = fortran_data[:,0]
!yqf = fortran_data[:,1]
!xif = fortran_data[:,2]
!yjf = fortran_data[:,3]
!zkf = fortran_data[:,4]
!vxf = fortran_data[:,5]
!vyf = fortran_data[:,6]
!velf = fortran_data[:,7]
do i = 1,100
  write(93,*) xpf(i),yqf(i),xif(i),yjf(i),zkf(i),vxf(i),vyf(i),velf(i),nu(i)
end do

close(93)

END PROGRAM kerbin_orbit

Subroutine linspace(array,start,end)
real*8 array(100),start,end,step
integer i

step = (end-start)/100

do i = 1,100
  array(i) = start + (i-1)*step
end do 

end Subroutine linspace