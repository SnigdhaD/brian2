import numpy as np
from brian2.ImportExport.base import import_export
from brian2.groups import *

# __all__ = ['Dict', 'Pandas']

class DictImportExport(import_export):
    def export_data(self, group, vars=None, units=True, level=0):
		#this function will set the state attributes of the group as get_states (old one)
	data = {}
	for var in vars[1:]:
		data[var] = np.array( group.state(var, use_units=units, level=level+1), copy=True, subok=True)
 	return data

    def import_data(self, group, vars, units, level):
		#this function will return a dict (SAME as set_states)
        for key, value in values.iteritems():
            group.state(key, use_units=units, level=level+1)[:] = value


class PandasImportExport(import_export):
    def export_data(self, group, vars, units, level):
        try:
            import pandas as pd
        except ImportError:
            raise ImportError('Pandas is not installed')
        data = {}
        for var in vars[1:]:
            data[var] = np.array(group.state(var, use_units=units,
                                            level=level+1),
                                 copy=True, subok=True)
     	return pd.DataFrame(data)

    def import_data(self, group, values, units, level):
    	try:
            import pandas as pd 
        except ImportError:
            raise ImportError('Pandas is not installed')
        values = values.to_dict()
    	for key, value in values.iteritems():
            group.state(key, use_units=units, level=level+1)[:] = value

Dict = DictImportExport()
Pandas = PandasImportExport()
