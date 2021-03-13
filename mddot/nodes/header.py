from nodes import AbstractNode
from mistletoe.block_token import Heading

import re

class HeaderNode(AbstractNode, tokenClass=Heading):
	# We manage to have only text without styling token as header.
	# It's mandatory tu use them as identifier inside the docx template
	#
	# Ex:
	# TODO
	xmlconcat = '</w:t></w:r></w:p>%s<w:p><w:r><w:t xml:space="preserve">' # If we have more than 1 children nodes, we have to add parapgrah by children node. And the first paragraph is set by the jinja token inside the template.
	# <w:p><w:r><w:t>{{ jinja2_token }}</w:t></w:r></w:p>

	def __init__(self, block, parent=None, children=[]):
		super().__init__(block, parent, children)
		self.level = block.level
		self.content = block.children[0].content
		self.id = re.sub(r'[^A-Za-z0-9]+', '', self.content).lower()

	def __str__(self):
		return "Header %s : %s" % (self.level, self.id)

	def generate(self):
		context = {
			self.id: {}
		}
		context_id = context[self.id]
		for child in self.children:
			child_generated = child.generate()
			for k,v in child_generated.items():
				if k not in context_id:
					context_id[k] = v
				else:
					context_id[k] += self.xmlconcat % v

		return context