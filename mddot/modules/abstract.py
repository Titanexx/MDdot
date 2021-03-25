class AbstractModule():
	MODULES = []

	def __init_subclass__(cls, **kwargs):
		super().__init_subclass__(**kwargs)
		AbstractModule.MODULES.append(cls)

	def __init__(self,files):
		self.files = files

	def runFirst(self, context):
		pass

	def runSecond(self,context):
		pass
		