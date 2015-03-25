from abc import abstractmethod, ABCMeta

from brian2.utils.logger import get_logger

__all__ = ['ImportExport']
logger = get_logger(__name__)

class ImportExport(object):
	__metaclass__ = ABCMeta
	importexport_classes = {}

	@staticmethod
	def register(name, importexport_class):
		name = name.lower()
		if name in ImportExport.importexport_classes:
			raise ValueError(('An ImportExport class with the name "%s" '
				'has already been registered') % name)

		if not isinstance(importexport_class, ImportExport):
			raise ValueError(('Given importer-exporter of type %s does not seem to be a valid ImportExport class.' % str(type(importexport_class))))
		else:
			ImportExport.importexport_classes[name] = importexport_class
	


	@staticmethod
	def determine_importexport_type(format):
		if format in ImportExport.importexport_classes:
			return ImportExport.importexport_classes[format]
		else:	
			raise ValueError(('No importexport class that is suitable for the given '
							'format has been found'))


	@abstractmethod
	def import_data(self, group, data):
		pass

	@abstractmethod
	def export_data(self, group, variables):
		pass
