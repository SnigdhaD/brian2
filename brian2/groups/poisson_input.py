from brian2.core.variables import Variables
from brian2.core.names import find_name
from brian2.units.fundamentalunits import check_units
from brian2.units.stdunits import Hz
from brian2.utils.binomial import BinomialFunction

@check_units(N=1, rate=Hz)
def PoissonInput(target, target_var, N, rate, weight=1.0, name='poissoninput*'):
    # We need a name already now, to decide the name of the function
    name = find_name(name)
    if not isinstance(weight, basestring):
        weight = repr(weight)

    binomial_sampling = BinomialFunction(N, rate*target.clock.dt)

    updater = target.custom_operation('{targetvar} += {binomial}()*{weight}'.format(targetvar=target_var,
                                                                                    binomial='_binomial_'+name,
                                                                                    weight=weight))
    updater.variables = Variables(updater)
    updater.variables._variables['_binomial_'+name] = binomial_sampling
    return updater


if __name__ == '__main__':
    from brian2 import *
    G = NeuronGroup(10, 'v:1')
    inp = PoissonInput(G, 'v', 1000, 100*Hz, weight=0.1)
    mon = StateMonitor(G, 'v', record=True)
    run(10*ms)
    print inp.codeobj.code
    plot(mon.t/ms, mon.v.T)
    show()
