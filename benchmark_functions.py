import numpy as np
from typing import Callable, Tuple, Dict, Any

class BenchmarkFunctions:
    """
    Collection of benchmark functions for testing optimization algorithms.
    
    These functions are commonly used in the optimization literature to evaluate
    the performance of metaheuristic algorithms.
    """
    
    @staticmethod
    def sphere(x: np.ndarray) -> float:
        """
        Sphere function: f(x) = sum(x_i^2)
        Global minimum: f(0,0,...,0) = 0
        Search domain: [-100, 100]^n
        """
        return np.sum(x**2)
    
    @staticmethod
    def rosenbrock(x: np.ndarray) -> float:
        """
        Rosenbrock function: f(x) = sum(100*(x_{i+1} - x_i^2)^2 + (1-x_i)^2)
        Global minimum: f(1,1,...,1) = 0
        Search domain: [-2.048, 2.048]^n
        """
        return np.sum(100 * (x[1:] - x[:-1]**2)**2 + (1 - x[:-1])**2)
    
    @staticmethod
    def ackley(x: np.ndarray) -> float:
        """
        Ackley function: f(x) = -20*exp(-0.2*sqrt(1/n*sum(x_i^2))) - exp(1/n*sum(cos(2*pi*x_i))) + 20 + e
        Global minimum: f(0,0,...,0) = 0
        Search domain: [-32.768, 32.768]^n
        """
        n = len(x)
        term1 = -20 * np.exp(-0.2 * np.sqrt(np.sum(x**2) / n))
        term2 = -np.exp(np.sum(np.cos(2 * np.pi * x)) / n)
        return term1 + term2 + 20 + np.exp(1)
    
    @staticmethod
    def rastrigin(x: np.ndarray) -> float:
        """
        Rastrigin function: f(x) = 10*n + sum(x_i^2 - 10*cos(2*pi*x_i))
        Global minimum: f(0,0,...,0) = 0
        Search domain: [-5.12, 5.12]^n
        """
        n = len(x)
        return 10 * n + np.sum(x**2 - 10 * np.cos(2 * np.pi * x))
    
    @staticmethod
    def griewank(x: np.ndarray) -> float:
        """
        Griewank function: f(x) = sum(x_i^2)/4000 - prod(cos(x_i/sqrt(i))) + 1
        Global minimum: f(0,0,...,0) = 0
        Search domain: [-600, 600]^n
        """
        term1 = np.sum(x**2) / 4000
        term2 = np.prod(np.cos(x / np.sqrt(np.arange(1, len(x) + 1))))
        return term1 - term2 + 1
    
    @staticmethod
    def schwefel(x: np.ndarray) -> float:
        """
        Schwefel function: f(x) = 418.9829*n - sum(x_i*sin(sqrt(|x_i|)))
        Global minimum: f(420.9687,420.9687,...,420.9687) = 0
        Search domain: [-500, 500]^n
        """
        n = len(x)
        return 418.9829 * n - np.sum(x * np.sin(np.sqrt(np.abs(x))))
    
    @staticmethod
    def levy(x: np.ndarray) -> float:
        """
        Levy function: f(x) = sin^2(pi*w1) + sum((w_i-1)^2*(1+10*sin^2(pi*w_i+1))) + (w_n-1)^2*(1+sin^2(2*pi*w_n))
        where w_i = 1 + (x_i-1)/4
        Global minimum: f(1,1,...,1) = 0
        Search domain: [-10, 10]^n
        """
        w = 1 + (x - 1) / 4
        term1 = np.sin(np.pi * w[0])**2
        term2 = np.sum((w[:-1] - 1)**2 * (1 + 10 * np.sin(np.pi * w[:-1] + 1)**2))
        term3 = (w[-1] - 1)**2 * (1 + np.sin(2 * np.pi * w[-1])**2)
        return term1 + term2 + term3
    
    @staticmethod
    def michalewicz(x: np.ndarray, m: float = 10) -> float:
        """
        Michalewicz function: f(x) = -sum(sin(x_i)*sin(i*x_i^2/pi)^(2*m))
        Global minimum: approximately -9.66 for n=2, -19.64 for n=5, -29.63 for n=10
        Search domain: [0, pi]^n
        """
        i = np.arange(1, len(x) + 1)
        return -np.sum(np.sin(x) * np.sin(i * x**2 / np.pi)**(2 * m))
    
    @staticmethod
    def zakharov(x: np.ndarray) -> float:
        """
        Zakharov function: f(x) = sum(x_i^2) + (sum(0.5*i*x_i))^2 + (sum(0.5*i*x_i))^4
        Global minimum: f(0,0,...,0) = 0
        Search domain: [-5, 10]^n
        """
        i = np.arange(1, len(x) + 1)
        term1 = np.sum(x**2)
        term2 = np.sum(0.5 * i * x)
        return term1 + term2**2 + term2**4
    
    @staticmethod
    def dixon_price(x: np.ndarray) -> float:
        """
        Dixon-Price function: f(x) = (x_1-1)^2 + sum(i*(2*x_i^2-x_{i-1})^2)
        Global minimum: f(2^(-(2^i-2)/(2^i)), i=1,2,...,n) = 0
        Search domain: [-10, 10]^n
        """
        term1 = (x[0] - 1)**2
        i = np.arange(2, len(x) + 1)
        term2 = np.sum(i * (2 * x[1:]**2 - x[:-1])**2)
        return term1 + term2
    
    @staticmethod
    def sum_squares(x: np.ndarray) -> float:
        """
        Sum Squares function: f(x) = sum(i*x_i^2)
        Global minimum: f(0,0,...,0) = 0
        Search domain: [-10, 10]^n
        """
        i = np.arange(1, len(x) + 1)
        return np.sum(i * x**2)
    
    @staticmethod
    def booth(x: np.ndarray) -> float:
        """
        Booth function (2D): f(x,y) = (x + 2*y - 7)^2 + (2*x + y - 5)^2
        Global minimum: f(1,3) = 0
        Search domain: [-10, 10]^2
        """
        if len(x) != 2:
            raise ValueError("Booth function is only defined for 2D")
        return (x[0] + 2*x[1] - 7)**2 + (2*x[0] + x[1] - 5)**2
    
    @staticmethod
    def matyas(x: np.ndarray) -> float:
        """
        Matyas function (2D): f(x,y) = 0.26*(x^2 + y^2) - 0.48*x*y
        Global minimum: f(0,0) = 0
        Search domain: [-10, 10]^2
        """
        if len(x) != 2:
            raise ValueError("Matyas function is only defined for 2D")
        return 0.26 * (x[0]**2 + x[1]**2) - 0.48 * x[0] * x[1]
    
    @staticmethod
    def easom(x: np.ndarray) -> float:
        """
        Easom function (2D): f(x,y) = -cos(x)*cos(y)*exp(-((x-pi)^2 + (y-pi)^2))
        Global minimum: f(pi,pi) = -1
        Search domain: [-100, 100]^2
        """
        if len(x) != 2:
            raise ValueError("Easom function is only defined for 2D")
        return -np.cos(x[0]) * np.cos(x[1]) * np.exp(-((x[0] - np.pi)**2 + (x[1] - np.pi)**2))
    
    @staticmethod
    def cross_in_tray(x: np.ndarray) -> float:
        """
        Cross-in-Tray function (2D): f(x,y) = -0.0001*(|sin(x)*sin(y)*exp(|100-sqrt(x^2+y^2)/pi|)| + 1)^0.1
        Global minimum: f(±1.34941,±1.34941) = -2.06261
        Search domain: [-10, 10]^2
        """
        if len(x) != 2:
            raise ValueError("Cross-in-Tray function is only defined for 2D")
        term = np.abs(np.sin(x[0]) * np.sin(x[1]) * np.exp(np.abs(100 - np.sqrt(x[0]**2 + x[1]**2) / np.pi)))
        return -0.0001 * (term + 1)**0.1
    
    @staticmethod
    def eggholder(x: np.ndarray) -> float:
        """
        Eggholder function (2D): f(x,y) = -(y+47)*sin(sqrt(|x/2+(y+47)|)) - x*sin(sqrt(|x-(y+47)|))
        Global minimum: f(512,404.2319) = -959.6407
        Search domain: [-512, 512]^2
        """
        if len(x) != 2:
            raise ValueError("Eggholder function is only defined for 2D")
        term1 = -(x[1] + 47) * np.sin(np.sqrt(np.abs(x[0]/2 + (x[1] + 47))))
        term2 = -x[0] * np.sin(np.sqrt(np.abs(x[0] - (x[1] + 47))))
        return term1 + term2
    
    @staticmethod
    def holder_table(x: np.ndarray) -> float:
        """
        Holder Table function (2D): f(x,y) = -|sin(x)*cos(y)*exp(|1-sqrt(x^2+y^2)/pi|)|
        Global minimum: f(±8.05502,±9.66459) = -19.2085
        Search domain: [-10, 10]^2
        """
        if len(x) != 2:
            raise ValueError("Holder Table function is only defined for 2D")
        term = np.sin(x[0]) * np.cos(x[1]) * np.exp(np.abs(1 - np.sqrt(x[0]**2 + x[1]**2) / np.pi))
        return -np.abs(term)
    
    @staticmethod
    def mccormick(x: np.ndarray) -> float:
        """
        McCormick function (2D): f(x,y) = sin(x+y) + (x-y)^2 - 1.5*x + 2.5*y + 1
        Global minimum: f(-0.54719,-1.54719) = -1.9133
        Search domain: x ∈ [-1.5, 4], y ∈ [-3, 4]
        """
        if len(x) != 2:
            raise ValueError("McCormick function is only defined for 2D")
        return np.sin(x[0] + x[1]) + (x[0] - x[1])**2 - 1.5*x[0] + 2.5*x[1] + 1
    
    @staticmethod
    def schaffer_n2(x: np.ndarray) -> float:
        """
        Schaffer N.2 function (2D): f(x,y) = 0.5 + (sin^2(x^2-y^2) - 0.5)/(1 + 0.001*(x^2+y^2))^2
        Global minimum: f(0,0) = 0
        Search domain: [-100, 100]^2
        """
        if len(x) != 2:
            raise ValueError("Schaffer N.2 function is only defined for 2D")
        numerator = np.sin(x[0]**2 - x[1]**2)**2 - 0.5
        denominator = (1 + 0.001 * (x[0]**2 + x[1]**2))**2
        return 0.5 + numerator / denominator
    
    @staticmethod
    def schaffer_n4(x: np.ndarray) -> float:
        """
        Schaffer N.4 function (2D): f(x,y) = 0.5 + (cos^2(sin(|x^2-y^2|)) - 0.5)/(1 + 0.001*(x^2+y^2))^2
        Global minimum: f(0,±1.25313) = 0.292579
        Search domain: [-100, 100]^2
        """
        if len(x) != 2:
            raise ValueError("Schaffer N.4 function is only defined for 2D")
        numerator = np.cos(np.sin(np.abs(x[0]**2 - x[1]**2)))**2 - 0.5
        denominator = (1 + 0.001 * (x[0]**2 + x[1]**2))**2
        return 0.5 + numerator / denominator

def get_function_info() -> Dict[str, Dict[str, Any]]:
    """
    Get information about all benchmark functions including their properties.
    
    Returns:
        Dictionary with function names as keys and their properties as values
    """
    return {
        'sphere': {
            'function': BenchmarkFunctions.sphere,
            'dimensions': 'any',
            'domain': [-100, 100],
            'global_minimum': 0,
            'global_minimizer': 'zeros',
            'type': 'unimodal'
        },
        'rosenbrock': {
            'function': BenchmarkFunctions.rosenbrock,
            'dimensions': 'any',
            'domain': [-2.048, 2.048],
            'global_minimum': 0,
            'global_minimizer': 'ones',
            'type': 'unimodal'
        },
        'ackley': {
            'function': BenchmarkFunctions.ackley,
            'dimensions': 'any',
            'domain': [-32.768, 32.768],
            'global_minimum': 0,
            'global_minimizer': 'zeros',
            'type': 'multimodal'
        },
        'rastrigin': {
            'function': BenchmarkFunctions.rastrigin,
            'dimensions': 'any',
            'domain': [-5.12, 5.12],
            'global_minimum': 0,
            'global_minimizer': 'zeros',
            'type': 'multimodal'
        },
        'griewank': {
            'function': BenchmarkFunctions.griewank,
            'dimensions': 'any',
            'domain': [-600, 600],
            'global_minimum': 0,
            'global_minimizer': 'zeros',
            'type': 'multimodal'
        },
        'schwefel': {
            'function': BenchmarkFunctions.schwefel,
            'dimensions': 'any',
            'domain': [-500, 500],
            'global_minimum': 0,
            'global_minimizer': [420.9687],
            'type': 'multimodal'
        },
        'levy': {
            'function': BenchmarkFunctions.levy,
            'dimensions': 'any',
            'domain': [-10, 10],
            'global_minimum': 0,
            'global_minimizer': 'ones',
            'type': 'multimodal'
        },
        'michalewicz': {
            'function': BenchmarkFunctions.michalewicz,
            'dimensions': 'any',
            'domain': [0, np.pi],
            'global_minimum': 'varies',
            'global_minimizer': 'varies',
            'type': 'multimodal'
        },
        'zakharov': {
            'function': BenchmarkFunctions.zakharov,
            'dimensions': 'any',
            'domain': [-5, 10],
            'global_minimum': 0,
            'global_minimizer': 'zeros',
            'type': 'unimodal'
        },
        'dixon_price': {
            'function': BenchmarkFunctions.dixon_price,
            'dimensions': 'any',
            'domain': [-10, 10],
            'global_minimum': 0,
            'global_minimizer': 'varies',
            'type': 'unimodal'
        },
        'sum_squares': {
            'function': BenchmarkFunctions.sum_squares,
            'dimensions': 'any',
            'domain': [-10, 10],
            'global_minimum': 0,
            'global_minimizer': 'zeros',
            'type': 'unimodal'
        },
        'booth': {
            'function': BenchmarkFunctions.booth,
            'dimensions': 2,
            'domain': [-10, 10],
            'global_minimum': 0,
            'global_minimizer': [1, 3],
            'type': 'unimodal'
        },
        'matyas': {
            'function': BenchmarkFunctions.matyas,
            'dimensions': 2,
            'domain': [-10, 10],
            'global_minimum': 0,
            'global_minimizer': [0, 0],
            'type': 'unimodal'
        },
        'easom': {
            'function': BenchmarkFunctions.easom,
            'dimensions': 2,
            'domain': [-100, 100],
            'global_minimum': -1,
            'global_minimizer': [np.pi, np.pi],
            'type': 'multimodal'
        },
        'cross_in_tray': {
            'function': BenchmarkFunctions.cross_in_tray,
            'dimensions': 2,
            'domain': [-10, 10],
            'global_minimum': -2.06261,
            'global_minimizer': [1.34941, 1.34941],
            'type': 'multimodal'
        },
        'eggholder': {
            'function': BenchmarkFunctions.eggholder,
            'dimensions': 2,
            'domain': [-512, 512],
            'global_minimum': -959.6407,
            'global_minimizer': [512, 404.2319],
            'type': 'multimodal'
        },
        'holder_table': {
            'function': BenchmarkFunctions.holder_table,
            'dimensions': 2,
            'dimensions': 2,
            'domain': [-10, 10],
            'global_minimum': -19.2085,
            'global_minimizer': [8.05502, 9.66459],
            'type': 'multimodal'
        },
        'mccormick': {
            'function': BenchmarkFunctions.mccormick,
            'dimensions': 2,
            'domain': [-1.5, 4],  # x ∈ [-1.5, 4], y ∈ [-3, 4]
            'global_minimum': -1.9133,
            'global_minimizer': [-0.54719, -1.54719],
            'type': 'multimodal'
        },
        'schaffer_n2': {
            'function': BenchmarkFunctions.schaffer_n2,
            'dimensions': 2,
            'domain': [-100, 100],
            'global_minimum': 0,
            'global_minimizer': [0, 0],
            'type': 'multimodal'
        },
        'schaffer_n4': {
            'function': BenchmarkFunctions.schaffer_n4,
            'dimensions': 2,
            'dimensions': 2,
            'domain': [-100, 100],
            'global_minimum': 0.292579,
            'global_minimizer': [0, 1.25313],
            'type': 'multimodal'
        }
    }