from typing import Union, Optional, List, Dict, Tuple, Any
from copy import deepcopy

import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy.integrate import solve_ivp
from scipy import optimize
OdeResult = scipy.integrate._ivp.ivp.OdeResult

# Initialization of class
class Model:
    pass
class PyCompartModelResult:
    pass

class ArithmaticBase():
    def get_value(self,obj) -> float:
        """Get value of object regardless of Compartment or Param.
        """
        if isinstance(obj, Compartment) or isinstance(obj, Param):
            value = obj.value
        else:
            value = obj
        return value

    def get_equ(self,obj) -> float:
        """Get string information for object.
        """
        if isinstance(obj, Compartment):
            equ = obj.equ
        elif isinstance(obj, Param):
            equ = obj.equ
        else:
            equ = f"{obj}"
        return equ
    
    def __add__(self, obj):
        new = deepcopy(self)
        value = self.get_value(obj)
        equ = self.get_equ(obj)

        new.value = new.value + value
        new.equ = f"{new.equ} + {equ}"
        return new
    
    def __radd__(self, obj):
        new = deepcopy(self)
        value = self.get_value(obj)
        equ = self.get_equ(obj)

        new.value = value + new.v
        new.equ = f"{equ} + {new.equ}"
        return new
    
    def __sub__(self, obj):
        new = deepcopy(self)
        value = self.get_value(obj)
        equ = self.get_equ(obj)

        new.value = new.value - value 
        new.equ = f"{new.equ} - {equ}"
        return new

    def __rsub__(self, obj):
        new = deepcopy(self)
        value = self.get_value(obj)
        equ = self.get_equ(obj)

        new.value = value - new.value
        new.equ = f"{equ} - {new.equ}"
        return new
    
    def __mul__(self, obj):
        new = deepcopy(self)
        value = self.get_value(obj)
        equ = self.get_equ(obj)

        new.value = new.value * value
        new.equ = f"{new.equ} * ({equ})"
        return new
    
    def __rmul__(self, obj):
        new = deepcopy(self)
        value = self.get_value(obj)
        equ = self.get_equ(obj)

        new.value = value * new.value
        new.equ = f"({equ}) * {new.equ}"
        return new
    
    def __truediv__(self, obj):
        new = deepcopy(self)
        value = self.get_value(obj)
        equ = self.get_equ(obj)

        new.value = new.value / value
        new.equ = f"{new.equ} / ({equ})"
        return new
    
    def __rtruediv__(self, obj):
        new = deepcopy(self)
        value = self.get_value(obj)
        equ = self.get_equ(obj)

        new.value = value / new.value
        new.equ = f"({equ}) / {new.equ}"
        return new
    
    def __pos__(self):
        new = deepcopy(self)
        new.equ = f" + {new.equ}"
        return new
    
    def __neg__(self):
        new = deepcopy(self)
        new.value = - new.value
        new.equ = f" - {new.equ}"
        return new
    
    def __repr__(self):
        return f"{self.equ}"

class Compartment(ArithmaticBase):
    def __init__(self, name: str, index : int, value : Optional[float] = None)->None:
        """
        Args:
            name : a name of a parameter..
            value : a value of this parameter. 
                If value is None, set value as np.inf. 
                (this is for proceeding calculation without operand type error.)

        Attributes:
            d : if not set when __exist__ part, raise Error. 
        """
        self.name = name
        if value is None:
            value = np.inf
        self.value = value 
        self.d = None  
        self.equ = self.name
        self.index = index

    def set_init(self, value : float) -> None:
        """Set a value.
        """
        self.value = value

class Param(ArithmaticBase):
    def __init__(self,name: str, value: Optional[float] = None) -> None:
        """

        Args:
            name : a name of a parameter..
            value : a value of this parameter. 
                If value is None, set value as np.inf. 
                (this is for proceeding calculation without operand type error.)
        Attribute:
            name : name of parameters. The reason name is within curly bracket is 
                to replace that parameter with values in Model.create_function 
                with format stirngs..
            index : Used for passing arguments to solver of ODE.
        """
        self.name = name
        self.name_equ = f"{name}" 
        if value is None:
            value = np.inf
        self.value = value
        self.equ = self.name_equ
        self.index = None

    def set_value(self, value : float) -> None:
        """Set a value.
        """
        self.value = value

class Model:
    def __init__(self):
        """
        Attributes:
            C_index : index for number of compartment, used when creating function.
        """
        self.comparts = {}
        self.C_index = 0
        
    def C(self,name: str, value : Optional[float] = None) -> Compartment:
        """Set Compartment for Compartment model.
        """
        comp = Compartment(name,self.C_index, value)
        self.C_index += 1

        self.comparts[name] = comp
        self.value = value 
        return comp
        
    def __enter__(self):
        return self

    def __exit__(self,exc_type, exc_value, exc_traceback):
        for k,v in self.comparts.items():
            if v.d is None:
                raise Exception(f"{k}'s difference (d) is not set")

    def create_function(self, params: Tuple[Param,...], verbose : bool = True) -> None:
        """Create function string with parameters information.
        """
        # Order by index is same as order inside self.params. 
        self.params = {}
        for i,x in enumerate(params):
            x.index = i
            self.params[x.name] = x

        # Create string version of function.
        if len(self.params):
            str_params = ", ".join([x.name for x in self.params.values()])
        fun = f"def _f(t, y, {str_params}):\n"
        for k,v in self.comparts.items():
            fun += f"    {v.name} = y[{v.index}]\n"
        ds= []
        for k,v in self.comparts.items():
            fun += f"    d{k} = {v.d.equ}\n"
            ds.append(f"d{k}")
        ret = ",".join(ds)
        ret = f"    return [{ret}]"
        fun += ret

        self.fun_str = fun
        exec(fun, globals())
        self.fun = _f

        if verbose:
            print(self.fun_str)

    def get_compartment_inits(self):
        """Sort by index of components of compartment model and return its initial values.
        """
        init = []
        for k, v in sorted(self.comparts.items(), key=lambda item: item[1].index):
            if np.isinf(v.value):
                raise Exception(f"{k} is not correctly set. ")
            init.append(v.value)
        return init

    def get_args_from_params(self):
        """Get arguments from parameters. It is noted that self.params are ordered by index.
        """
        args = []
        for k, v in sorted(self.params.items(), key=lambda item: item[1].index):
            if np.isinf(v.value):
                raise Exception(f"{k} is not correctly set. ")
            args.append(v.value)
        return args

    def solve(self,t_span,raw: bool = False, **kargs) -> PyCompartModelResult:
        """
        Args:
            raw : if True, return results from solve_ivp.
        """
        inits = self.get_compartment_inits()
        args = self.get_args_from_params()
        res = solve_ivp(self.fun, t_span=t_span,y0=inits, args=args, **kargs)
        if raw:
            return res
        res = PyCompartModelResult(self,res)

        return res

class PyCompartModelResult:
    def __init__(self, 
                 model : Model, 
                 res : OdeResult,
                 ) -> None: 
        model = deepcopy(model)
        self.model = model
        self.fun_str = model.fun_str
        self.comparts = model.comparts
        self.params = model.params
        self.args = {x.name:x.value for x in self.params.values()}
        self.inits = {x.name:x.value for x in self.comparts.values()}
        self.result = self.reverse_res_to_compartments(res)

    def reverse_res_to_compartments(self, res : OdeResult) -> OdeResult:
        """Reverse results of y returned from Model.solve method into components results. 

        Note:
            If the result name is conflicted with default name of the results of solve_ivp,
            Raise Error.
        """
        index_name = {v.index : k for k,v in self.comparts.items()}
        dir_ = dir(res)
        for ind, name in index_name.items():
            if name in dir_:
                raise Exception(f"Compartment name, '{name}' is conflicted with default result names")
            setattr(res, name, res.y[ind])
        return res
    
    def summary(self):
        s = f"""inits : {self.inits}
args : {self.args}
message : {self.result.message}
"""
        print(s)


    def __repr__(self):
        return __class__.__name__

def plot_over_time(
    ode_res : PyCompartModelResult,
    comparts : Optional[List[str]]= None,
    ax : Optional[plt.Axes] = None,
):
    """Plot results of a solver against time, 
    """
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)

    res = ode_res.result
    t = res.t

    if comparts is not None:
        keys = []
        for c in comparts:
            if isinstance(c, Compartment):
                keys.append(c.name)
            else:
                keys.append(c)
    else:
        keys = ode_res.comparts.keys()

    for k in keys:
        v = getattr(res,k)
        ax.plot(t, v, label=k)
    ax.set_xlabel("Time")
    plt.legend()

