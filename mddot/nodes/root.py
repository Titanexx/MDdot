from nodes import AbstractNode

class RootNode(AbstractNode):
	def __init__(self, mdFilename, template, **args):
		super().__init__(*args)
		AbstractNode.mdFilename = mdFilename
		self.setTemplate(template)

	def generate(self):
		context = {}

		for child in self.children:
			context = context | child.generate()

		for d in [self.images,self.tables]:
			for k,v in d.items():
				context[k] = v

		return context
