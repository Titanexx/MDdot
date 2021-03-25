from nodes import AbstractNode

class RootNode(AbstractNode):
	def __init__(self, files, **args):
		super().__init__(*args)
		self.files = files

	def generate(self):
		context = {}

		for child in self.children:
			context = context | child.generate()

		data = [self.images,self.tables]
		dataKey = ["images",'tables']

		for i in range(len(data)):
			context[dataKey[i]] = {}
			for k,v in data[i].items():
				context[dataKey[i]][k] = v

		return context
