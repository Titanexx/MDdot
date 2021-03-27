from logger import logger

class Singleton(type):
	_instances = {}
	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
		return cls._instances[cls]

class AbstractModule(metaclass=Singleton):
	MODULES = []

	logger = logger

	def __init_subclass__(cls, **kwargs):
		super().__init_subclass__(**kwargs)
		AbstractModule.MODULES.append(cls)

	def __init__(self,files):
		self.files = files

	def runBeforeParsing(self):
		pass

	def runBeforeRendering(self, context):
		pass

	def runAfterRendering(self,context):
		pass
		