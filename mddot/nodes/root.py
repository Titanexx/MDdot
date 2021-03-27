from nodes import AbstractNode

class RootNode(AbstractNode):
	def __init__(self, files, **args):
		super().__init__(*args)
		self.files = files

	def generate(self):
		context = {}

		for child in self.children:
			context = context | child.generate()

		return context
