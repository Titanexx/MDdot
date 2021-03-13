from nodes import AbstractNode
from mistletoe.block_token import Heading

import re

class HeaderNode(AbstractNode, tokenClass=Heading):
	# We manage to have only text without styling/link token as header.
	# It's mandatory to use them as identifier inside the docx template

	# If we have more than one child node, we have to add parapgrah by child node.
	# And the first paragraph is set by the jinja token inside the template.
	# <w:p><w:r><w:t>{{ jinja2_token }}</w:t></w:r></w:p>
	rawxml = '</w:t></w:r></w:p>%s<w:p><w:r><w:t xml:space="preserve">' 

	def __init__(self, block, parent=None, children=[]):
		super().__init__(block, parent, children)
		self.level = block.level
		self.content = block.children[0].content
		self._id = re.sub(r'[^A-Za-z0-9]+', '', self.content).lower()

	def __str__(self):
		return "Header %s : %s" % (self.level, self.id)

	def generate(self):
		context = {}
		count_keys = {}
		for child in self.children:
			child_context = child.generate()
			for k,v in child_context.items():
				if k not in context:
					# First paragraph no need to merge
					context[k] = v
					count_keys[k] = 0
				else:
					if k == "xml":
						context[k] += self.rawxml % v
					elif k == "table":
						if type(context[k]) == dict:
							# Create the tables endpoint if there are more than 1 table
							context["tables"] = [context[k]]
						context["tables"].append(v)
					else:
						#Change key if there is already the same sub header _id inside context
						count_keys[k] += 1
						k = "%s%s" % (k,count_keys[k])
						context[k] = v

		return {self._id:context}