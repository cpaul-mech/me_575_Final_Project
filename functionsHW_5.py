import numpy as np

# define the objective functions:
# first up, the Easom function: {\displaystyle f(x,y)=-\cos \left(x\right)\cos \left(y\right)\exp \left(-\left(\left(x-\pi \right)^{2}+\left(y-\pi \right)^{2}\right)\right)}
def easomFunction(x):
    ### x is a 2-element numpy array
    result= -np.cos(x[0])*np.cos(x[1])*np.exp(-((x[0]-np.pi)**2+(x[1]-np.pi)**2))
    return result
def gradEasom(x):
    x0, x1 = x[0], x[1]
    exp_term = np.exp(-((x0-np.pi)**2 + (x1-np.pi)**2))
    dx0 = exp_term * np.cos(x1) * (np.sin(x0) + 2*(x0-np.pi)*np.cos(x0))
    dx1 = exp_term * np.cos(x0) * (np.sin(x1) + 2*(x1-np.pi)*np.cos(x1))
    return np.array([dx0, dx1])
def g1Easom(x):  # To enforce (-x2 + ((x1-3)^2 + 2.5)) <= 0 → return -(original)
    return -(-x[1] + ((x[0]-3)**2 + 2.5))
def g2Easom(x): # should be -2x1+ 9.5 -x2 <= 0
    return -(-2.*x[0] + 9.5 - x[1])

# himmelbau's function: f(x1,x2) = (x1^2 + x2 - 11)^2 + (x1 + x2^2 - 7)^2
def himmelblauFunction(x):
    ### x is a 2-element numpy array
    result = (x[0]**2 + x[1] - 11.)**2 + (x[0] + x[1]**2 - 7.)**2
    return result
def gradHimmelblau(x):
    x0, x1 = x[0], x[1]
    term1 = x0**2 + x1 - 11
    term2 = x0 + x1**2 - 7
    dx0 = 4*x0*term1 + 2*term2
    dx1 = 2*term1 + 4*x1*term2
    return np.array([dx0, dx1])
def g1Himmelblau(x): # should be 0 = (x1-1)^2 + (x2-1)^2 - 6
    return (x[0]-1.)**2 + (x[1]-1.)**2 - 6.
def g2Himmelblau(x): # should be (-2x1 -x2 + 5) <= 0
    return -(-2.*x[0] - x[1] + 5.)

# now the three hump camel function: f(x1,x2) = 2*x1^2 - 1.05*x1^4 + x1^6/6 + x1*x2 + x2^2
def threeHumpCamelFunction(x):
    ### x is a 2-element numpy array
    result = 2*x[0]**2 - 1.05*x[0]**4 + x[0]**6/6 + x[0]*x[1] + x[1]**2
    return result
def gradThreeHumpCamel(x):
    x0, x1 = x[0], x[1]
    dx0 = 4*x0 - 4.2*x0**3 + x0**5 + x1
    dx1 = x0 + 2*x1
    return np.array([dx0, dx1])
def g1threeHumpCamel(x): # should be .5x1 - x2 -.25 <= 0
    return -(.5*x[0] - x[1] - .25)
def g2threeHumpCamel(x): # should be  -3x1 + 3 - x2 <= 0
    return -(-3.*x[0] + 3. - x[1])