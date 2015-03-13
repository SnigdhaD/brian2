import numpy as np
import pandas as pd
from brian2.ImportExport.base import ImportExport
from brian2.groups import *

__all__ = ['Dict', 'Pandas']

class DictImportExport(ImportExport):
    def export_data(self, group, vars=None, units=True, level=0):
		#this function will set the state attributes of the group as get_states (old one)
        if vars is None:
	    vars = [name for name in group.variables.iterkeys() ]
	for var in vars:
	    data[var] = np.array( group.state(var, use_units=units, level=level+1), copy=True, subok=True)
 	return data

    def import_data(self, group, vars, units, level):
		#this function will return a dict (SAME as set_states)
        for key, value in values.iteritems():
            group.state(key, use_units=units, level=level+1)[:] = value


class PandasImportExport(ImportExport):
    def export_data(self, group, vars, units, level):
        if vars is None:
            vars = [name for name in group.variables.iterkeys()
                    if not name.startswith('_')]
        data = {}
        for var in vars:
            data[var] = np.array(group.state(var, use_units=units,
                                            level=level+1),
                                 copy=True, subok=True)
     	return pd.DataFrame(data)

    def import_data(self, group, values, units, level):
    	values = values.to_dict()
    	for key, value in values.iteritems():
            group.state(key, use_units=units, level=level+1)[:] = value

Dict = DictImportExport()
Pandas = PandasImportExport()
