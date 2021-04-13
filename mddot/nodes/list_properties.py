from ..helpers import MDict
from ..logger import logger
from ..nodes import AbstractNode

from mistletoe.block_token import List

class PropertiesListNode(AbstractNode, tokenClass = List):
	# The property list must be text only and follow the format :
	# - key : value
	#
	# EX:
	# - name : John Smith

	# Needed to detect property list node
	condition=lambda b,p: hasattr(p, 'id') and p.id.endswith(".properties")

	def __init__(self, block, parent=None, children=[]):
		super().__init__(block, parent, children)
		self.props = MDict()

		try:
			for item in block.children:
				# Todo support other token type. Only rawtext
				cut_index = item.children[0].children[0].content.index(':') 
				idProp = item.children[0].children[0].content[:cut_index].strip()
				prop = item.children[0].children[0].content[cut_index+1:].strip()
				self.props[idProp] = prop
			logger.verbose("Parsed properties: %s" % self.props)
		except Exception as e:
			logger.error("Unable to parse properties. Do you follow the syntax ? (`- key : value ` in one line without styling token )")
			logger.error(e)

	def __str__(self):
		return "ListPropertiesNode: %s" % self.props

	def generate(self):
		return self.props
		