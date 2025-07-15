import numpy as np
import math

class UF1:
    """
    UF1 Test Function (CEC'09 Competition)
    2-objective, 30-dimensional optimization problem
    """
    def __init__(self, dim=30):
        self.dim = dim
        self.bounds = [(0, 1) if i == 0 else (-1, 1) for i in range(dim)]
        
    def __call__(self, x):
        """Evaluate UF1 function"""
        x = np.array(x)
        n = len(x)
        
        # Separate odd and even indices (1-indexed in original definition)
        J1 = []  # odd indices (2, 4, 6, ...)
        J2 = []  # even indices (3, 5, 7, ...)
        
        for i in range(1, n):  # Skip first variable (x[0])
            if (i + 1) % 2 == 0:  # Even index in 1-indexed
                J1.append(i)
            else:  # Odd index in 1-indexed
                J2.append(i)
        
        # Calculate objective functions
        sum1 = sum([(x[j] - np.sin(6*np.pi*x[0] + (j+1)*np.pi/n))**2 for j in J1])
        sum2 = sum([(x[j] - np.cos(6*np.pi*x[0] + (j+1)*np.pi/n))**2 for j in J2])
        
        f1 = x[0] + (2/len(J1)) * sum1 if J1 else x[0]
        f2 = 1 - np.sqrt(x[0]) + (2/len(J2)) * sum2 if J2 else 1 - np.sqrt(x[0])
        
        return np.array([f1, f2])

class UF7:
    """
    UF7 Test Function (CEC'09 Competition)
    2-objective, 30-dimensional optimization problem
    """
    def __init__(self, dim=30):
        self.dim = dim
        self.bounds = [(0, 1) if i == 0 else (-1, 1) for i in range(dim)]
        
    def __call__(self, x):
        """Evaluate UF7 function"""
        x = np.array(x)
        n = len(x)
        
        # Separate odd and even indices (1-indexed in original definition)
        J1 = []  # odd indices (2, 4, 6, ...)
        J2 = []  # even indices (3, 5, 7, ...)
        
        for i in range(1, n):  # Skip first variable (x[0])
            if (i + 1) % 2 == 0:  # Even index in 1-indexed
                J1.append(i)
            else:  # Odd index in 1-indexed
                J2.append(i)
        
        # Calculate y values
        y = [x[0]]
        for i in range(1, n):
            y.append(x[i] - np.sin(6*np.pi*x[0] + (i+1)*np.pi/n))
        
        # Calculate objective functions
        sum1 = sum([y[j]**2 for j in J1])
        sum2 = sum([y[j]**2 for j in J2])
        
        f1 = y[0] + (2/len(J1)) * sum1 if J1 else y[0]
        f2 = 1 - y[0]**2 + (2/len(J2)) * sum2 if J2 else 1 - y[0]**2
        
        return np.array([f1, f2])

class ZDT1:
    """
    ZDT1 Test Function
    2-objective, 30-dimensional optimization problem
    """
    def __init__(self, dim=30):
        self.dim = dim
        self.bounds = [(0, 1) for _ in range(dim)]
        
    def __call__(self, x):
        """Evaluate ZDT1 function"""
        x = np.array(x)
        n = len(x)
        
        f1 = x[0]
        g = 1 + 9 * np.sum(x[1:]) / (n - 1)
        h = 1 - np.sqrt(f1 / g)
        f2 = g * h
        
        return np.array([f1, f2])

class ZDT2:
    """
    ZDT2 Test Function
    2-objective, 30-dimensional optimization problem
    """
    def __init__(self, dim=30):
        self.dim = dim
        self.bounds = [(0, 1) for _ in range(dim)]
        
    def __call__(self, x):
        """Evaluate ZDT2 function"""
        x = np.array(x)
        n = len(x)
        
        f1 = x[0]
        g = 1 + 9 * np.sum(x[1:]) / (n - 1)
        h = 1 - (f1 / g)**2
        f2 = g * h
        
        return np.array([f1, f2])

class ZDT3:
    """
    ZDT3 Test Function
    2-objective, 30-dimensional optimization problem
    """
    def __init__(self, dim=30):
        self.dim = dim
        self.bounds = [(0, 1) for _ in range(dim)]
        
    def __call__(self, x):
        """Evaluate ZDT3 function"""
        x = np.array(x)
        n = len(x)
        
        f1 = x[0]
        g = 1 + 9 * np.sum(x[1:]) / (n - 1)
        h = 1 - np.sqrt(f1 / g) - (f1 / g) * np.sin(10 * np.pi * f1)
        f2 = g * h
        
        return np.array([f1, f2])

class DTLZ1:
    """
    DTLZ1 Test Function
    3-objective, scalable dimensional optimization problem
    """
    def __init__(self, dim=7, n_obj=3):
        self.dim = dim
        self.n_obj = n_obj
        self.bounds = [(0, 1) for _ in range(dim)]
        
    def __call__(self, x):
        """Evaluate DTLZ1 function"""
        x = np.array(x)
        
        # Calculate g(x)
        g = 100 * (len(x) - self.n_obj + 1 + 
                  np.sum([(xi - 0.5)**2 - np.cos(20*np.pi*(xi - 0.5)) 
                         for xi in x[self.n_obj-1:]]))
        
        # Calculate objectives
        f = []
        for i in range(self.n_obj):
            if i == 0:
                fi = 0.5 * (1 + g) * np.prod(x[:self.n_obj-1])
            elif i == self.n_obj - 1:
                fi = 0.5 * (1 + g) * (1 - x[0])
            else:
                fi = 0.5 * (1 + g) * (1 - x[self.n_obj-1-i]) * np.prod(x[:self.n_obj-1-i])
            f.append(fi)
            
        return np.array(f)

class DTLZ2:
    """
    DTLZ2 Test Function
    3-objective, scalable dimensional optimization problem
    """
    def __init__(self, dim=12, n_obj=3):
        self.dim = dim
        self.n_obj = n_obj
        self.bounds = [(0, 1) for _ in range(dim)]
        
    def __call__(self, x):
        """Evaluate DTLZ2 function"""
        x = np.array(x)
        
        # Calculate g(x)
        g = np.sum([(xi - 0.5)**2 for xi in x[self.n_obj-1:]])
        
        # Calculate objectives
        f = []
        for i in range(self.n_obj):
            if i == 0:
                fi = (1 + g) * np.prod([np.cos(xi * np.pi / 2) for xi in x[:self.n_obj-1]])
            elif i == self.n_obj - 1:
                fi = (1 + g) * np.sin(x[0] * np.pi / 2)
            else:
                fi = (1 + g) * np.sin(x[self.n_obj-1-i] * np.pi / 2) * \
                     np.prod([np.cos(xi * np.pi / 2) for xi in x[:self.n_obj-1-i]])
            f.append(fi)
            
        return np.array(f)

class Schaffer:
    """
    Schaffer Test Function
    2-objective, 1-dimensional optimization problem
    """
    def __init__(self, dim=1):
        self.dim = dim
        self.bounds = [(-1000, 1000) for _ in range(dim)]
        
    def __call__(self, x):
        """Evaluate Schaffer function"""
        x = np.array(x)
        x = x[0] if len(x) > 0 else x
        
        if x <= 1:
            f1 = -x
        elif x <= 3:
            f1 = x - 2
        elif x <= 4:
            f1 = 4 - x
        else:
            f1 = x - 4
            
        f2 = (x - 5)**2
        
        return np.array([f1, f2])

# Dictionary of available test functions
TEST_FUNCTIONS = {
    'UF1': UF1,
    'UF7': UF7,
    'ZDT1': ZDT1,
    'ZDT2': ZDT2,
    'ZDT3': ZDT3,
    'DTLZ1': DTLZ1,
    'DTLZ2': DTLZ2,
    'Schaffer': Schaffer
}

def get_test_function(name, **kwargs):
    """Get a test function by name"""
    if name not in TEST_FUNCTIONS:
        raise ValueError(f"Unknown test function: {name}. Available: {list(TEST_FUNCTIONS.keys())}")
    
    return TEST_FUNCTIONS[name](**kwargs)