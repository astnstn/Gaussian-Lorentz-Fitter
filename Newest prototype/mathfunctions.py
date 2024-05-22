"""
mathfunctions.py

This script contains the MathFunction class
"""

import numpy as np
from scipy.optimize import curve_fit
import inspect
import dill
import os


def save(function, name, cwd=False):
    os.chdir(".\saved_functions") if cwd == False else os.chdir(os.getcwd())
    file = open(name + ".txt", 'wb')
    dill.dump(function, file)
    file.close()


def load(name, cwd=False):
    os.chdir(".\saved_functions") if cwd == False else os.chdir(os.getcwd())
    file = open(name + ".txt", 'rb')
    fun = dill.load(file)
    file.close()
    return fun


def join_functions(func_list):
    func = func_list[0]
    for other in func_list[1:]:
        func += other
    return func


# function wrapped in class
class Function:
    """
    This is a function wrapped in a class which is contained inside a list 
    inside a MathFunction object.
    """

    # used to scale the y value of the function
    coeff = 1

    def __init__(self, function, params=None, name=None, errors=None):
        """
        Initialises a function

        Parameters
        ----------
        function : function
            Python function which defines the mathematical function.
        params : tuple, optional
            The params used in the function (not x/y). The default is None.
        name : str, optional
            Name of the function. The default is None.
        errors : tuple, optional
            Known errors in the params. The default is None.

        Returns
        -------
        Function object.

        """
        # initialises with chosen/default name, a function, and parameters if chosen
        self.name = name if name else function.__name__

        self.params = {}
        # gets the parameter names from the arguments of the function with inspect
        # sets params
        if params:
            [self.params.update({x: param}) for x, param in zip(
                inspect.getfullargspec(function).args[1:], params)]
        else:
            [self.params.update({x: None})
             for x in inspect.getfullargspec(function).args[1:]]
        self.function = function

        # sets errors if given
        self.errors = {}
        if errors:
            [self.errors.update({x: error}) for x, error in zip(
                inspect.getfullargspec(function).args[1:], errors)]
        else:
            [self.errors.update({x: None})
             for x in inspect.getfullargspec(function).args[1:]]

    def __repr__(self):
        return self.name.ljust(30, '.') + str(self.params)

    def __call__(self, x, *args):
        # calls the function with parameters already set
        if not args:
            return self.function(x, *list(self.params.values()))*self.coeff
        # calls the function with specific parameters given
        else:
            return self.function(x, *args)*self.coeff


# actual function used, contains one or more instances of the Function class
class MathFunction:
    def __init__(self, function, params=None, name=None, errors=None):

        # initialises a Function instance and adds it to list
        self.functions = [Function(function, params, name, errors)]

    def __repr__(self):
        fnames = [fun.__repr__() for fun in self.functions]
        return "***MathFunction***\n\n" + "\n\n".join(fnames)

    # uses default parameters if no arguments set
    def __call__(self, x, *args):
        if not args:
            return sum(func(x) for func in self.functions)
        else:
            i = 0
            val = 0
            for k in range(len(self.functions)):
                theseArgs = args[i:i + len(self.functions[k].params)]
                val += self.functions[k](x, *theseArgs)
                i += len(self.functions[k].params)
            return val

    # indexing accesses individual functions
    def __getitem__(self, i):
        return self.functions[i]

    # adding joins the function lists
    def __add__(self, other):
        self.functions += other.functions
        return self

    def __mul__(self, other):
        for func in self.functions:
            func.coeff *= other
        return self

    # uses scipy curve_fit to get optimal parameters and error
    def fit(self, x, y):

        estimates = []
        for func in self.functions:
            estimates += list(func.params.values())

        # Convert any array-like elements to scalars (Hotfix)
        estimates = [param.item() if isinstance(param, np.ndarray)
                     else param for param in estimates]

        opt, cov = curve_fit(self, x, y, estimates)
        self.cov = cov
        i = 0
        for func in self.functions:
            for key, param in zip(func.params.keys(), opt[i:i + len(func.params)]):
                func.params[key] = param
            for key, diag in zip(func.params.keys(), np.diag(cov[i:i + len(func.params)])):
                func.errors[key] = np.sqrt(abs(diag))
            i += len(func.params)

    def info(self, sf=3):
        out = ""
        for func in self.functions:
            out += "\n" + func.name + "\n"
            for key in func.params.keys():
                value, error = func.params[key], func.errors[key]
                out += f"{key} : {value:.{sf}g} +/- {error:.{sf}g} \n"
        print(out)
