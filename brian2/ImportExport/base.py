from abc import abstractmethod, ABCMeta

from brian2.utils.logger import get_logger

__all__ = ['ImportExport']
logger = get_logger(__name__)

class ImportExport(object):
	__metaclass__ = ABCMeta
	importexport_classes = []

	@staticmethod
	def register(name, importexport_class, index = None):
		name = name.lower()
		for registered_name, _ in ImportExport.importexport_classes:
			if registered_name == name:
				raise ValueError(('An ImportExport class with the name "%s" '
				'has already been registered') % name)

		if not isinstance(importexport_class, ImportExport):
			raise ValueError(('Given importer-exporter of type %s does not seem to be a valid ImportExport class.' % str(type(importexport_class))))
		if not index is None:
			try:
				index = int(index)
				ImportExport.importexport_classes.insert(index, (name, importexport_class))
			except (TypeError, ValueError):
				raise TypeError(('Index argument should be an integer, is '
					'of type %s instead.') % type(index))
		else:
			ImportExport.importexport_classes.append((name, importexport_class))
	


	@staticmethod
	def determine_importexport_type(format):
		for name, importexport_class in ImportExport.importexport_classes:
			if name == format:
				logger.info('Using importexport class "%s"' % name)
				return importexport_class

		raise ValueError(('No importexport class that is suitable for the given '
							'format has been found'))


	@abstractmethod
	def import_data(self, group, data):
		pass

	@abstractmethod
	def export_data(self, group, variables):
		pass
