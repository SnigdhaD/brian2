'''
Implementation of `BinomialFunction`
'''
import numpy as np

from brian2.core.functions import Function, DEFAULT_FUNCTIONS
from brian2.units.fundamentalunits import check_units
from .stringtools import word_substitute


__all__ = ['BinomialFunction']


class BinomialFunction(Function):

    @check_units(n=1, p=1)
    def __init__(self, n, p, approximate=True):
        '''
        Parameters
        ----------
        n : int
            Number of samples
        p : float
            Probablility
        approximate : bool, optional
            Whether to approximate the binomial with a normal distribution if
            :math:`n\cdot p > 5`. Defaults to ``True``.
        '''

        #Python implementation
        use_normal = approximate and (n*p > 5)
        if use_normal:
            loc = n*p
            scale = np.sqrt(n*p*(1-p))
            def sample_function(vectorisation_idx):
                try:
                    N = len(vectorisation_idx)
                except TypeError:
                    N = int(vectorisation_idx)
                return np.random.normal(loc, scale, size=N)
        else:
            def sample_function(vectorisation_idx):
                try:
                    N = len(vectorisation_idx)
                except TypeError:
                    N = int(vectorisation_idx)
                return np.random.binomial(n, p, size=N)

        Function.__init__(self, pyfunc=lambda: sample_function(1),
                          arg_units=[], return_unit=1)
        self.implementations.add_implementation('numpy', sample_function)

        # C++ implementation
        # Inversion transform sampling
        if use_normal:
            loc = n*p
            scale = np.sqrt(n*p*(1-p))
            cpp_code = '''
            float _call_sample_function(py::object& numpy_randn)
            {
                return _call_randn(numpy_randn) * %SCALE% + %LOC%;
            }
            '''.replace('%SCALE%', '%.15f' % scale).replace('%LOC%', '%.15f' % loc)
            hash_defines = '#define _sample_function(_vectorisation_idx) _call_sample_function(_python_randn)'
            dependencies = {'randn': DEFAULT_FUNCTIONS['randn']}
        else:
            # The following code is an almost exact copy of numpy's
            # rk_binomial_inversion function
            # (numpy/random/mtrand/distributions.c)
            q = 1.0 - p
            qn = np.exp(n * np.log(q))
            bound = min(n, n*p + 10.0*np.sqrt(n*p*q + 1))
            cpp_code = '''
            long _call_sample_function(py::object& numpy_rand)
            {
                long X = 0;
                double px = %QN%;
                double U = _call_rand(numpy_rand);
                while (U > px)
                {
                    X++;
                    if (X > %BOUND%)
                    {
                        X = 0;
                        px = %QN%;
                        U = _call_rand(numpy_rand);
                    } else
                    {
                        U -= px;
                        px = ((%N%-X+1) * %P% * px)/(X*%Q%);
                    }
                }
                return X;
            }
            '''.replace('%N%', '%.15f' % n).replace('%P%', '%.15f' % p).replace('%Q%', '%.15f' % q).replace('%QN%', '%.15f' % qn).replace('%BOUND%', '%.15f' % bound)
            hash_defines = '#define _sample_function(_vectorisation_idx) _call_sample_function(_python_rand)'
            dependencies = {'rand': DEFAULT_FUNCTIONS['rand']}

        self.implementations.add_implementation('weave', {'support_code': cpp_code,
                                                          'hashdefine_code': hash_defines},
                                                dependencies=dependencies,
                                                name='_sample_function')