##So there's this routine in MATLAB called K = place(A,B,poles) which basically solves for gains in a
##matrix K = [K1,....KN] to put the closed loop system at poles. I can demonstrate this in the following way
import numpy as np
import control as ctl
import matplotlib.pyplot as plt
import scipy.integrate as sint
import scipy.signal as sci
import sympy as sp
import sys

class makeSystem():
    def __init__(self,A,B,C=1,D=0,systype='SS'):
        if systype == 'SS':
            #State space matrices given
            ##Let's make a state space system
            self.sysSS = ctl.StateSpace(A,B,C,D)
            print('State Space = ',self.sysSS)

            #Let's convert the system to a transfer function
            self.sysTF = ctl.ss2tf(self.sysSS)
            print('TF = ',self.sysTF)
        elif systype == 'TF':
            self.num = A
            self.den = B
            self.sysTF = ctl.tf(self.num,self.den)
            print('TF = ',self.sysTF)
            self.sysSS = ctl.tf2ss(self.sysTF)
            print('State Space = ',self.sysSS)

        self.A = np.asarray(self.sysSS.A)
        self.B = np.asarray(self.sysSS.B)
        self.C = np.asarray(self.sysSS.C)
        self.D = np.asarray(self.sysSS.D)
        self.statespace = True

        if self.C[0][0] == 0:
            self.inverse = True
            print("INVERSION DETECTED IN STATE SPACE")
        else:
            self.inverse = False

        #Compute plant poles and zeros
        self.plant_poles = ctl.pole(self.sysTF)
        self.plant_zeros = ctl.zero(self.sysTF)
        print('ZPK = ',self.plant_zeros,self.plant_poles,1.0)
        [self.num,self.den] = sci.zpk2tf(self.plant_zeros,self.plant_poles,1.0)

        ##Let's compute the eigenvalues
        [self.sOL,self.vOL] = np.linalg.eig(self.A)
        print('Eigenvalues = ',self.sOL)
        self.gram()    

    def gram(self):
        ##Let's also compute the controllability gramian to see if we're controllable
        #Wc = ctl.gram(sysSS,'c') #<-So the funny thing about this routine is it will only compute it if the system is stable
        #So in this case we will have to write our own. First let's figure out what size our system is
        [self.N,self.N] = np.shape(self.A)
        self.Wc = np.zeros([self.N,self.N])
        for n in range(0,self.N):
            if n > 0:
                temp = self.A
                for i in range(0,n-1):
                    temp = np.matmul(temp,self.A)
                self.Wc[:,n] = np.matmul(temp,self.B)[:,0]
            else:
                self.Wc[:,n] = self.B[:,0]
        #Now we need to determine if the system if full rank
        self.rank = np.linalg.matrix_rank(self.Wc)
        a = self.check_controllability()

    def check_controllability(self):
        print('System is a ',self.N,' x ',self.N)
        print('Controllability Gramian = ',self.Wc)
        print('Rank of Wc Matrix = ',self.rank)
        if self.rank == self.N:
            print('Full Rank. System is controllable')
            return 1
        else:
            print('System is not fully controllable')
            return 0 

    def place(self,desired_closedloop_poles):
        #First things first. Check for rank of matrix
        if self.check_controllability():
            self.desired_closedloop_poles = desired_closedloop_poles
            print('Desired Closed Loop Poles = ',self.desired_closedloop_poles)
            
            ###########This is the easy way############
            #Basically this use a bunch of built in python functions
            #Ok so basically what we want to do is construct a closed loop transfer function with zpk
            #[self.NGCL,self.DGCL] = sci.zpk2tf([],self.desired_closedloop_poles,1.0) #Controller is default no poles and unity gain
            #self.desired_GCL = ctl.tf(self.NGCL,self.DGCL)
            #print('Desired Transfer Function = ',self.desired_GCL)
            #print('Desired Denominator Coefficients = ',self.DGCL)
            #print('Truncated Coefficients = ',self.DGCL[1::])
            #print('Current Cofficients = ',self.den[1::])
            #GCL = C*G / (1 + k*C*G)
            #We know the denominator is going to be 
            # self.den + [k1,...kn]*[self.num]
            #Assuming that B = [0,....1]
            #K is just the difference between the two matrices
            #Kvals = self.DGCL[1::] - self.den[1::]

            #Let's do the hardway which is also more robust
            #This still uses some built in python functions 
            #but they are more low weight symbolic manipulation
            #Ok first let's see if we can reconstruct the RHS
            #det(sI-A+B*K) = prod(si-(oi+wi j))
            #Unfortunately this only works if the system is quadratic. 
            #Otherwise we have to use the built in routine :(
            if len(desired_closedloop_poles) == 2:
                RHS = 1.0
                self.s = sp.Symbol('s')
                K = []
                for i in range(0,self.N):
                    RHS *= (self.s-self.desired_closedloop_poles[i])
                    K.append(sp.Symbol('k'+str(i+1)))
                RHS = sp.simplify(RHS)
                print('RHS = ',RHS)
                RHS = sp.Poly(RHS,self.s)
                desired_coefficients = RHS.coeffs()
                print('Desired Coefficients = ',desired_coefficients)
                #Alright now we need to get the LHS
                #First we need K
                K = np.asarray(K)
                K = K.reshape((1,self.N))
                BK = np.dot(self.B,K)
                ACL = self.A - BK
                sI = self.s*np.eye(self.N)
                sIA = sI - ACL
                sIA = sp.Matrix(sIA)
                self.LHS = sp.simplify(sIA.det())

                print('K = ',K)
                print('A = ',self.A)
                print('B = ',self.B)
                print('BK = ',BK)
                print('ACL = ',ACL)
                print('sI = ',sI)
                print('sIA = ',sIA)
                print('Determinant = ',self.LHS)

                #Now we need to extract the coefficients from the LHS
                self.LHS = sp.Poly(self.LHS,self.s)
                current_coefficients = self.LHS.coeffs()
                print('Current Coefficients = ',current_coefficients)

                ##Alright now we need to solve a system of equations
                self.expressions = []
                length = 0
                for i in range(0,self.N+1):
                    self.expressions.append(current_coefficients[i]-desired_coefficients[i])
                    if self.expressions[-1] == 0:
                        self.expressions.pop()
                print('Expressions Needed to be solved = ',self.expressions)
                sol = sp.solve(self.expressions)
                print('Solution = ',sol)
                #We have the solution now we need to go and populate the K matrix
                Kvals = []
                for i in range(0,self.N):
                    key = K[0][i]
                    #print(key)
                    #print(sol[key])
                    Kvals.append(np.float(sol[key]))
                Kvals = np.asarray(Kvals)
            else:
                #I haven't figured this out for larger than 2nd order systems
                Kvals = ctl.place(self.A,self.B,desired_closedloop_poles)[0]
            print('Kvals = ',Kvals)
            self.K = Kvals

            #In order to get a transfer function we need to make a controller C
            #but to do that we need the controller zeros
            self.KSTAR = Kvals[-1]*self.C[0][0]
            #It's possible the state space matrices are inverted
            if self.inverse:
                self.KSTAR = Kvals[0]*self.C[0][-1]
                controller_zeros = np.roots(Kvals) 
            else:
                controller_zeros = np.roots(Kvals[-1::-1]) 

            self.controllerTF(controller_zeros)
            self.GCL = self.closed_loop(self.KSTAR,verbose=True)
            self.closedloopStateSpace()
            
            return 1
        else:
            print('Place is not possible. System uncontrollable')
            return 0

    def integrateClosedLoop(self,tstart,tend,num=1000,ic = [],input='step'):
        print('Integrating closed loop from ',tstart,' to ',tend)
        tout = np.linspace(tstart,tend,num)
        
        ##Let's now simulate the system open loop with a step input and zero initial conditions
        xinitial = np.zeros(self.N)
        xcommand = np.zeros(self.N)

        #Compute the input
        if input == 'step':
            if self.inverse:
                xcommand[-1] = -1.0
                xinitial[0] = -self.KSTAR
            else:
                xcommand[0] = 1.0 
                xinitial[-1] = self.KSTAR

        if len(ic) > 0:
            xinitial = ic

        print('Initial Conditions = ',xinitial)
        print('Input Type = ',input)

        #Numerical Integration
        if input != 'impulse' and self.statespace:
            self.BKxc = np.matmul(self.BK,xcommand)
            self.xoutSS = sint.odeint(DerivativesClosedLoop,xinitial,tout,args=(self.ACL,self.BKxc))
            #self.xoutNOICs = sint.odeint(DerivativesClosedLoop,0*xinitial,tout,args=(self.ACL,self.BKxc))
            self.ySS = self.Cx(self.xoutSS)
            #self.yNOICs = self.Cx(self.xoutNOICs)

        ##We can also simulate the system using the transfer function
        if input == 'step':
            tout,self.xoutTF = ctl.step_response(self.GCL,tout)
        elif input == 'impulse':
            tout,self.xoutTF = ctl.impulse_response(self.GCL,tout)

        #Let's plot it
        self.plot = 0
        plt.figure()
        if input != 'impulse' and self.statespace:
            self.plot = 1
            plt.plot(tout,self.ySS,'b-',label='State Space')
            #plt.plot(tout,self.yNOICs,'g-',label='State Space (x0=0)')
        if input != 'none' and np.sum(ic) == 0:
            self.plot = 1
            plt.plot(tout,self.xoutTF,'r-',label='Transfer Function')
        plt.xlabel('Time (sec)')
        plt.ylabel('X1')
        plt.grid()
        plt.legend()

        if input != 'impulse' and self.statespace:
            self.plot = 1
            for i in range(0,self.N):
                plt.figure()
                plt.plot(tout,self.xoutSS[:,i])
                plt.xlabel('Time (sec)')
                plt.ylabel('State = '+str(i))
                plt.grid()
        if self.plot:
            plt.show()
        else:
            print('No plots to show. Remember state space cannot simulate an impulse')
            print('and transfer functions must have zero initial conditions')
            print('Furthermore if you tuned the controller with rltools() your state')
            print('system must be the same order as your transfer function')

    def Cx(self,xout):
        [r,c] = np.shape(xout)
        y = np.zeros((r,1))
        for i in range(0,r):
            y[i] = np.matmul(self.C,xout[i,:])
        return y

    def integrateOpenLoop(self,tstart,tend,ic=[],num=1000,input='step'):
        print('Integrating from ',tstart,' to ',tend)
        tout = np.linspace(tstart,tend,num)
        ##Let's now simulate the system open loop with a step input and zero initial conditions
        if len(ic) == 0 or np.sum(ic) == 0:
            xinitial = np.zeros(self.N)
            ##We can simulate the system using the transfer function
            #Since the initial conditions are zero
            if input == 'impulse':
                tout,self.xoutTF = ctl.impulse_response(self.sysTF,tout)
            elif input == 'step':
                tout,self.xoutTF = ctl.step_response(self.sysTF,tout)
        else:
            xinitial = ic
        print('Initial Conditions = ',xinitial)
        print('Input Type = ',input)

        #Numerical Integration
        ssint = False
        if input == 'step':
            self.xout = sint.odeint(DerivativesOpenLoopStep,xinitial,tout,args=(self.A,self.B))
            ssint = True
        elif input == 'none':
            self.xout = sint.odeint(DerivativesOpenLoop,xinitial,tout,args=(self.A,self.B))
            ssint = True

        #Let's plot it
        plt.figure()
        if ssint == True:
            self.y = self.Cx(self.xout)
            plt.plot(tout,self.y,'b-',label='State Space')
        if len(ic) == 0 and input != 'none':
            plt.plot(tout,self.xoutTF,'r-',label='Transfer Function')
        plt.xlabel('Time (sec)')
        plt.ylabel('X1')
        plt.grid()
        plt.legend()
        plt.show()

    #Closed Loop TF function
    def closed_loop(self,k,verbose=False):
        if 'self.sysC' in locals():
            print('Cannot compute closed loop. Need controller first')
            sys.exit()
        else:
            GCL = ctl.minreal(k*self.sysC*self.sysTF/(1+k*self.sysC*self.sysTF),verbose=False)
            if verbose:
                print('Closed Loop Transfer Function = ')
                print(GCL)
                self.closedloop_poles = ctl.pole(GCL)
                print('Closed Loop Poles (TF) = ',self.closedloop_poles)
                self.closedloop_zeros = ctl.zero(GCL)
            return GCL

    def controllerTF(self,controller_zeros,controller_poles=[]):
        print('Computing Compensator...')
        #Create the Controller Transfer Function
        self.controller_zeros = controller_zeros
        self.controller_poles = controller_poles
        [self.NC,self.DC] = sci.zpk2tf(self.controller_zeros,controller_poles,1.0) 
        self.sysC = ctl.tf(self.NC,self.DC)
        print('C_tf=',self.sysC)

    def closedloopStateSpace(self):
        if len(self.DC) == 1:
            if len(self.NC) != self.N:
                print('Cannot create a closed loop system in state space')
                print('Controller has extra poles requiring a larger state space system')
                print('Recommend including controller dynamics into transfer function')
                print('and converting to state space')
                self.statespace = False
            else:
                self.K = np.zeros((1,self.N))
                #It's possible the state space matrices are inverted
                if self.inverse:
                    #So we need to flip the NC matrix around
                    self.K[0] = self.KSTAR*self.NC*self.C[0][-1]
                else:
                    self.K[0] = self.KSTAR*self.NC[-1::-1]*self.C[0][0]

                self.BK = np.matmul(self.B,self.K)
                self.ACL = self.A-self.BK
                [self.sCL,self.vCL] = np.linalg.eig(self.ACL)
                print('Closed Loop Full State Feedback Matrix = ',self.K)
                print('Closed Loop State Transition Matrix = ',self.ACL)
                print('Closed Loop Poles (SS) = ',self.sCL)
        else:
            print('Cannot create a closed loop system in state space')
            print('Controller has extra poles requiring a larger state space system')
            print('Recommend including controller dynamics into transfer function')
            print('and converting to state space')
            self.statespace = False

    def rltools(self,KMAX,KSTEP,KSTAR,controller_zeros,controller_poles=[]):
        #Save the KSTAR value
        self.KSTAR = KSTAR

        #Create Controller
        self.controllerTF(controller_zeros,controller_poles)

        ##PLOT POLES AND ZEROS OF PLANT AND CONTROLLER
        plt.figure()
        plt.plot(np.real(self.plant_zeros),np.imag(self.plant_zeros),'go',label='Plant Open Loop Zeros',markersize=10)
        plt.plot(np.real(self.plant_poles),np.imag(self.plant_poles),'gx',label='Plant Open Loop Poles',markersize=15)
        plt.plot(np.real(controller_zeros),np.imag(controller_zeros),'ro',label='Controller Zeros',markersize=10)
        plt.plot(np.real(controller_poles),np.imag(controller_poles),'rx',label='Controller Poles',markersize=10)
        ##Determine Range on plots
        self.xmins = []
        self.ymins = []
        self.xmaxs = []
        self.ymaxs = []
        self.addmin(self.plant_poles)
        self.addmin(self.plant_zeros)
        self.addmin(controller_zeros)
        self.addmin(controller_poles)
        self.addmax(self.plant_poles)
        self.addmax(self.plant_zeros)
        self.addmax(controller_zeros)
        self.addmax(controller_poles)
        self.xmin = np.min(self.xmins)
        self.xmax = np.max(self.xmaxs)
        self.ymin = np.min(self.ymins)
        self.ymax = np.max(self.ymaxs)
        ###LOOP ON K TO MAKE LOCUS
        print('Calculating Root Locus...')
        k_vec = np.arange(KSTEP,KMAX,KSTEP)
        #p_vec = []
        #z_vec = []
        for k in k_vec:
            #Compute closed loop TF
            GCL = self.closed_loop(k)
            poles = ctl.pole(GCL)
            zeros = ctl.zero(GCL)
            #Check range on plot
            self.check_range(poles)
            self.check_range(zeros)
            #Plot poles and zeros
            #p_vec.append(poles)
            #z_vec.append(zeros)
            plt.plot(np.real(poles),np.imag(poles),'b*')
            plt.plot(np.real(zeros),np.imag(zeros),'r*')
        plt.plot(np.real(poles),np.imag(poles),'b*',label='Root Locus')
        plt.plot(np.real(zeros),np.imag(zeros),'r*',label='Zero Locus')

        #This part doesn't quite work yet because
        #I think MATLAB uses an adaptive step to compute
        #the locuse
        #Convert to Numpy Array
        #p_vec = np.asarray(p_vec)
        #z_vec = np.asarray(z_vec)
        #Plot locus
        #nrc = np.shape(p_vec)
        #Np = nrc[1]
        #for i in range(0,Np):
        #    plt.plot(np.real(p_vec[:,i]),np.imag(p_vec[:,i]),'b-')

        #Now compute the transfer function for KSTAR
        self.GCL = self.closed_loop(self.KSTAR,verbose=True)

        #In order to get the gain matrix K for state space we just need to grab the numerator of the
        ##controller and then multiply by KSTAR
        self.closedloopStateSpace()

        #Plot the last bits of the root locus
        plt.plot(np.real(self.closedloop_poles),np.imag(self.closedloop_poles),'ms',label='K='+str(KSTAR))
        #Last minute range check
        if self.xmax < 0:
            self.xmax = -0.1*self.xmin
        if self.ymin == self.ymax:
            self.ymin = self.xmin
            self.ymax = -self.ymin
        self.xmax *= 1.11
        self.xmin *= 1.11
        self.ymin *= 1.11
        self.ymax *= 1.11
        #Extra Bits
        #Plot real and imaginary axes
        plt.plot([self.xmin,self.xmax],[0,0],'k-')
        plt.plot([0,0],[self.ymin,self.ymax],'k-')
        #Set Range
        plt.xlim([self.xmin,self.xmax])
        plt.ylim([self.ymin,self.ymax])
        #Set labels
        plt.xlabel('Real')
        plt.ylabel('Imaginary')
        plt.legend()
        plt.grid()

        #Since we have a closed loop system let's simulate the closed loop system
        #in this case let's dynamically determine how long to simulate
        tfinal = self.howlong(self.closedloop_poles)
        self.integrateClosedLoop(0,tfinal)

        plt.show()

    def howlong(self,cpoles):
        closedloop_real_pole = np.max(np.real(cpoles))
        return abs(8./closedloop_real_pole) ##Simulate twice as long as needed

    def addmin(self,input):
        if len(input) > 0:
            self.xmins.append(np.min(np.real(input)))
            self.ymins.append(np.min(np.imag(input)))
    def addmax(self,input):
        if len(input) > 0:
            self.xmaxs.append(np.max(np.real(input)))
            self.ymaxs.append(np.max(np.imag(input)))

    ##Checking Range Function
    def check_range(self,input):
        if len(input) > 0:
            mp = np.min(np.real(input))
            mxp = np.max(np.real(input))
            if mp < self.xmin:
                self.xmin = mp
            if mxp > self.xmax:
                self.xmax = mxp
            ymp = np.min(np.imag(input))
            ymxp = np.max(np.imag(input))
            if ymp < self.ymin:
                self.ymin = ymp
            if ymxp > self.ymax:
                self.ymax = ymxp

def DerivativesOpenLoopStep(x,t,A,B):
    xdot = np.matmul(A,x) + np.transpose(B)
    return xdot[0]

def DerivativesOpenLoop(x,t,A,B):
    xdot = np.matmul(A,x)
    return xdot

def DerivativesClosedLoop(x,t,ACL,BKxc):
    #xdot = A*x + B*u
    #xdot = A*x + B*K*(xc-x)
    #xdot = A*x - B*K*x + B*K*xc
    #xdot = (A-B*K)*x + B*K*xc
    #xdot = ACL*x + BKxc
    xdot = np.matmul(ACL,x) + BKxc
    return xdot